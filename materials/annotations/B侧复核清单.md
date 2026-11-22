# B 侧复核清单（苏同学）

> 生成：2026-11-22｜生成方式：`materials/annotations/fill_B_from_evidence.py`（可重跑）
> 状态：**`annotator_B.json` 仍是 108 格 TODO**。本文件是机器初标 + 复核清单，不是 B 的标注结果。

## 0. 为什么 B 还要你自己过一遍

`materials/双人标注操作指南.md` 第 57 行写得很清楚：

> 不能冒充第二个独立标注员；否则 kappa 是假的，评审一问就穿。

同一份指南规定 B 要"从空白 TODO 开始独立标注"。所以 108 格我按证据算好、把每一格的
支撑条目摊开给你，但**最后那一遍必须是你自己看的**——这跟王同学的做法一致：A 侧也是
"机器初标 + 逐条核验留痕"，只是他那 108 格核完是 0 处修改。

如果你认可这份初标，落地只要一条命令（见 §6），修改处同样要在 `annotator_B.json`
的 `_note` 里留痕。

## 1. 判定口径（与指南一致，只是把"证据"收紧了）

| 情形 | 标签 |
|---|---|
| 有**有效**证据条目支撑该检查项 | `found` |
| 有逐项运行时反证（如抓包 10 分钟无明文外联） | `clear` |
| 无证据，或证据本身支撑不了该检查项 | `not_tested` |

两条补充：

1. **无效证据不算 found**。标准/文档地址（iana / lanana / linuxbase / freebsd /
   broadband-forum）和厂商帮助页里的超链接，不是设备外联端点，判无效（见 §4）。
2. **不给 clear**。当前只有 A2 有运行时取证，三条全是阳性（空口令 200、未认证 HNAP 200、
   信息泄露），没有一条能证明"不存在"。其余 11 台没有逐项运行时测试，所以 `not_tested`
   就是最诚实的值——不要用 `clear` 冒充"没测到"。

结果：**found 40 / not_tested 68 / clear 0**（A 侧是 47 / 61 / 0，差的 7 格全在 §3）。

## 2. 20 分钟怎么过

```bash
# 0) 环境（干净 clone 下 92 passed 即可开始）
python -m pytest -q

# 1) 重跑初标，确认和本文件一致
python materials/annotations/fill_B_from_evidence.py

# 2) 逐格看依据：cells.<固件>.<检查项>.found_on / rejected
#    只读这一个文件就够，不用翻 evidence 原件
code materials/annotations/annotator_B_draft_核验明细.json

# 3) 重点看 §3 的 7 格，逐格决定 found 还是 not_tested
# 4) 认可后落地（§6），再跑校验
```

## 3. 7 格争议（唯一需要你拍板的）

这 7 格 A 判 found、草稿判 not_tested，原因是**该格全部证据都是误报**：一旦按"证据存在
即 found"字面执行，等于把 `www.iana.org` 这种协议文件注释当成设备外联端点。

| 固件 | 检查项 | A | 草稿 | 该格全部证据 | 建议 |
|---|---|---|---|---|---|
| A2 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | `E-A2-0002` web/cgi-bin/home.asp:619 → www.dlink.com，帮助页超链接 | 判 not_tested（DCS-960L 真实外联应看 TR-069/HNAP，不是官网链接） |
| C1 | EGRESS_FIXED_CLOUD_ENDPOINT | found | not_tested | `E-C1t-0002` etc/protocols:3 → www.iana.org | not_tested |
| C2 | 同上 | found | not_tested | `E-C2t-0003` etc/protocols:3 → www.iana.org | not_tested |
| C3 | 同上 | found | not_tested | `E-C3t-0003` etc/protocols:3 → www.iana.org | not_tested |
| C4 | 同上 | found | not_tested | `E-C4t-0003` etc/protocols:3 → www.iana.org | not_tested |
| C5 | 同上 | found | not_tested | `E-C5-0002` etc/protocols:3 → www.iana.org | not_tested |
| R3 | 同上 | found | not_tested | `E-R3-0001..0005`：iana / lanana / linuxbase / freebsd / TR-069 数据模型命名空间 | not_tested |

