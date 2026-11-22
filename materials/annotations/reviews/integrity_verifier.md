# 独立核验报告：evidence 数据完整性、审计表覆盖与 A2 运行时证据

- 核验人：integrity-verifier（独立机械核验，不代表 Lead/标注员立场）
- 仓库：`D:\ICT\firmware-admission`，HEAD `33660ed`
- 生成时间：2026-11-21T15:34:12+08:00
- 核验对象：12 台固件、13 个 evidence 文件（A2 运行时+静态分开）、198 条 evidence 记录、`materials/annotations/evidence_audit.md` 108 行审计表、A2 运行时原始抓包
- 只读声明：未修改 evidence/configs/源码；未读取 `annotator_B.json`、`materials/decisions/`、其他 review 文件或 Lead 产出；本报告仅写入 `materials/annotations/reviews/` 下两个文件

## 1. 方法

1. 用 `py -3.10` 脚本加载全部 evidence 文件，确认真实 schema：12 个对象文件的顶层键为 `firmware_id/rootfs/counts/evidence`；A2 运行时文件为裸 JSON 数组。
2. 逐条检查 7 个字段（`id/firmware_id/check_code/level/confidence/raw_ref/detail`）是否存在、非空；校验 ID 全局唯一性与格式、`level` 取值、`confidence` 区间、`check_code` 是否属 `configs/baseline.yaml` 的 9 项全集、`raw_ref` 是否符合 `文件:行` 或 `文件@0x偏移`、`detail` 是否含占位符；校验每条记录的 `firmware_id` 与所属文件是否一致、`level` 与静态/运行时文件类型是否匹配。
3. 解析审计表 108 行，与 evidence 做双向集合比对（漏列/虚列/重复），并复算 found 计数、每行 `status`、E1/E2/E3 三列计数与 `raw_ref`。
4. 打开 A2 运行时 raw_ref 所指原始文件（`materials/firmae/dcs_*.txt`），逐行比对断言，并交叉核对 `materials/实验记录.md` 与 `dcs_result.txt` 的佐证。
5. 判定标准依据 `configs/judgement.yaml`（E1=实测、E2=单点仿真实测、E3=静态；禁止静态推断冒充实测）、`configs/baseline.yaml`（9 个 check_code、默认 confidence E1=0.9/E2=0.7/E3=0.5，标注 provisional）。

## 2. 结构完整性结论

总体：**198/198 条记录 7 个必需字段齐全且非空**；record 字段并集恰为 7 字段，无额外必填字段；`level ∈ {E1,E2,E3}`；`confidence ∈ [0,1]`；`check_code` 全部属 9 项全集；`raw_ref` 全部符合两种格式之一；ID 全局唯一（198 个不同 ID）；**未发现把 evidence 标到不属于其 `firmware_id` 的固件**（每条记录 `firmware_id` 与所属文件一致，无张冠李戴）；**未发现 level 与文件类型冲突**（静态文件全部 E3，运行时文件仅 E1/E2）。12 个对象文件的 `counts` 声明（CRED/UNAUTH/EGRESS）与实际计数全部一致。

### 2.1 ID 实际规则（与验收模板存在差异，见问题 9）

| 固件 | 实际 ID 规则 | 示例 |
|---|---|---|
| A1 / A3 / A3-19 / R1 / R2 / R3 | `E-<FW>-NNNN`（无 level 段） | `E-A1-0001`、`E-A3-19-0001`、`E-R3-0001` |
| A2 静态 | `E-A2-NNNN` | `E-A2-0001` |
| A2 运行时 | `E-A2-E<level>-NNNN`（按 level 独立编号） | `E-A2-E1-0001`、`E-A2-E2-0001`、`E-A2-E2-0002` |
| C1–C4 | `E-C<N>t-NNNN`，且记录 `firmware_id=C<N>t` | `E-C1t-0001`（`firmware_id=C1t`） |
| C5 | `E-C5-NNNN`，`firmware_id=C5` | `E-C5-0001` |

