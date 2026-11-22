# 分歧仲裁记录（第三人口径）

- 日期：2026-11-22（v2：补 CRED_HARDCODED_SECRET 4 格，原 v1 只处理 EGRESS 7 格）
- 输入：`annotator_A.json`（王同学）、`annotator_B.json`（苏同学）
- 规模：12 固件 × 9 检查项 = **108 格**
- 一致性（用**原始** A/B 计算，未做任何改写）：

| 指标 | v2（本版） | v1（仅 EGRESS） |
|---|---|---|
| agreement | **0.8981**（97/108） | 0.9352（101/108） |
| Cohen's κ | **0.7871** | 0.8659 |
| coverage（按 A 主标注） | 0.4352（47/108） | 同 |
| 不一致格数 | **11** | 7 |

不一致全部是 **A = found / B = not_tested**，没有反方向分歧，也没有一格的 B 比 A 更激进。

---

## 1. 结论先行：11 格，两个检查项，全部是提取器误报

| 组 | 格数 | 检查项 | 误报性质 |
|---|---|---|---|
| 甲组 | 7 | `EGRESS_FIXED_CLOUD_ENDPOINT` | 把 `/etc` 注册表文件里的规范注释、Web 页面里的帮助超链接当成设备外联端点 |
| 乙组 | 4 | `CRED_HARDCODED_SECRET` | 把"口令字段名"当成"硬编码口令值"；实际是运行时读取或工厂测试标记 |

**关键交叉验证**：A 侧（王同学）在 PR #1 里独立做了 198 条 raw_ref 逐行核对，其 §4.3 给出的
"语义修正建议"表恰好也是这 **11 格**，并预测"若采纳，A 侧 found 会从 47 降到 36"。
B 侧在**没有看 A 的标注**的前提下独立判读，结果正是 **36**。
两条路径（A 看原文、B 看证据元数据）落点相同，这是本份材料里最强的一处互证。

## 2. 甲组：EGRESS 7 格

| 固件 | 检查项 | A | B | 仲裁建议 | 依据（证据 ID / raw_ref） |
|---|---|---|---|---|---|
| A2 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-A2-0002` / `web/cgi-bin/home.asp:619`：`www.dlink.com` 帮助页超链接 |
| C1 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-C1t-0002` / `etc/protocols:3`：IANA 协议号表头注释 |
| C2 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-C2t-0003` / `etc/protocols:3`：同上 |
| C3 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-C3t-0003` / `etc/protocols:3`：同上 |
| C4 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-C4t-0003` / `etc/protocols:3`：同上 |
| C5 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-C5-0002` / `etc/protocols:3`：同上 |
| R3 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-R3-0001..0005`：`etc/ethertypes:7`(IANA)、`etc/init.d/p910nd:113`(LANANA)、同文件 `:28`(LinuxBase)、`etc/services:8`(FreeBSD)、`sbin/tr069@0x65c40`(TR-069 命名空间) |

**为什么不是 found**：

1. `etc/protocols`、`etc/services`、`etc/ethertypes` 是 libc 附带的注册表副本，注释里写
   `# http://www.iana.org/...` 是规范出处标注，任何一台 Linux 都有，与"这台设备连哪个云"无关。
2. `home.asp:619` 的 `<a href>` 是渲染给人点的链接，设备不会请求它；要证明外联需要 DNS/连接
   行为或配置项里的主机名，页面锚点两条都不满足。
3. **仓库内自带对照组**：`materials/实验记录.md` 2026-11-20 行记 OpenWrt 干净对照用同一规则
   报出 EGRESS **6** 条（含 IANA 文档 URL），裁掉 `etc/protocols`、`www` 等文件后归零。
   这直接说明该规则度量的是"镜像里出现过 URL"，不是"设备会外联"。

## 3. 乙组：CRED_HARDCODED_SECRET 4 格

| 固件 | 检查项 | A | B | 仲裁建议 | 依据（证据 ID / raw_ref / 原文） |
|---|---|---|---|---|---|
| A2 | CRED_HARDCODED_SECRET | found | not_tested | **not_tested** | `E-A2-0001` / `etc/rc.d/init.d/pppoe.sh:8`：``PPPoEPWD=`userconfig -read NETWORK_V4 PPPoEPWD` `` —— 运行时从设备配置读取，脚本里没有口令字面量 |
| C2 | CRED_HARDCODED_SECRET | found | not_tested | **not_tested** | `E-C2t-0002` / `etc/init.d/wlan-manager:6`：`RADIO_PASS="radio:P;"` —— `P` 是工厂测试 pass 标记，不是口令 |
| C3 | CRED_HARDCODED_SECRET | found | not_tested | **not_tested** | `E-C3t-0002` / 同上 |
| C4 | CRED_HARDCODED_SECRET | found | not_tested | **not_tested** | `E-C4t-0002` / 同上 |