> 如果你认为"证据条目存在即 found"（指南字面口径），这 7 格改回 found 即可，
> 但那样 A/B 会 108/108 全一致、kappa=1.0，等于没做双标——这个结果本身就是证据规则要修的证明。

## 4. 判无效的 11 条证据（原因）

| 证据 ID | raw_ref | 判无效原因 |
|---|---|---|
| E-A2-0002 | web/cgi-bin/home.asp:619 | 帮助页超链接，不是设备主动外联 |
| E-C1t-0002 / E-C2t-0003 / E-C3t-0003 / E-C4t-0003 / E-C5-0002 | etc/protocols:3 | IANA 协议号表里的规范注释地址 |
| E-R3-0001 | etc/ethertypes:7 | IANA 规范注释地址 |
| E-R3-0002 | etc/init.d/p910nd:113 | LANANA 规范注释地址 |
| E-R3-0003 | etc/init.d/p910nd:28 | LinuxBase 规范注释地址 |
| E-R3-0004 | etc/services:8 | FreeBSD 规范注释地址 |
| E-R3-0005 | sbin/tr069@0x65c40 | TR-069 数据模型命名空间，不是 ACS 地址 |

## 5. 顺带发现的两个数据缺陷（建议转给队员 A）

1. **C1–C4 证据文件的 `firmware_id` 写成 `C1t`/`C2t`/`C3t`/`C4t`**（C5 正常）。
   任何按 `firmware_id` 关联标注的脚本都会**静默丢掉这 4 台**——我第一次跑就掉了 4 台 36 格。
   草稿里做了读取归一（`NORMALIZE`），证据文件本身没改（属 A 侧取证材料）。
2. **`src/evidence.py` 的出向外联规则没有过滤标准地址**，见 §4 的 11 条。
   建议加一个 host 白/黑名单（`iana.org` / `lanana.org` / `linuxbase.org` / `freebsd.org` /
   `*.broadband-forum.org` 直接跳过），并对 `web/**.html|asp` 里的 `<a href>` 做排除。
   修完要重跑 evidence，A/B 双方都要重标，**不宜在 B 交付前动**。

## 6. 认可后怎么落地

```bash
# 1) 草稿 → B（先看一眼 _note 再执行）
python - <<'PY'
import json, pathlib
src = json.load(open("materials/annotations/annotator_B_draft.json", encoding="utf-8"))
src["_note"] = "B = 苏同学。按 fill_B_from_evidence.py 初标逐格核验后确认，7 格 EGRESS 维持 not_tested。"
pathlib.Path("materials/annotations/annotator_B.json").write_text(
    json.dumps(src, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY

# 2) 校验 + 合并 + 指标
python materials/annotations/check_annotations.py materials/annotations/annotator_A.json materials/annotations/annotator_B.json
python materials/annotations/merge_annotations.py materials/annotations/annotator_A.json materials/annotations/annotator_B.json materials/annotations/annotation_combined.json
python -m src.metrics materials/annotations/annotation_combined.json --output materials/metrics_12.json
```

## 7. 预演指标（**不要直接写进指标表**）

用 A + 草稿 B 跑出来的数，仅供你判断量级：

| 指标 | 值 | 口径 |
|---|---|---|
| N | 108 | 12 固件 × 9 检查项 |
| agreement | 0.9352 | 101/108 一致 |
| kappa | 0.8659 | 扣除随机一致 |
| coverage | 0.4352 | 47/108（A 侧为主标注） |

为什么不能直接写进 `materials/指标表.md`：这份 B 和 A 的机器初标**同源**（都从同一批
evidence 文件推导），0.8659 度量的是"同口径可复现性"，不是"两个独立人的一致性"。
你核验过、并改过自己不同意的地方之后，这个数字才有双人标注的含义；在那之前它只能算
预演值（`materials/metrics_B_draft.json`）。