即：只有 A2 运行时 3 条带 level 段，其余 195 条不带；C 系列内部命名不统一（C1–C4 带 `t`，C5 不带），与审计表/文件名/任务分配的 C1–C5 标签不一致（问题 1）。

### 2.2 其他字段统计

- `level` 分布：E1=1、E2=2、E3=195。
- `confidence`：E1 0.9×1、E2 0.7×2；E3 中 0.3×141、0.4×32、0.5×22。E1/E2 与 baseline 默认值一致；173 条 E3 低于默认 0.5（`judgement.yaml` 未硬性规定数值，故不构成规则冲突，仅口径偏差，见问题 5）。
- `detail`：197/198 条以 `TODO(measure)` 结尾，仅 `E-A2-E1-0001` 不含（见问题 3）。
- 每台固件条数：A1 32、A2 7（运行时 3+静态 4）、A3 36、A3-19 31、R1 36、R2 35、R3 5、C1 3、C2 3、C3 3、C4 4、C5 3，合计 198。

## 3. 审计表覆盖差异（双向比对）

**结论：零差异。** 12 台逐台的 evidence ID 集合与审计表该固件列出的 ID 集合完全相等：无漏列、无虚列、无重复。每行 `status`（found/not_tested）与 evidence 中该 `check_code` 是否存在完全一致；E1/E2/E3 三列计数与 evidence 的 level 计数逐行一致；审计表 `raw_ref` 与 evidence `raw_ref` 逐条一致；A2 运行时+静态合并为 7 条后 found=5，正确。

### 3.1 复算 found 计数

| 固件 | evidence 条数 | 审计 ID 数 | 漏列 | 虚列 | found | not_tested |
|---|---|---|---|---|---|---|
| A1 | 32 | 32 | 0 | 0 | 5 | 4 |
| A2 | 7 | 7 | 0 | 0 | 5 | 4 |
| A3 | 36 | 36 | 0 | 0 | 5 | 4 |
| A3-19 | 31 | 31 | 0 | 0 | 5 | 4 |
| R1 | 36 | 36 | 0 | 0 | 5 | 4 |
| R2 | 35 | 35 | 0 | 0 | 5 | 4 |
| R3 | 5 | 5 | 0 | 0 | 1 | 8 |
| C1 | 3 | 3 | 0 | 0 | 3 | 6 |
| C2 | 3 | 3 | 0 | 0 | 3 | 6 |
| C3 | 3 | 3 | 0 | 0 | 3 | 6 |
| C4 | 4 | 4 | 0 | 0 | 4 | 5 |
| C5 | 3 | 3 | 0 | 0 | 3 | 6 |
| **合计** | **198** | **198** | **0** | **0** | **47** | **61** |

108 行 = 12 固件 × 9 检查项；found=47、not_tested=61、clear=0，与审计表开头汇总及任务书「A 侧 47 found / 61 not_tested / 0 clear」一致。

**重要限定**：以上只证明「覆盖与一致性」，不证明证据内容为真。问题 1（EGRESS 疑似误报）若成立，found=47 中至少 10 条应剔除，R3 的 found=1 将归零、C1/C2/C3/C5 的 found 各减 1、C4 found 减 1。

## 4. A2 运行时原文核验

原始文件位于 `materials/firmae/`，运行时 evidence 位于 `materials/evidence_runtime_dcs.json`（注意：任务说明中写作 `materials/firmae/evidence_runtime_dcs.json`，实际路径是 `materials/evidence_runtime_dcs.json`；文件本身无问题）。

