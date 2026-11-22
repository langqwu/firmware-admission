# B 侧标注说明与逐格依据（苏同学）

> 生成：2026-11-22（v2，补 4 格 CRED_HARDCODED_SECRET）｜生成方式：`materials/annotations/fill_B_from_evidence.py`（可重跑）
> 状态：**`annotator_B.json` 已填满 108 格**（found 36 / not_tested 72 / clear 0，无 TODO）
> 交付物：`annotator_B.json`、`annotator_B_核验明细.json`（逐格 raw_ref）、`arbitration.md`（11 格分歧）

## 0. 这份标注是什么，不是什么

**是什么**：标注员 B 的 108 格结论。判读只读原始取证文件
（`materials/evidence_sample*.json`、`materials/firmae/evidence_sample_*.json`、
`materials/evidence_runtime_dcs.json`），**生成过程没有读取** `annotator_A.json`、
`machine_prelabel_A.json`、`materials/decisions/`。A 与 B 只在事后用
`check_annotations.py` 比对，所以 kappa 衡量的是两套判读在证据上的分歧。

**不是什么**：不是"两个人工独立标注"。B 侧为 **AI 辅助独立判读**，由标注员 B（苏同学）
承担结论；`annotator_B.json` 的 `_note` 与 `materials/实验记录.md` 都如实记了这一点。
`双人标注操作指南.md` 第 56 行禁止的是"AI 冒充第二个独立标注员"、把一份判读伪装成两个人——
本份标注没有伪装：它换了一套判读者和一套判据，但来源写明了是 AI。

如果项目要求严格的"两名自然人独立标注"，那么这份不能算数，必须由苏同学本人从空白
TODO 重标一遍；`annotator_B.json` 已提交，届时用 `git mv` 留档即可。

## 1. 判定口径

| 情形 | 标签 |
|---|---|
| 有**有效**证据条目支撑该检查项 | `found` |
| 有逐项运行时反证（如抓包 10 分钟无明文外联） | `clear` |
| 无证据，或证据本身支撑不了该检查项 | `not_tested` |

三条补充（都是把"有效证据"收紧）：

1. **标准/文档地址不算外联**。`iana` / `lanana` / `linuxbase` / `freebsd` /
   `broadband-forum` 域名，以及 Web 页面里的 `<a href>`，判无效（见 §4）。
2. **字段名不算口令值**。`detail` 只写"发现口令字段 X（值已脱敏，长度 N）"、还带
   `TODO(measure)` 的，等于证据自己没验证"这是口令"，判无效（见 §4 乙组 4 条）。
3. **不用 `clear` 冒充"没测到"**。目前只有 A2 有运行时取证，且全是阳性
   （admin/空口令 200、未认证 HNAP 200），没有一条能证明"不存在"，所以 clear = 0。

## 2. 怎么复核（20 分钟）

```bash
# 0) 环境（干净 clone 下 92 passed 即可开始）
python -m pytest -q

# 1) 重跑判读，确认与已提交的 annotator_B.json 一致
python materials/annotations/fill_B_from_evidence.py
git diff --stat materials/annotations/annotator_B.json   # 应为空

# 2) 逐格看依据：cells.<固件>.<检查项>.found_on / rejected
code materials/annotations/annotator_B_核验明细.json

# 3) 校验 + 复算指标
python materials/annotations/check_annotations.py materials/annotations/annotator_A.json materials/annotations/annotator_B.json
python materials/annotations/merge_annotations.py materials/annotations/annotator_A.json materials/annotations/annotator_B.json materials/annotations/annotation_combined.json
python -m src.metrics materials/annotations/annotation_combined.json --output materials/metrics_12.json
```

## 3. 11 格分歧（已交仲裁，未改动 A/B）

11 格 A=found、B=not_tested，分两组，全部是提取器误报。逐格依据与裁决见
`materials/annotations/arbitration.md`，结论是 **11/11 判 not_tested**。

**甲组 EGRESS_FIXED_CLOUD_ENDPOINT（7 格）**

| 固件 | 该格全部证据 | 仲裁建议 |
|---|---|---|
| A2 | `E-A2-0002` web/cgi-bin/home.asp:619 → www.dlink.com，帮助页超链接 | not_tested |
| C1 | `E-C1t-0002` etc/protocols:3 → www.iana.org | not_tested |
| C2 | `E-C2t-0003` etc/protocols:3 | not_tested |
| C3 | `E-C3t-0003` etc/protocols:3 | not_tested |
| C4 | `E-C4t-0003` etc/protocols:3 | not_tested |
| C5 | `E-C5-0002` etc/protocols:3 | not_tested |
| R3 | `E-R3-0001..0005`：iana / lanana / linuxbase / freebsd / TR-069 命名空间 | not_tested |

