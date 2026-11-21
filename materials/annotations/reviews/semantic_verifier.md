# 语义核验报告（独立核验员 semantic-verifier）

- 核验对象：`materials/annotations/annotator_A.json`（标注员 A，机器预填版）12 台固件 × 9 检查项 = **108 格**
- 对照基准：`configs/baseline.yaml`（9 项定义 / 权重 / 证据等级口径）、`configs/judgement.yaml`（E1/E2/E3 判定）、`materials/双人标注操作指南.md` §3–4、任务书（标注人员分配）
- 仓库 HEAD：`33660ed`
- 机器可读结果：`materials/annotations/reviews/semantic_verifier.json`（本报告所有数字与其一致）
- 独立性：本核验只读 evidence / 配置 / 指南与 A 侧预填；**未**读 `annotator_B.json`、`materials/decisions/`、`evidence_audit.md`、`machine_prelabel_A.json`、其他 review 文件或 Lead 任何产出。

---

## 1. 结论摘要

| 指标 | 数值 |
|---|---|
| confirm（预填成立） | **101** |
| correct_to_not_tested（应改） | **6** |
| correct_to_found（漏标） | **0** |
| unsure（需人工裁决） | **1** |
| 合计 | 108 |

预填分布：**47 found / 61 not_tested / 0 clear**。经核验：47 个 found 中 40 个成立、6 个应改 not_tested、1 个存疑；61 个 not_tested 全部成立；**未发现“有证据却填 not_tested”的漏项**，亦无 clear 格需要纠正（A 侧无 clear）。

偏差全部集中在 `EGRESS_FIXED_CLOUD_ENDPOINT` 一项：证据提取器把**标准组织/规范文档 URL** 当成“云平台/厂商服务端外联地址”。若采纳 6 处纠正，A 侧将变为 **41 found / 67 not_tested**，R3 变为 9 项全 not_tested。

---

## 2. 核验方法

1. **建基准**：从 `configs/baseline.yaml` 取 9 项的准确定义、权重与 source（静态检索 / 影子设备抓包 / 抓包+abuse.ch），从 `configs/judgement.yaml` 取 E1/E2/E3 口径（E1=实测请求-响应复现；E2=仿真单点探测未成链；E3=静态推断未运行验证；仿真失败一律降 E3）。
2. **按格取证**：按固件汇总 evidence（A2 = 运行时 `evidence_runtime_dcs.json` + 静态 `evidence_sample_a2.json` 合看），逐 `check_code` 分组；确认 `annotator_A.json` 的 found 恰好等于“evidence 中存在同 check_code 条目”（脚本断言 108 格无一 MISMATCH）。
3. **found 判定标准**：存在同 check_code 条目，**且** detail / raw_ref 指示的事实类型与 baseline 定义相符。按指南 §3.3/§4.4 与分配书例 1，**E3 静态同类发现可以填 found，且 found 只表示“找到风险”，不表示已验证可利用**；但以下不算：标准组织/文档/许可证 URL、与定义无关的任意字符串、仅有接口名而无鉴权结论的“访问证据”。
4. **not_tested 判定**：确认无同 check_code 条目且无实测/抓包记录；同时反向检查有无同类证据被挂到别项而应改判（发现 Tenda 组 DownloadCfg/DownloadSyslog 等接口条目挂在 UNAUTH_MGMT_ENDPOINT 下，未验证未授权读取，不构成 UNAUTH_INFO_DISCLOSURE 证据，维持 not_tested）。
5. **raw 复核**：A2 运行时 raw 文件（`materials/firmae/dcs_result.txt`、`dcs_login_home_headers.txt`、`dcs_login_hnap.txt`、`dcs_https_root.txt`）在仓库内，逐份复核；其余 raw_ref 指向固件解包 rootfs（如 A1 `rootfs=/home/rmua/t12/...`），仓库无 `data/` 与 rootfs，无法逐行复核，只能按 detail + ref 路径语义判断。
6. **不臆测**：争议格不强行判，记 unsure 并写清争议点与建议裁决路径。

---

## 3. 偏差表（7 格）

