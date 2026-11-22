# T3-2 策略 demo 记录

> 目标：在隔离环境演示「端点 → 最小权限 ACL → 下发 → 允许/阻断 → 回滚」。
> 日期：2026-11-22。环境：WSL Ubuntu 22.04 `netns admit-demo`，只使用 loopback `127.0.0.0/8`，不接触宿主机/外部网络。
> 说明：本机未安装 tcpdump；用本地 HTTP server access log + curl 状态作为回放证据，**不声称 PCAP**。

## 1. 输入

- 策略来源：`materials/policy_sample_a3.json`（AC15，FQDN / ACL，5 条 `permit`）
- 演示映射（只在 netns 内）：
  - `allowed.test` → `127.0.0.2:8080`
  - `blocked.test` → `127.0.0.3:8080`（不在策略允许列表）
- 回滚引用：`policy.rollback_ref`（样例中为 `rb-A3`）

## 2. 结果

| 阶段 | allowed（策略内） | blocked（策略外） |
|---|---|---|
| 基线（未下发） | HTTP 200 | HTTP 200 |
| 下发最小权限 ACL 后 | HTTP 200 | HTTP 000（连接失败） |
| 回滚后 | HTTP 200 | HTTP 200 |

下发的 netns OUTPUT 规则：

```text
Chain OUTPUT (policy DROP)
ACCEPT tcp -- lo  any -> 127.0.0.2 tcp dpt:8080
ACCEPT tcp -- lo  127.0.0.2 -> any tcp spt:8080
```

回滚：`iptables -F` + `iptables -P OUTPUT ACCEPT`，随后删除 netns。

## 3. 计数（模拟流量，只用于 demo）

| 项 | 值 |
|---|---|
| legit_total | 1 |
| false_blocks | 0 |
| false_block_rate（demo） | **0/1 = 0.0** |
| malicious_total | 1 |
| missed | 0 |
| miss_rate（demo） | **0/1 = 0.0** |

> 这不是生产流量的误杀/漏放率；真实比例仍需 PCAP/策略回放，材料中不要把 demo 的 0.0 写成最终指标。

## 4. 原始文件

- 执行脚本：[run_demo.sh](策略demo/run_demo.sh)
- 自动结果：[result.md](策略demo/result.md)
- 允许路径访问日志：[server_allowed.log](策略demo/server_allowed.log)
- 阻断路径访问日志：[server_blocked.log](策略demo/server_blocked.log)

## 5. 复现

```bash
wsl -d Ubuntu-22.04 -u root -- bash "/mnt/e/dsh_talking/firmware-admission/materials/策略demo/run_demo.sh"
```

脚本会自行清理 `admit-demo` netns；验证：

```bash
ip netns list | grep admit-demo || echo NO_DEMO_NS
```

## 6. 限制

- 只有 1 条 allowed + 1 条 blocked，**N=1**，不能算统计显著；
- 本机无 tcpdump，未生成 PCAP；只有 HTTP 访问日志和 curl 状态；
- 真实策略回放需要把 FQDN 映射到影子设备实际端点，并统计正常/恶意流量；
- 视频录制时画面标注“隔离环境 / 模拟流量”，不出现真实内网 IP/MAC/域名解析记录。
