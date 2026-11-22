# PPT 大纲（12–15 页，初赛版）

> 目标：12 月 14 日前定稿；每页只讲一个评分点，数字必须来自 `materials/实验记录.md` / `materials/指标表.md`。
> 评分对齐：创新性 60% + 应用价值 40%；五个必含项：背景价值 / 创新性 / 数据集与处理 / 关键代码 / 可量化指标。

| 页 | 标题 | 要点 | 素材 |
|---|---|---|---|
| 1 | 封面 | 作品名《入网体检》；一句话：上传固件 → 影子设备实测 → 能不能进网 + 放行什么 + 同族影响面；队伍/学校 | 项目名、队名 |
| 2 | 问题：设备上线前的安全判断是空的 | 校园/园区 IoT 设备先上线再补安全；NAC/微隔离要求“先跑起来才能学”；采购验收只看功能 | `docs/00` §1、信息表背景节 |
| 3 | 现有方案的结构性缺口 | 802.1X/NAC/微分段：先上线→再学习→后收紧；未部署设备没有流量，无法生成策略 | 对比图 |
| 4 | 我们的答案：上线前给结论 | 影子设备（FirmAE/QEMU 隔离仿真）→ 三类取证 → 证据分级 → 三态判定 → 最小权限策略 | 八段流水线图 |
| 5 | 创新点一：证据分级决策 | E1 实测 / E2 单点 / E3 静态；仿真失败强制降级 E3；每条 raw_ref 可追溯；不把静态推断写成实测 | `configs/judgement.yaml`、`src/evidence.py` |
| 6 | 创新点二：判定口径可解释 | 阳性发现按风险累计；未测按最坏；保障度不足只能条件放行；Critical E1 硬红线 | `materials/判定口径-T2-1.md`、`src/exposure.py` |
| 7 | 创新点三：策略与判定同源、可回滚 | 端点 → FQDN/vendor-group/ASN；ACL/MUD；`asn-fallback` 显式；`rollback_ref` 必填 | `src/policy.py`、`configs/baseline.yaml` |
| 8 | 数据集：三锚点 + 12 固件 | A1 Tenda O4 V3.0、A2 D-Link DCS-960L 1.07.102、A3 Tenda AC15 V15.03.05.18；**12/12 文件已获取（6 摄像头 / 6 路由）**，SHA-256 与直链见数据集说明；其余 9 个为样本，不冒充锚点 | `configs/anchors.yaml`、`materials/数据集说明.md` |
| 9 | 数据集处理：解包与取证 | binwalk 封装；AC15 841 文件/1.488 s、DCS-960L 1133 文件/1.432 s、O4 614 文件；R1 748、R2 780、R3 1695、C1 971、C2 783、C3 790、C4 785、C5 978；静态证据 A3 36、R1 36、R2 35、R3 5、C1–C5 3/3/3/4/3 | `materials/实验记录.md`、`materials/firmae/` |
| 10 | 实验：影子设备跑分 | AC15 armel 启动成功/Web 失败；DCS mipseb 启动+Web+HNAP 200+`admin:` 空口令 E1；O4 mipsel 启动/网络可达/Web 未检出（timebox） | `materials/firmae/` |
| 11 | 证据链样例 | AC15 `sys.baseuserpass`、`/goform/telnet`；DCS `admin:` 默认口令 E1 + 未认证 HNAP E2；每条 level/confidence/raw_ref | `materials/report_a3.md`、`materials/report_fail_a2.md` |
| 12 | 判定样例 | **12 台：conditional 11 / reject 1 / pass 0**；A2 E1 默认口令 → reject（U=0.932/A=0.299/conf=0.900）；A1/A3/R1–R3/C1–C5 为 E3-only conditional；pass 用 OpenWrt lab control 单列 | `materials/判定分布-12固件.md`、`materials/decisions/` |
| 13 | 策略样例与 demo | A1/A2/A3 ACL 4/1/5 条；FQDN；`asn-fallback` 0/3（真实样例），ASN 路径由单测覆盖；netns demo：基线 200/200、下发 200/000、回滚 200/200 | `materials/policy_sample_a*.json`、`materials/策略demo记录.md` |
| 14 | 指标与验证 | 内核启动 3/3、Web 1/3；DCS 默认口令 E1；标注 AI 预标 + 人工核验（coverage 0.3611，不报告 human κ）；策略 demo 误杀/漏放 0/1、0/1（模拟） | `materials/指标表.md`、`src/metrics.py` |
| 15 | 落地与路线 | 校园/园区网管场景、等保最小授权、可复制性；CodeArts/RDS/Redis 留痕；下一步 FirmAE/标注/策略 demo | 部署方案、实验记录 |

## 讲述节奏（15 分钟版）

- 0–2 min：问题与现有方案缺口（页 2–3）；
- 2–6 min：三个创新点（页 5–7），重点讲“为什么 E1 不能算 0”；
- 6–9 min：数据与实验（页 8–10），只讲有来源的数字；
- 9–12 min：证据/判定/策略样例（页 11–13）；
- 12–15 min：指标、落地与路线（页 14–15）。

## 制作注意

- E3-only 的页面必须加“静态初判，未实测”角标；
- 不把 A1/A2/A3 的 `conditional` 说成“通过”或“拒绝”；
- 图表中每个数字标注来源（实验记录行/JSON 文件）；
- CodeArts 截图、模型名单独一页或页脚留痕。
