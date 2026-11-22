# T3-2 策略 demo 记录

- 日期：2026-11-22T18:57:19+08:00
- 环境：WSL netns `admit-demo`，仅 loopback 127.0.0.0/8，无外部网络
- 策略来源：`materials/policy_sample_a3.json`（FQDN / ACL，5 条 permit）
- 映射：`allowed.test` -> 127.0.0.2:8080；`blocked.test` -> 127.0.0.3:8080（不在策略中）
- 证据：HTTP server access log + curl；未安装 tcpdump，不声称 PCAP

## 1. 基线（未下发）
- allowed: HTTP 200（期望 200）
- blocked: HTTP 200（期望 200）

## 2. 下发最小权限 ACL
```text
Chain OUTPUT (policy DROP 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
    0     0 ACCEPT     tcp  --  *      lo      0.0.0.0/0            127.0.0.2            tcp dpt:8080
    0     0 ACCEPT     tcp  --  *      lo      127.0.0.2            0.0.0.0/0            tcp spt:8080
```

## 3. 回放
- allowed: HTTP 200（期望 200）
- blocked: HTTP 000（期望 000/失败）

## 4. 回滚
- allowed: HTTP 200（期望 200）
- blocked: HTTP 200（期望 200）

## 5. 计数（模拟流量，只用于 demo）
- legit_total=1, false_blocks=0 -> false_block_rate=0/1=0.0
- malicious_total=1, missed=0 -> miss_rate=0/1=0.0
