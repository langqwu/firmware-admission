# 标注员 A：108 格核验记录

> 任务来源：负责人下发的标注任务分配书（标注员 A；核对机器预填、逐条看 raw_ref、确认/纠正 108 格）。
> 核验日期：2026-11-21；仓库 HEAD：`33660ed`；标注文件：`materials/annotations/annotator_A.json`。
> **历史状态（2026-11-22 证据规则修正后）**：本记录针对旧版 evidence（47 found / 61 not_tested），已不适用于新版；新版 A 为 39/69，需按新版重新核验。
> 结论：**108 格逐条核验完成，`TODO=0`，标签无需修改（47 found / 61 not_tested / 0 clear）；另发现 27 条证据质量问题，上报负责人（不写进 A/B 标注，见第 4 节）。**

## 1. 做法（为什么这次核验比“只看 JSON”更强）

任务书允许 A 以 evidence JSON + 审计表为准，但 JSON 里的 `raw_ref` 只是指针。为了确认“证据真的存在”，本机完成了：

1. **下载全部 12 台固件**到 `data/firmware/`（gitignored），12/12 的 SHA-256 与 `materials/固件获取记录.md` 完全一致；
2. 用 WSL Ubuntu + `binwalk -e -M` 解包 12 台 rootfs（A1/A2/A3/A3-19/R1/R2 为 zip 内 `.bin`，R3/C1–C5 为 `.bin`），12/12 成功；
3. 对 **198 条 evidence** 逐条打开 `raw_ref` 原文：
   - `文件:行号`：读取该行，核对 detail 中的 host / 账号 / 字段 / 接口 token 是否真的出现在该行；
   - `文件@0x偏移`：读取偏移邻域（-96~+320 字节），核对 token 是否真实存在；
   - A2 运行时 3 条：直接核对 `materials/firmae/dcs_login_home_headers.txt`、`dcs_login_hnap.txt`（并交叉 `dcs_result.txt`）。
4. 判定规则按 `materials/双人标注操作指南.md`（第 32/179/249 行）与任务书（§2.2、§3.2、例 7）执行：**证据条目存在且 raw_ref 对得上 → found**；`clear` 必须有真实测试记录（本项目没有，故 0 clear）；其余 `not_tested`；不留 `TODO`。
5. 标注只改 `annotators.A`；未改 evidence、未改 decisions、未看 B 侧文件。

## 2. 核验结果

| 项目 | 结果 |
|---|---|
| 108 格状态 | found **47** / not_tested **61** / clear **0** / TODO **0** |
| 与机器预填相比 | **0 处需改标签**（预填的 found 与 evidence 条目一一对应，not_tested 无对应证据） |
| 198 条 evidence 的 raw_ref | **198/198 可定位**（文件存在、行号/偏移越界 0 处） |
| token 逐字命中 | **198/198**（其中 4 条为变量名大小写差异：`PPPoEPWD`、`RADIO_PASS`，详见 4.2） |
| 审计表 `evidence_audit.md` | 108 行与 evidence 的 ID 集合、E1/E2/E3 计数、raw_ref 完全一致（0 差异） |
| A2 运行时证据 | E1 `/home.asp` 200 + 38,782 字节 **原文命中**；E2 `GET /HNAP1/` 200 + `GetDeviceSettingsResponse`、泄露 DCS-960L/A1/1.07/MAC **原文命中**（以 `dcs_*.txt` 为准） |

### 逐台统计

| 固件 | evidence 条数 | found | not_tested | raw_ref 定位 | token 命中 | 语义缺陷条数 |
|---|---|---|---|---|---|---|
| A1 | 32 | 5 | 4 | 32/32 | 32/32 | 0 |
| A2 | 7 | 5 | 4 | 7/7 | 7/7 | 2 |
| A3 | 36 | 5 | 4 | 36/36 | 36/36 | 3 |
| A3-19 | 31 | 5 | 4 | 31/31 | 31/31 | 3 |
| R1 | 36 | 5 | 4 | 36/36 | 36/36 | 3 |
| R2 | 35 | 5 | 4 | 35/35 | 35/35 | 3 |
| R3 | 5 | 1 | 8 | 5/5 | 5/5 | 5 |
| C1 | 3 | 3 | 6 | 3/3 | 3/3 | 1 |
| C2 | 3 | 3 | 6 | 3/3 | 3/3 | 2 |
| C3 | 3 | 3 | 6 | 3/3 | 3/3 | 2 |
| C4 | 4 | 4 | 5 | 4/4 | 4/4 | 2 |
| C5 | 3 | 3 | 6 | 3/3 | 3/3 | 1 |
| **合计** | **198** | **47** | **61** | **198/198** | **198/198** | **27** |