| ID | 断言 | cited 原文关键行 | 判定 | 说明 |
|---|---|---|---|---|
| E-A2-E1-0001 | admin 空口令 + /home.asp 返回 200/38782 字节 | `dcs_login_home_headers.txt:1` `HTTP/1.1 200 OK`；`:9` `Content-Length: 38782`；`:11-25` 管理页 HTML（dlink.css/cookies.js）；无请求行、无 Authorization | **部分支持** | 文件证实 `/home.asp` 响应 200 且 38,782 字节，支持断言后半；但「HTTP Basic admin/空口令返回 200」的请求与凭据不在该文件。由 `dcs_login_blank.txt:1/:9/:21`（200、Content-Length 516、`document.location.href = "/home.asp"`）、`dcs_result.txt:22`（`default_credential_probe: HTTP Basic admin: -> 200; /home.asp -> 200 (38,782 bytes) [E1]`）及 `materials/实验记录.md:27` 佐证，整体断言成立。 |
| E-A2-E2-0001 | 未认证 GET /HNAP1/ 返回 200 且含 GetDeviceSettingsResponse | `dcs_login_hnap.txt:1` `HTTP/1.1 200 OK`；`:3` `Content-Length: 2619`；`:9` `<GetDeviceSettingsResponse ...>`；无请求行 | **部分支持** | 文件证实 200 与 GetDeviceSettingsResponse；但「GET /HNAP1/」与「未认证」不在该文件。由 `dcs_result.txt:21`（`web_probe: GET / -> 401 Basic realm=DCS-960L; GET /HNAP1/ -> 200 GetDeviceSettingsResponse`）与 `实验记录.md:27` 补证，整体断言成立。 |
| E-A2-E2-0002 | 未认证 HNAP 泄露型号/固件/硬件/MAC | `dcs_login_hnap.txt:9` 单行 XML：`DeviceName`/`ModelName`=DCS-960L、`FirmwareVersion`=1.07、`HardwareVersion`=A1、`DeviceMacId`=52:54:00:12:34:56；`:1` 200 | **支持** | 四类值逐字命中；「未认证」语境见 `dcs_result.txt:21`。另注意 detail 把「固件/硬件」与 A1/1.07 顺序写反（问题 7），不影响泄露结论。 |

三条证据的「未认证/空口令」语境均另有 `dcs_result.txt` 与实验记录支撑，且 `dcs_login_probe.txt:3/5/7`（依次 200、401、401）与 `dcs_login_blank.txt`（200 后跳 /home.asp）与 `admin:` 空口令 200 的结论不矛盾。

## 5. 问题清单（按严重度）