**为什么不是 found**：

1. 这 4 条的 `detail` 是同一模板：「静态发现口令字段 *X*（值已脱敏，长度 *N*）；是否默认/可用
   待实测 TODO(measure)」——**证据自己就声明了没有验证"这是口令"**。
2. **长度指纹可独立交叉**：C2/C3/C4 报 `radio_pass` 长度 **7**，而 `radio:P` 正好 7 个字符；
   三个不同固件同一文件同一行同一长度，指向同一个字符串常量。
3. `pppoe.sh` 的 `PPPoEPWD` 后面跟的是命令替换（反引号里的 `userconfig -read`），不是引号字面量。
   静态提取器把"字段名 + 赋值的值"整体长度当口令长度，于是把运行时配置读成了硬编码。

**证据来源的诚实说明**：B 侧没有解包 rootfs，无法亲自打开这两行原文。乙组的"原文内容"引自
A 侧 PR #1 §4.2（那份材料做了 198/198 raw_ref 逐行核对），B 侧独立贡献的是
①`detail` 自带 `TODO(measure)` 这一自证；②`长度 7` 与 `radio:P` 的指纹吻合。
两方在互不知情的情况下判到同一结果（A §4.3 表 11 格 ∩ B 判读 11 格 = 11），可供复核。

## 4. 为什么保留分歧，而不是抹平成 κ=1.0

若按 `双人标注操作指南.md` §8.2 的字面口径（"有对应证据 → found"），这 11 格全部回到 found，
A/B 立刻 108/108 全一致、κ = 1.0。

不采用，理由有三：

1. **κ=1.0 在这里是坏消息**。两个人被同一条有缺陷的规则抹平，一致性度量的就不是判读质量。
2. **A 侧自己也不认这些标签**。王同学的 PR #1 明确写"11 格 found 仅靠误报证据"，只是按规则
   没改标签。若 B 也照抄，等于两个人一起把明知有问题的标签包装成"高一致性"。
3. **κ=0.7871 有解释力**。11 格分歧全部可归因到两条具体规则（EGRESS URL 白名单缺失、
   CRED 只认字段名不认值形态），修复后 κ 会自然回升。这比一个无法解释的 1.0 更能说明系统状态。

对照表：

| 口径 | A found | B found | 一致格 | agreement | κ | 可解释性 |
|---|---|---|---|---|---|---|
| 字面（证据条目存在即 found） | 47 | 47 | 108 | 1.0000 | 1.0000 | 无法解释为何"任何 Linux 都连 IANA" |
| 语义（本版，按证据有效性） | 47 | 36 | 97 | 0.8981 | 0.7871 | 11 格全部指到两条规则缺陷 |

## 5. 影响与后续动作

| 项 | 结论 |
|---|---|
| A/B 原始文件 | **不改**。κ 与 agreement 始终用原始 A/B 计算（指南 §8.3） |
| `annotation_combined.json` | 以 A 为主标注合并，未把仲裁值写回，指标可复算 |
| coverage | 0.4352 由 A 的 47 个 found 决定；B 的 36 个 found 是"经语义复核的阳性" |
| 根因 | ①`src/evidence.py` 外联 URL 规则缺白名单；②CRED 规则只匹配字段名，不校验值形态 |
| 修复顺序 | 改规则 → evidence 全量重跑 → A/B 两份重标 → 指标重算。**不要只改标注不改规则** |
| 谁的活 | 规则属 `src/evidence.py`，改完 A 侧需重跑（他有 rootfs 与解包环境），B 侧重跑本脚本即可 |

## 6. 数据缺陷（与仲裁无关，但影响可复算性）

- `materials/firmae/evidence_sample_C1..C4.json` 的 `firmware_id` 写作 `C1t`/`C2t`/`C3t`/`C4t`
  （C5 正常），ID 为 `E-C<N>t-NNNN`。按 `firmware_id` 关联标注的脚本会**静默丢掉 4 台 36 格**。
  B 侧脚本已做读取归一，证据文件未动（属 A 侧取证材料）。
- 建议：在 `src/evidence.py` 输出处统一归一 `firmware_id`，别让下游各自打补丁。