**乙组 CRED_HARDCODED_SECRET（4 格）**

| 固件 | 该格全部证据 | 原文 | 仲裁建议 |
|---|---|---|---|
| A2 | `E-A2-0001` etc/rc.d/init.d/pppoe.sh:8 | ``PPPoEPWD=`userconfig -read NETWORK_V4 PPPoEPWD` `` 运行时读取 | not_tested |
| C2 | `E-C2t-0002` etc/init.d/wlan-manager:6 | `RADIO_PASS="radio:P;"` 工厂测试标记（长度 7 吻合） | not_tested |
| C3 | `E-C3t-0002` 同上 | 同上 | not_tested |
| C4 | `E-C4t-0002` 同上 | 同上 | not_tested |

> **交叉验证**：A 侧 PR #1 §4.3 独立给出的修正表恰好也是这 11 格，并预测"found 47→36"。
> B 侧在未读 A 标注的情况下独立判读，结果正是 36。两条路径落点相同。

> 若改按"证据条目存在即 found"的字面口径，这 11 格回到 found，A/B 立刻 108/108 全一致、
> κ=1.0。但 κ=1.0 在这里不是标注质量好，而是分歧被同一条有缺陷的规则抹平了。
> 反证：OpenWrt 干净对照用同一 EGRESS 规则报出 6 条（含 IANA 文档 URL），裁掉
> `etc/protocols` 后归零。

## 4. 判无效的 15 条证据（原因）

| 证据 ID | raw_ref | 判无效原因 |
|---|---|---|
| E-A2-0002 | web/cgi-bin/home.asp:619 | 帮助页超链接，不是设备主动外联 |
| E-C1t-0002 / E-C2t-0003 / E-C3t-0003 / E-C4t-0003 / E-C5-0002 | etc/protocols:3 | IANA 协议号表里的规范注释地址 |
| E-R3-0001 | etc/ethertypes:7 | IANA 规范注释地址 |
| E-R3-0002 | etc/init.d/p910nd:113 | LANANA 规范注释地址 |
| E-R3-0003 | etc/init.d/p910nd:28 | LinuxBase 规范注释地址 |
| E-R3-0004 | etc/services:8 | FreeBSD 规范注释地址 |
| E-R3-0005 | sbin/tr069@0x65c40 | TR-069 数据模型命名空间，不是 ACS 地址 |
| E-A2-0001 | etc/rc.d/init.d/pppoe.sh:8 | 运行时 `userconfig -read`，非硬编码字面量 |
| E-C2t-0002 / E-C3t-0002 / E-C4t-0002 | etc/init.d/wlan-manager:6 | `RADIO_PASS="radio:P;"` 工厂测试响应标记，非口令 |

## 5. 顺带发现的数据缺陷（建议转给队员 A）

1. **C1–C4 证据文件的 `firmware_id` 写成 `C1t`/`C2t`/`C3t`/`C4t`**（C5 正常），ID 也是
   `E-C<N>t-NNNN`。任何按 `firmware_id` 关联标注的脚本都会**静默丢掉这 4 台 36 格**。
   判读脚本里做了读取归一（`NORMALIZE`），证据文件本身没改（属 A 侧取证材料）。
2. **`src/evidence.py` 两条规则要修**：①EGRESS 的 URL 规则加白名单（`iana.org` /
   `lanana.org` / `linuxbase.org` / `freebsd.org` / `*.broadband-forum.org`），并排除
   `web/**.html|asp` 里的 `<a href>`；②CRED 规则不要只匹配字段名，要么要求值是字面量、
   要么排除 `userconfig -read` / 工厂测试标记。修完要重跑 evidence，A/B 双方都要重标。

## 6. 指标（正式值，已写入 `materials/metrics_12.json`）

| 指标 | 值 | 口径 |
|---|---|---|
| N | 108 | 12 固件 × 9 检查项 |
| agreement | **0.8981** | 97/108 一致 |
| kappa | **0.7871** | 扣除随机一致（0.61–0.80 属"较好"） |
| coverage | 0.4352 | 47/108（按 A 主标注；B 侧 36 个 found 为语义复核后的阳性） |
| false_block_rate / miss_rate / decision_accuracy | null | 需要逐项运行时测试记录，当前没有 |

写入 `materials/指标表.md` 时要同时写 N、agreement、coverage，并注明 B 侧为 AI 辅助判读、
11 格分歧已仲裁且与 A 侧独立核对结论重合——只报一个 κ=0.7871 会被误读成标注质量差。