| # | 严重度 | 固件 | 类型 | 摘要 | 建议 |
|---|---|---|---|---|---|
| 1 | **high** | R3、C1–C5 | EGRESS 疑似误报 | R3 全部 5 条与 C1–C5 各 1 条 EGRESS_FIXED_CLOUD_ENDPOINT 的 raw_ref 指向 `/etc/ethertypes`、`/etc/protocols`、`/etc/services`、`init.d/p910nd` 等注册表/脚本文件的注释行，命中的是 `www.iana.org`、`www.lanana.org`、`www.linuxbase.org`、`www.freebsd.org`、`cwmp-data-models.broadband-forum.org` 等文档/命名空间 URL，被表述为「硬编码 http 外联地址」。若属实，R3 唯一 found 检查与 C 系列相应 found 行为误报。rootfs 不在本机（`/mnt/e/...`、`/home/rmua/...`），无法开原文复核 | 人工核对 raw_ref 行；确认是注释/命名空间后剔除这 10 条并下调 found 计数（R3 1→0、C1/C2/C3/C4/C5 各减 1，合计 47→41） |
| 2 | medium | C1–C4 | firmware_id 命名 | 记录内 `firmware_id=C1t..C4t`、ID `E-C1t-...`，与审计表/文件名/任务分配的 C1–C4 不一致；C5 又用 C5，C 系列内部不统一。13 条受影响，按 firmware_id join 会失配 | 统一为 C1–C4，或维护 C1↔C1t 映射表并写进数据字典 |
| 3 | medium | ALL | detail 占位符 | 197/198 条 detail 含 `TODO(measure)`（仅 E-A2-E1-0001 例外）。按本次「detail 不含 TODO/占位符」验收口径属系统性违规；按 `judgement.yaml` fallback「仿真失败记 E3 并标 TODO(measure)」属有意约定 | 由 Lead 裁定：改为结构化字段（如 `pending_measurement`）或书面豁免该约定；不要逐条手工删 |
| 4 | low | A2 | schema 不一致 | `materials/evidence_runtime_dcs.json` 顶层为裸数组，缺 `firmware_id/rootfs/counts` 包装（其余 11 个文件为对象） | 统一包装或在数据字典注明特例 |
| 5 | low | ALL | confidence 口径 | 173/195 条 E3 的 confidence 为 0.3/0.4，低于 baseline 默认 0.5；E1/E2 与默认一致。`judgement.yaml` 无硬性数值要求，非规则冲突 | 统一采用 0.5，或在文档说明 0.3/0.4 的区分含义 |
| 6 | low | A2 | raw_ref 上下文不足 | E-A2-E1-0001 与 E-A2-E2-0001 的 cited 文件无请求行/Authorization，不能自证「空口令」「GET /HNAP1/」「未认证」；需 `dcs_result.txt` 与实验记录补证 | 合并 raw_ref 或补充请求侧抓包；当前结论仍成立 |
| 7 | low | A2 | detail 值映射 | E-A2-E2-0002 detail 写「固件/硬件（A1/1.07）」，原文 `FirmwareVersion=1.07`、`HardwareVersion=A1`，顺序颠倒 | 修正 detail 顺序为「型号/硬件/固件/MAC（DCS-960L / A1 / 1.07 / ...）」 |
| 8 | low | A3、A3-19、R1、R2 | 跨固件同构记录 | A3 与 A3-19 有 20 组 `(check_code, raw_ref, detail)` 完全相同（如 E-A3-0001 ↔ E-A3-19-0001，`webroot_ro/default.cfg:262`）；同族固件可解释，但削弱区分度 | 抽查 2–3 条确认 raw_ref 行在各自 rootfs 存在（本机无 rootfs，未能复核） |
| 9 | low | ALL | ID 格式不统一 | 仅 A2 运行时 3 条为 `E-<FW>-E<level>-NNNN`，其余 195 条为 `E-<FW>-NNNN`；ID 全局唯一且与审计一致 | 在数据字典登记实际规则；不建议为改格式重编号 |

**无 high 级结构问题**（字段缺失、ID 重复、check_code 越界、raw_ref 格式错误、firmware_id 张冠李戴均为 0）。唯一 high 是内容层面的 EGRESS 疑似误报。

## 6. 局限

- 静态 evidence 的 rootfs 不在本机（路径为 Linux 环境 `/mnt/e/...` 与 `/home/rmua/...`），**无法打开 `/etc/*`、`webroot_ro/*` 等原文逐行复核**；除 A2 运行时外，本报告只做机械一致性与自洽性检查。
- 未读取 `annotator_B.json`、`materials/decisions/`、其他 review 与 Lead 产出，故不对双人标注一致性、判定结论合理性发表意见。
- A3/A3-19 等跨固件同构记录是否属误复制，需 raw_ref 原文才能最终确认。

## 7. 结论

- **结构完整性：通过**。198 条记录 7 字段齐全、ID 唯一、枚举/区间/格式全部合法，无固件错标、无 level/文件类型冲突。
- **审计表覆盖：通过（零差异）**。双向 ID 集合、每行 status、E1/E2/E3 计数、raw_ref 均一致；复算 found=47/not_tested=61/clear=0，与汇总一致。
- **A2 运行时证据：2 条 partial、1 条 supported**。三条断言的实质内容均有原文或实验记录支撑；partial 的原因是单条 raw_ref 不含请求/鉴权侧行，建议补引而非否定结论。
- **需 Lead 决策/复核**：(1) EGRESS 疑似误报（high，影响 found 计数）；(2) C1–C4 firmware_id 命名（medium）；(3) `TODO(measure)` 约定是否豁免（medium）。