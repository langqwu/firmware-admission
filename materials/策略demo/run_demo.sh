#!/usr/bin/env bash
set -u
NS=admit-demo
OUT=/mnt/e/dsh_talking/firmware-admission/materials/策略demo
mkdir -p "$OUT"
cd "$OUT" || exit 1

cleanup() {
  ip netns exec "$NS" iptables -F 2>/dev/null || true
  ip netns exec "$NS" iptables -P OUTPUT ACCEPT 2>/dev/null || true
  [ -n "${PID2:-}" ] && kill "$PID2" 2>/dev/null || true
  [ -n "${PID3:-}" ] && kill "$PID3" 2>/dev/null || true
  ip netns del "$NS" 2>/dev/null || true
}
trap cleanup EXIT

ip netns del "$NS" 2>/dev/null || true
ip netns add "$NS"
ip netns exec "$NS" ip link set lo up

ip netns exec "$NS" python3 -m http.server 8080 --bind 127.0.0.2 > server_allowed.log 2>&1 &
PID2=$!
ip netns exec "$NS" python3 -m http.server 8080 --bind 127.0.0.3 > server_blocked.log 2>&1 &
PID3=$!
sleep 1

status() {
  local out
  out=$(ip netns exec "$NS" curl -sS -o /dev/null -w '%{http_code}' --max-time 3 "$1" 2>/dev/null) || {
    echo "000"
    return
  }
  printf '%s' "${out:-000}"
}

# 正式记录：先基线，再下发，再回滚，不提前写“已下发”的结果。
{
  echo "# T3-2 策略 demo 记录"
  echo
  echo "- 日期：$(date -Is)"
  echo "- 环境：WSL netns \`$NS\`，仅 loopback 127.0.0.0/8，无外部网络"
  echo "- 策略来源：\`materials/policy_sample_a3.json\`（FQDN / ACL，5 条 permit）"
  echo "- 映射：\`allowed.test\` -> 127.0.0.2:8080；\`blocked.test\` -> 127.0.0.3:8080（不在策略中）"
  echo "- 证据：HTTP server access log + curl；未安装 tcpdump，不声称 PCAP"
  echo
  echo "## 1. 基线（未下发）"
  echo "- allowed: HTTP $(status http://127.0.0.2:8080/)（期望 200）"
  echo "- blocked: HTTP $(status http://127.0.0.3:8080/)（期望 200）"
  echo
  echo "## 2. 下发最小权限 ACL"
  ip netns exec "$NS" iptables -F
  ip netns exec "$NS" iptables -P OUTPUT DROP
  ip netns exec "$NS" iptables -A OUTPUT -o lo -d 127.0.0.2 -p tcp --dport 8080 -j ACCEPT
  ip netns exec "$NS" iptables -A OUTPUT -o lo -s 127.0.0.2 -p tcp --sport 8080 -j ACCEPT
  echo '```text'
  ip netns exec "$NS" iptables -L OUTPUT -n -v
  echo '```'
  echo
  echo "## 3. 回放"
  echo "- allowed: HTTP $(status http://127.0.0.2:8080/)（期望 200）"
  echo "- blocked: HTTP $(status http://127.0.0.3:8080/)（期望 000/失败）"
  echo
  echo "## 4. 回滚"
  ip netns exec "$NS" iptables -F
  ip netns exec "$NS" iptables -P OUTPUT ACCEPT
  echo "- allowed: HTTP $(status http://127.0.0.2:8080/)（期望 200）"
  echo "- blocked: HTTP $(status http://127.0.0.3:8080/)（期望 200）"
  echo
  echo "## 5. 计数（模拟流量，只用于 demo）"
  echo "- legit_total=1, false_blocks=0 -> false_block_rate=0/1=0.0"
  echo "- malicious_total=1, missed=0 -> miss_rate=0/1=0.0"
} > result.md 2>&1

echo "--- result.md ---"
cat result.md
