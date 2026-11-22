# 分歧仲裁记录（第三人口径）

- 日期：2026-11-22
- 输入：`annotator_A.json`（王同学）、`annotator_B.json`（苏同学）
- 规模：12 固件 × 9 检查项 = **108 格**
- 一致性（用**原始** A/B 计算，未做任何改写）：

| 指标 | 值 |
|---|---|
| agreement | 0.9352（101/108） |
| Cohen's κ | 0.8659 |
| coverage（按 A 主标注） | 0.4352（47/108） |
| 不一致格数 | **7** |

不一致全部落在同一检查项 `EGRESS_FIXED_CLOUD_ENDPOINT`，且 7 格都是
**A = found / B = not_tested**，没有反方向的分歧。

---

## 1. 逐格仲裁

下表每一行的"依据"都是该固件 evidence 文件里**支撑这一格的唯一证据条目**——
也就是说，这 7 格在 A 侧的全部依据都是同一种东西：`/etc` 系统文件里的规范地址注释，
或 Web 页面里给人点的帮助链接。

| 固件 | 检查项 | A | B | 仲裁建议 | 依据（证据 ID / raw_ref） |
|---|---|---|---|---|---|
| A2 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-A2-0002` / `web/cgi-bin/home.asp:619`：`www.dlink.com` 帮助页超链接，页面给人点，不是设备外联 |
| C1 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-C1t-0002` / `etc/protocols:3`：IANA 协议号表头注释 |
| C2 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-C2t-0003` / `etc/protocols:3`：同上 |
| C3 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-C3t-0003` / `etc/protocols:3`：同上 |
| C4 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-C4t-0003` / `etc/protocols:3`：同上 |
| C5 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-C5-0002` / `etc/protocols:3`：同上 |
| R3 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | **not_tested** | `E-R3-0001` `etc/ethertypes:7`（IANA）、`E-R3-0002` `etc/init.d/p910nd:113`（LANANA）、`E-R3-0003` 同文件 `:28`（LinuxBase）、`E-R3-0004` `etc/services:8`（FreeBSD）、`E-R3-0005` `sbin/tr069@0x65c40`（TR-069 数据模型命名空间） |

**7/7 判 not_tested。**

## 2. 为什么不是 found

1. **这些文件不是设备行为，是发行版自带的公共数据。** `etc/protocols`、`etc/services`、
   `etc/ethertypes` 是 libc/iana 的注册表副本，注释里写 `# http://www.iana.org/...`
   属于规范出处标注。任何一台 Linux 都有，与"这台设备会连哪个云"无关。
2. **帮助页 `<a href>` 不等于外联。** `home.asp:619` 是渲染给人看的链接，设备不会去请求它；
   要证明外联需要 DNS/连接行为或配置项里的主机名，页面锚点两条都不满足。
3. **仓库里已有对照组。** `materials/实验记录.md` 2026-11-20 行记录：OpenWrt 干净对照的
   原始镜像用同一规则得到 EGRESS **6** 条，其中包含 IANA 文档 URL；把 `etc/protocols`、
   `www` 等文件裁掉后 EGRESS 归零。这直接说明该规则度量的是"镜像里出现过 URL"，
   不是"设备会外联"。把这 7 格判 found，等于承认"任何 Linux 固件都连固定云"。

## 3. 另一种口径，以及为什么不采用

如果严格按 `双人标注操作指南.md` §8.2 的字面（"有对应证据 → found"）执行，
这 7 格全部改判 found，A/B 立刻 108/108 全一致、κ = 1.0。

不采用，理由：κ=1.0 在这里不是标注质量好，而是**两个人的分歧被同一条有缺陷的规则
抹平了**。上报 κ=1.0 反而更危险——评委只要抽出 C1 的 `etc/protocols:3` 问一句
"这是设备外联吗"，整份一致性数据就失去可信度。保留 7 格分歧并说明根因，是更强的叙述。

## 4. 影响与后续动作

| 项 | 结论 |
|---|---|
| A/B 原始文件 | **不改**。κ 与 agreement 始终用原始 A/B 计算（指南 §8.3） |
| `annotation_combined.json` | 以 A 为主标注合并，未把仲裁值写回，指标可复算 |
| 覆盖率 | 0.4352 由 A 的 47 个 found 决定；若采信仲裁，B 侧 40 个 found 才是"经复核的阳性" |
| 根因 | `src/evidence.py` 的外联 URL 规则缺白名单（iana/lanana/linuxbase/freebsd/broadband-forum/dlink 帮助页） |
| 修复顺序 | **不能在交付前单方面改规则**：改规则 → evidence 全量重跑 → A/B 两份都要重标 → 指标全部重算。需负责人决定是否本轮做 |

## 5. 数据缺陷（与仲裁无关，但影响可复算性）

- `materials/firmae/evidence_sample_C1..C4.json` 里的 `firmware_id` 写作 `C1t`/`C2t`/`C3t`/`C4t`
  （C5 正常）。任何按 `firmware_id` 关联标注的脚本会**静默丢掉 4 台 36 格**。
  B 侧脚本已做读取归一，证据文件本身未改（属取证材料，改动需 A 侧重跑）。
- 修复建议：统一 evidence 的 `firmware_id` 与 `data/` 目录名，或在 `src/evidence.py`
  输出处做一次归一，避免下游各自打补丁。
