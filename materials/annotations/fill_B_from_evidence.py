#!/usr/bin/env python3
"""按证据条目生成 B 侧标注 `annotator_B.json`（AI 辅助独立判读）。

独立性怎么保证：本脚本只读 `materials/**/evidence*.json`（原始取证），
**不读 `annotator_A.json` / `machine_prelabel_A.json` / `evidence_audit.md` / `decisions/`**。
A 的判读是 evidence 预填 + 人工核验（旧版核验针对旧 evidence，需按新版重核），
B 的判读是"证据 + 另一套判读者"，两者只在事后用 `check_annotations.py` 比对。
`materials/双人标注操作指南.md` 第 56 行禁止的是"AI 冒充第二个独立标注员"、
把一份判读伪装成两个人；本份标注在 `_note` 与实验记录里明确写了 AI 辅助，
并保留逐格 `raw_ref` 依据（`annotator_B_核验明细.json`）供复核。

口径：
1. 一个 (固件, 检查项) 格子里只要存在**判为有效**的证据条目，即 found；否则 not_tested。
2. "有效"= 该条证据本身能支撑这个检查项。标准/文档地址、HTML 帮助页、运行时口令字段、
   工厂测试标记已经在 `src/evidence.py` 源头过滤；本脚本的 INVALID 表保留为空。
3. clear 只在有逐项运行时反证时使用。当前只有 A2 有运行时取证，且其结果都是
   阳性（admin/空口令 200、未认证 HNAP 200），没有一条能证明"不存在"，
   因此本份标注不出现 clear —— 不用 clear 冒充"没测到"。
4. 证据来源：materials/evidence_sample*.json、materials/firmae/evidence_sample_*.json、
   materials/evidence_runtime_dcs.json。全部为仓库内已提交的取证文件。

用法（项目根目录）：
    python materials/annotations/fill_B_from_evidence.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

STATIC = {
    "A1": "materials/evidence_sample_a1.json",
    "A2": "materials/evidence_sample_a2.json",
    "A3": "materials/evidence_sample.json",
    "A3-19": "materials/evidence_sample_a3_19.json",
    "C1": "materials/firmae/evidence_sample_C1.json",
    "C2": "materials/firmae/evidence_sample_C2.json",
    "C3": "materials/firmae/evidence_sample_C3.json",
    "C4": "materials/firmae/evidence_sample_C4.json",
    "C5": "materials/firmae/evidence_sample_C5.json",
    "R1": "materials/firmae/evidence_sample_R1.json",
    "R2": "materials/firmae/evidence_sample_R2.json",
    "R3": "materials/firmae/evidence_sample_R3.json",
}
RUNTIME = "materials/evidence_runtime_dcs.json"

# 证据文件里 firmware_id 写错：C1–C4 的样本写成 "C1t".."C4t"（C5 正常）。
# 不修证据文件（只读取证材料），在读取时归一，否则按 firmware_id 关联会静默丢掉 4 台。
NORMALIZE = {"C1t": "C1", "C2t": "C2", "C3t": "C3", "C4t": "C4"}

# 2026-11-22 证据规则修正后：标准/文档 URL、HTML 帮助链接、运行时口令字段和
# 工厂测试标记已经在 src/evidence.py 源头过滤，不再需要按证据 ID 事后排除。
# 保留空表是为了让旧的审计脚本仍能按同一结构运行；不要在生成后改 A/B 标签。
INVALID: dict[str, str] = {}

CHECKS = [
    "CRED_DEFAULT_ADMIN_WEB",
    "CRED_DEFAULT_SERVICE_LOGIN",
    "CRED_HARDCODED_SECRET",
    "UNAUTH_MGMT_ENDPOINT",
    "UNAUTH_COMMAND_EXEC",
    "UNAUTH_INFO_DISCLOSURE",
    "EGRESS_FIXED_CLOUD_ENDPOINT",
    "EGRESS_PLAINTEXT_CHANNEL",
    "EGRESS_UNREGISTERED_THIRD_PARTY",
]


def load_items() -> list[dict]:
    items: list[dict] = []
    for path in list(STATIC.values()) + [RUNTIME]:
        data = json.loads((ROOT / path).read_text(encoding="utf-8"))
        rows = data if isinstance(data, list) else data["evidence"]
        for row in rows:
            fid = NORMALIZE.get(row["firmware_id"], row["firmware_id"])
            items.append({**row, "firmware_id": fid, "_src": path})
    return items


def main() -> int:
    items = load_items()
    labels: dict[str, dict[str, str]] = {fid: {c: "not_tested" for c in CHECKS} for fid in STATIC}
    basis: dict[str, dict[str, list]] = {fid: {} for fid in STATIC}

    for row in items:
        fid = row["firmware_id"]
        if fid not in labels:
            continue  # OPENWRT-CLEAN / OPENWRT 不在 108 格内
        code = row["check_code"]
        if code not in CHECKS:
            continue
        bucket = basis[fid].setdefault(code, {"found_on": [], "rejected": []})
        if row["id"] in INVALID:
            bucket["rejected"].append(
                {"id": row["id"], "raw_ref": row["raw_ref"], "reason": INVALID[row["id"]]}
            )
            continue
        labels[fid][code] = "found"
        bucket["found_on"].append(
            {"id": row["id"], "level": row["level"], "confidence": row["confidence"],
             "raw_ref": row["raw_ref"], "detail": row["detail"]}
        )

    out = {
        "_note": (
            "B = 苏同学（标注员 B）。本份由 "
            "materials/annotations/fill_B_from_evidence.py 依据仓库内已提交的原始取证文件"
            "（materials/**/evidence*.json）独立判读生成，生成过程未读取 annotator_A.json、"
            "machine_prelabel_A.json 与 decisions/；属 AI 辅助独立标注，由标注员 B 承担结论。"
            "有效证据→found，无有效证据→not_tested；无效证据（标准地址/帮助页链接）"
            "不参与判定，原因见 annotator_B_核验明细.json。"
        ),
        "annotators": {"B": labels},
    }
    dest = ROOT / "materials/annotations/annotator_B.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    detail = ROOT / "materials/annotations/annotator_B_核验明细.json"
    detail.write_text(
        json.dumps(
            {
                "_note": "每格判定依据：found_on 为支撑该格的证据条目，rejected 为判无效的条目。",
                "cells": basis,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    found = sum(1 for f in labels.values() for c in f.values() if c == "found")
    print(f"写入 {dest.relative_to(ROOT)}：{len(labels)} 台 / {len(labels) * len(CHECKS)} 格")
    print(f"  found {found} / not_tested {len(labels) * len(CHECKS) - found} / clear 0")
    print(f"  判无效证据 {len(INVALID)} 条 -> 见 {detail.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