| # | 固件 | 检查项 | 预填 | 建议 | evidence | 理由 |
|---|---|---|---|---|---|---|
| 1 | R3 | EGRESS_FIXED_CLOUD_ENDPOINT | found | **not_tested** | E-R3-0001..0005 | 5 条证据全为 `etc/ethertypes:7`（www.iana.org）、`etc/init.d/p910nd:113`（www.lanana.org）、`p910nd:28`（www.linuxbase.org）、`etc/services:8`（www.freebsd.org）、`sbin/tr069@0x65c40`（cwmp-data-models.broadband-forum.org），均为标准组织/规范文档 URL，非云平台或厂商服务端外联地址 |
| 2 | C1 | EGRESS_FIXED_CLOUD_ENDPOINT | found | **not_tested** | E-C1t-0002 | 唯一证据 `etc/protocols:3` 中 www.iana.org，属 IANA 协议注册表文件头引用，非外联地址 |
| 3 | C2 | EGRESS_FIXED_CLOUD_ENDPOINT | found | **not_tested** | E-C2t-0003 | 同上，`etc/protocols:3` www.iana.org |
| 4 | C3 | EGRESS_FIXED_CLOUD_ENDPOINT | found | **not_tested** | E-C3t-0003 | 同上，`etc/protocols:3` www.iana.org |
| 5 | C4 | EGRESS_FIXED_CLOUD_ENDPOINT | found | **not_tested** | E-C4t-0003 | 同上，`etc/protocols:3` www.iana.org |
| 6 | C5 | EGRESS_FIXED_CLOUD_ENDPOINT | found | **not_tested** | E-C5-0002 | 同上，`etc/protocols:3` www.iana.org |
| 7 | A2 | EGRESS_FIXED_CLOUD_ENDPOINT | found | **unsure** | E-A2-0002 | 唯一证据 `web/cgi-bin/home.asp:619` 硬编码 www.dlink.com。D-Link 是设备厂商，字面属“厂商服务端地址”；但该 ref 位于管理页模板，可能是超链接/版权链而非实际外联调用地址，且该固件无二进制/API 云端点证据，raw 不在仓库内无法核实上下文。**建议人工查看 home.asp:619 原文：若为页面超链接 → not_tested；若为实际外联请求地址 → found** |

> 说明：#1–#6 属同一类系统性误报（静态检索把标准 URL 当外联端点），与“标准组织/文档 URL 不算 found”的核验标准一致；该 6 格纠正后，C1–C5 的 found 数各减 1，R3 仅剩的 1 个 found 归零。

---

## 4. 逐台小结

| 固件 | found | 确认 | 纠正 | 存疑 | 核验要点 |
|---|---|---|---|---|---|
| A1 | 5 | 5 | 0 | 0 | EGRESS 4 条真实厂商云域名（cloudfi.tendacn.com、ims/imsen.ip-com.com.cn、cloudfi.tenda.com.cn）成立；CRED 由 default.cfg 口令字段 / passwd 账号 / shadow 哈希支撑；UNAUTH_MGMT 24 条仅为接口字符串（鉴权未验证，E3 口径，材料勿写成“未授权访问已验证”）。注意 ip-com.com.cn 与 Tenda 品牌归属差异，建议后续复核该产品线是否同族。 |
| A2 | 5 | 4 | 0 | 1 | 运行时 E1/E2 已用 `dcs_*.txt` 复核成立：admin/空口令 Basic → 200 + `/home.asp` 38,782 字节；admin:admin、admin:password 均 401；未认证 `/HNAP1/` → 200 GetDeviceSettingsResponse（DCS-960L / 1.07 / A1 / MAC）。静态 CRED_HARDCODED（pppoe.sh pppoepwd）成立。**EGRESS 唯一证据 www.dlink.com 存疑（见偏差表 #7）**。 |
| A3 | 5 | 5 | 0 | 0 | EGRESS 由 `bin/phddns@0xd3f5` 内 www.oray.com（花生壳云 DDNS）+ default.cfg www.tenda.com.cn 支撑，成立；www.baidu.com（WifiPowerGet.txt 连通性测试）属噪声但不影响本格成立。CRED_SERVICE（passwd 多账号 + FTP/Samba 口令字段）、CRED_ADMIN（sys.baseuserpass）、CRED_HARDCODED（shadow）、UNAUTH_MGMT（DownloadCfg 等接口串）按 E3 口径成立。 |
| A3-19 | 5 | 5 | 0 | 0 | 与 A3 同构，结论相同（厂商云域名 oray/tenda 支撑 EGRESS）。 |
| R1 | 5 | 5 | 0 | 0 | 与 A3 同构，结论相同。 |
| R2 | 5 | 5 | 0 | 0 | 与 A3 同构，结论相同。 |
| R3 | 1 | 0 | 1 | 0 | 仅 5 条 EGRESS 证据，全为标准/文档 URL（iana / lanana / linuxbase / freebsd / broadband-forum），**纠正后 9 项全 not_tested**；该固件证据量最少，建议补采。 |
| C1 | 3 | 2 | 1 | 0 | CRED_SERVICE（`etc/passwd:1` root，shell=/bin/ash）成立；UNAUTH_MGMT（uhttpd 内 /cgi-bin/luci 字符串）按 E3 成立；**EGRESS 的 www.iana.org 纠正**。 |
| C2 | 3 | 2 | 1 | 0 | 同上 + CRED_HARDCODED（`etc/init.d/wlan-manager:6` radio_pass）成立；**EGRESS 纠正**。 |
| C3 | 3 | 2 | 1 | 0 | 同上（passwd root + radio_pass + luci）；**EGRESS 纠正**。 |
| C4 | 4 | 3 | 1 | 0 | passwd root + radio_pass + uhttpd luci；**EGRESS 纠正**。 |
| C5 | 3 | 2 | 1 | 0 | passwd root + uhttpd luci；**EGRESS 纠正**。 |