> 逐条明细（每条 evidence 的 raw_ref、命中状态、原文摘录）见 `materials/annotations/annotator_A_核验明细.json`。
> 说明：`data/unpacked/` 各 rootfs 的文件计数与 `实验记录.md` 里旧的 `find | wc -l` 口径（含目录/符号链接）不同，本记录不引用该计数作为结论。

## 3. A2 运行时证据复核（唯一 E1/E2 来源）

- `E-A2-E1-0001`：`dcs_login_home_headers.txt` 第 1 行为 `HTTP/1.1 200 OK`、第 9 行 `Content-Length: 38782`，与 detail 一致；但该文件只有响应头，没有请求行/Authorization。“admin 空口令”由 `dcs_login_blank.txt` 与 `dcs_result.txt:22` 补证 —— **结论成立，属“部分支持”**。
- `E-A2-E2-0001`/`0002`：`dcs_login_hnap.txt` 命中 200 + `GetDeviceSettingsResponse` + 型号/固件/硬件/MAC；“GET /HNAP1/、未认证”由 `dcs_result.txt:21` 补证 —— **结论成立，属“部分支持/支持”**。
- 因此 A2 的 found（默认口令 E1、未授权 HNAP E2、信息泄露 E2）可以保留，材料中仍应写“E2 单次未认证请求”，不要写成完整利用链。

## 4. 证据质量问题（上报负责人；未改标注）

> 原则：这些问题出在 `src/evidence.py` 的提取规则（E3 启发式），不是 A/B 的标注错误。按现行规则（证据条目存在→found），`annotator_A.json` 保留 found；但建议负责人先修规则、重生成 evidence 再重算双人标注，否则 kappa 建立在错误证据上。

### 4.1 EGRESS 误报 10 条（标准/文档/帮助文本 URL，HTML 超链接）

- `E-R3-0001..0005`：`etc/ethertypes:7`、`etc/init.d/p910nd:28/:113`、`etc/services:8`、`sbin/tr069@0x65c40` —— 命中 `www.iana.org`、`www.lanana.org`、`www.linuxbase.org`、`www.freebsd.org`、`cwmp-data-models.broadband-forum.org`，均是**注册表文件头注释或 TR-069 数据模型命名空间**；R3 唯一的 found 检查就是这 5 条。
- `E-C1t-0002`、`E-C2t-0003`、`E-C3t-0003`、`E-C4t-0003`、`E-C5-0002`：`etc/protocols:3` 的 `# Updated from http://www.iana.org/assignments/protocol-numbers` 注释行。
- `E-A2-0002`：`web/cgi-bin/home.asp:619` 是管理页里的 `<a href="http://www.dlink.com/">` 产品超链接。
- Tenda 家族（A3/A3-19/R1/R2）每台 5 条，其中 4 条同类误报：oray 帮助文本 `Please visit http://www.oray.com for detail.`、`"homePageLink":"http://www.baidu.com"`、yunos/xunlei 页面超链接；仅 `adv.upnp.osurl=http://www.tenda.com.cn/` 属于厂商 URL 配置项。**这 4 格暂保留 found，建议人工裁决。**
- A1 的 4 条（`cloudfi.tendacn.com`、`cloudfi.tenda.com.cn`、`ims.ip-com.com.cn`、`imsen.ip-com.com.cn`）是二进制内真实云平台地址，**无此问题**。

### 4.2 CRED_HARDCODED_SECRET 误报 4 条（未找到硬编码口令字面值）

- `E-A2-0001`：`etc/rc.d/init.d/pppoe.sh:8` 为 ``PPPoEPWD=`userconfig -read NETWORK_V4 PPPoEPWD` ``，**运行时读取用户配置，不是硬编码值**。
- `E-C2t-0002`/`E-C3t-0002`/`E-C4t-0002`：`etc/init.d/wlan-manager:6` 为 `RADIO_PASS="radio:P;"`，是工厂测试的响应标记（P=pass/F=fail），**不是口令**；detail 里的 `radio_pass` 是变量名小写化，raw 原行不存在该字面 token。

