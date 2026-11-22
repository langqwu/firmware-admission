# 策略 demo 说明（T3-2）

> 状态（2026-11-22）：**已在 WSL 隔离 netns 跑过一次**，结果见 `materials/策略demo记录.md` 与 `materials/策略demo/`；以下为可复现命令与录制模板。
> 目标：在隔离环境演示「抓包/端点 → 策略 → 下发 → 拦截 → 回滚」。
> 本文件是命令与验收记录模板；没有真实 PCAP 时用模拟流量/预录回放，视频必须标注“模拟环境”。
> 不在宿主机、办公网或真实设备上执行。

## 1. 输入

- 端点来源：`materials/evidence_sample_*.json` 或影子设备抓包（PCAP）；
- 策略样例：`materials/policy_sample_a3.json`（ACL，FQDN，5 条）；
- 判定/报告：`materials/decision_sample_a3.json`、`materials/report_a3.md`。

## 2. 隔离环境

```bash
# 在 WSL/Linux 的独立 netns 中做，不接触宿主机网络
sudo ip netns add admit-demo
sudo ip netns exec admit-demo ip link set lo up
sudo ip link add veth-demo type veth peer name veth-demo-ns
sudo ip link set veth-demo-ns netns admit-demo
sudo ip addr add 10.99.0.1/24 dev veth-demo
sudo ip link set veth-demo up
sudo ip netns exec admit-demo ip addr add 10.99.0.2/24 dev veth-demo-ns
sudo ip netns exec admit-demo ip link set veth-demo-ns up
```

## 3. 把 FQDN 策略映射到隔离环境

真实 ACL 按域名下发；netns 里用 `/etc/hosts` 或本地 DNS 把允许的域名映射到测试服务器：

```bash
# 允许的目的地址（示例，换成你自己的测试服务）
sudo ip netns exec admit-demo sh -c 'echo "10.99.0.2 allowed.test" >> /etc/hosts'
# 启动一个本地 HTTP 服务作为“允许的目的地”
sudo ip netns exec admit-demo python3 -m http.server 80 --bind 10.99.0.2 &
```

## 4. 下发 ACL（iptables 映射）

`policy.rules` 是平台无关的 ACL 行；在 demo 里映射成 iptables：

```bash
# 默认拒绝出向，只放行策略里允许的 host:port（示例：allowed.test:80）
sudo ip netns exec admit-demo iptables -F
sudo ip netns exec admit-demo iptables -P OUTPUT DROP
sudo ip netns exec admit-demo iptables -A OUTPUT -o lo -j ACCEPT
sudo ip netns exec admit-demo iptables -A OUTPUT -d 10.99.0.2 -p tcp --dport 80 -j ACCEPT
```

## 5. 回放与记录

```bash
# 允许路径：应成功
sudo ip netns exec admit-demo curl -sS -m 3 http://allowed.test/ >/dev/null && echo ALLOW_OK

# 阻断路径：应失败
sudo ip netns exec admit-demo curl -sS -m 3 http://blocked.test/ && echo UNEXPECTED || echo BLOCK_OK
```

记录到 `materials/策略demo记录.md`：

| 项 | 值 |
|---|---|
| 策略来源 | `policy_sample_a3.json` |
| 规则条数 | 5 |
| 允许用例 | 1/1 成功 |
| 阻断用例 | 1/1 成功 |
| 回滚命令 | `sudo ip netns del admit-demo` / `iptables -F` |
| 误杀/漏放 | 按实际回放计数，未测写 `TODO(measure)` |

## 6. 回滚

```bash
sudo ip netns exec admit-demo iptables -F
sudo ip netns exec admit-demo iptables -P OUTPUT ACCEPT
sudo ip netns del admit-demo
sudo ip link del veth-demo 2>/dev/null || true
```

回滚后确认 `ip netns list` 不含 `admit-demo`，并记录回滚耗时/结果。

## 7. 视频录制注意

- 画面先出现“隔离环境 / 模拟流量”角标；
- 不出现真实内网 IP、MAC、域名解析记录；
- 录制前先预跑一次，确保 `iptables`/`curl` 可用；
- 若使用 FirmAE 影子设备抓包，标注“影子设备（FirmAE/QEMU）”。