合计：confirm 101（40 found + 61 not_tested）、correct 6、unsure 1。

---

## 5. 证据层面疑点（供 Lead 与证据维护者参考）

1. **EGRESS 提取器系统性误收标准/文档 URL**：iana.org、lanana.org、linuxbase.org、freebsd.org、broadband-forum.org 被标为“外联地址”，直接造成 R3 全 5 条、C1–C5 各 1 条误报。建议在静态检索规则中加**标准组织域名/文档清单黑名单**，并要求“域名出现在 HTTP 客户端调用上下文（URL 拼接、connect/sendto 邻近字符串）”才算端点。
2. **baidu 连通性测试噪声**：A3/A3-19/R1/R2 的 `webroot_ro/goform/WifiPowerGet.txt:4` www.baidu.com 属联网自检 URL，非云/厂商外联；建议剔除或降级，避免污染 EGRESS 统计（本格另有有效条目，不影响 found 成立）。
3. **A2 EGRESS 证据上下文缺失**：`web/cgi-bin/home.asp:619` 的 www.dlink.com 无法从仓库内 raw 判断是外联调用还是页面超链接/版权链（该固件 EGRESS 静态证据本应来自二进制/证书/API 域名，此处偏弱）。这正是该格判 unsure 的原因。
4. **radio_pass 可能非字面口令**：C2/C3/C4 的 `etc/init.d/wlan-manager:6` radio_pass（长度 7）可能是脚本变量名或配置引用而非固定字面值，仓库无 rootfs 无法复核；按 E3（c=0.5）保留 found 可以，但材料中不应表述为“已确认硬编码口令”。
5. **UNAUTH_MGMT_ENDPOINT 证据只是接口字符串**：A1 24 条、Tenda 组 16–21 条、C 侧 /cgi-bin/luci 均为路径字符串，**鉴权状态未验证**。按项目口径 found≠已验证可利用，但报告/答辩措辞需注明“接口存在、未授权访问未实测”。
6. **A2 运行时 raw 只有响应报文**：无请求头与命令记录，“未认证”依赖 `dcs_result.txt` 的探测汇总与 401 缺失推断；已复核该汇总与响应长度/XML 内容自洽，但若要求严格复现，建议补存完整请求-响应抓包。
7. **A2 管理面明文不等于外联明文**：`443 Connection refused` + Basic 明文管理页属实，但 `EGRESS_PLAINTEXT_CHANNEL` 定义为“外联通道”，且该项 source 为影子设备抓包，A2 无外联抓包，故维持 not_tested 正确；管理面明文若需计分应另立检查项。
8. **第三方静态域名分类口径**：oray/yunos/xunlei 等第三方域名现挂在 EGRESS_FIXED_CLOUD_ENDPOINT（静态检索口径）；按 baseline，EGRESS_UNREGISTERED_THIRD_PARTY 的 source 是抓包对照厂商域名清单，故未改判，但两类的归属口径建议在标注指南中统一，否则 B 侧易产生系统性分歧。

---

## 6. 限制与声明

- 除 A2 的 `materials/firmae/dcs_*.txt` 外，其余 evidence 的 raw_ref 指向固件解包 rootfs，仓库内无 `data/` 与 rootfs，**无法逐行复核**；本核验基于 evidence 的 detail 与 raw_ref 路径语义做判断，若原始 rootfs 可获取，建议对偏差表 #7 与疑点 3/4 做终裁。
- 本核验为独立第二轮语义复核，结论可与 Lead 结果交叉比对；两方若对 #7（A2 EGRESS）或 #1–#6 有分歧，应以“是否存在语义上满足定义的证据”这一标准裁决，而非以“是否存在同 check_code 条目”裁决。
- 未修改 `annotator_A.json`、任何 evidence / 配置 / 源码文件。