### 4.3 受影响的格子（仅当修规则后建议值；当前 A 文件不动）

| 固件 | 检查项 | 现标注 | 语义修正建议 | 依据 |
|---|---|---|---|---|
| A2 | CRED_HARDCODED_SECRET | found | not_tested | E-A2-0001 为运行时读取，无硬编码值 |
| A2 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | E-A2-0002 为 HTML 产品超链接 |
| R3 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | E-R3-0001..0005 全为文档/命名空间 URL |
| C1 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | E-C1t-0002 为 IANA 注册表注释 |
| C2 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | E-C2t-0003 同上 |
| C3 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | E-C3t-0003 同上 |
| C4 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | E-C4t-0003 同上 |
| C5 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | E-C5-0002 同上 |
| C2 | CRED_HARDCODED_SECRET | found | not_tested | E-C2t-0002 为测试响应标记 |
| C3 | CRED_HARDCODED_SECRET | found | not_tested | E-C3t-0002 同上 |
| C4 | CRED_HARDCODED_SECRET | found | not_tested | E-C4t-0002 同上 |

即：11 格“仅靠误报证据”支撑 found（另有 A3/A3-19/R1/R2 共 4 格部分可疑）。若负责人采纳，A 侧 found 会从 47 降到 36（+4 格待裁决）。**在规则修正前不要手工改标注**：B 无法看到 rootfs 原文，按同一规则会标 found，A 单方面改只会制造系统性分歧，kappa 反映的将是规则差异而不是标注质量差异。

### 4.4 其他（中/低）

1. **firmware_id 命名**：C1–C4 的 evidence 里 `firmware_id=C1t/C2t/C3t/C4t`、ID 为 `E-C<N>t-NNNN`，而标注键/审计表/文件名用 C1–C4；跨表 join 会失配（C5 正常）。
2. **运行时 raw_ref 不完整**：A2 的 E1/E2 原始文件只有响应（无请求行/凭据行），断言的“空口令、未认证”依赖 `dcs_result.txt`、`dcs_login_blank.txt` 补证；建议把请求命令也留档。
3. **197/198 条 detail 含 `TODO(measure)`**：与 `configs/judgement.yaml` 的 E3 fallback 约定一致，属有意为之，不是脏数据。
4. **ID 格式**：195/198 条为 `E-<FW>-NNNN`（无 level 段），与验收模板 `E-<FW>-E<level>-NNNN` 不完全一致，不影响功能。
5. **口径提醒**：UNAUTH_MGMT 的 24 条只是二进制/配置里的**接口路径字符串**，未做鉴权实测；SERVICE_LOGIN 是 `passwd` 静态条目，默认口令未验证；ADMIN_WEB 是口令字段，未验证可登录。材料里写“发现”即可，不要写“已验证可利用”（A2 除外）。

## 5. 文件与留痕

- 标注结果：`materials/annotations/annotator_A.json`（本次仅更新 `_note` 记录人工核验完成；108 个标签未变）。
- 逐条明细：`materials/annotations/annotator_A_核验明细.json`（198 条 raw_ref + 12 台 SHA/rootfs 元数据）。
- 审计表补记：`materials/annotations/evidence_audit.md` 末尾“人工核验补记（A 侧）”。
- 实验记录：`materials/实验记录.md` 已追加一行。
- AI 辅助审计（不计入 A/B 双人标注，仅作交叉核对）：`materials/annotations/reviews/semantic_verifier.*`、`materials/annotations/reviews/integrity_verifier.*`。
- 固件/rootfs 在 `data/`（gitignored，不入库）；临时脚本已删除。

## 6. 给负责人的一句话

A 侧 108 格已逐条核验（198/198 raw_ref 打开核对，0 处标签需改，TODO=0）；但 27 条证据是提取器误报（11 格仅靠误报证据 found），建议先修 `src/evidence.py` 的 EGRESS/HARDCODED 规则并重生成 evidence，再继续 B 侧与 kappa，否则双人标注的一致性会建立在错误证据上。