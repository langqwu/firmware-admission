"""src.evidence 的三类静态取证、脱敏与失败路径测试。"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from src.evidence import collect_evidence, main
from src.schema import EvidenceLevel


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _build_rootfs(root: Path) -> None:
    _write(root / "etc/passwd", "root:x:0:0:root:/root:/bin/sh\nadmin:x:0:0:Admin:/:/bin/sh\n")
    _write(root / "etc/shadow", "root:$1$abc$defghijklmnopqrstuv:19000:0:99999:7:::\n")
    _write(root / "etc/httpd.conf", "secret=abc123\n")
    _write(root / "webroot/config.cfg", 'password="admin123"\nurl="https://cloud.vendor.example/api"\n')
    _write(root / "webroot/default.cfg", "usb.ftp.pwd=admin\nsys.baseuserpass=admin\n")
    _write(root / "webroot/lang/cn/translate.json", '{"password": "密码"}\n')
    (root / "usr/sbin").mkdir(parents=True, exist_ok=True)
    binary = (
        b"\x7fELF"
        + b"\x00" * 16
        + b"GET /goform/GetStatus HTTP/1.1\x00"
        + b"https://cloud.vendor.example/ota\x00"
    )
    (root / "usr/sbin/httpd").write_bytes(binary)


def test_collect_evidence_covers_three_categories(tmp_path: Path) -> None:
    root = tmp_path / "rootfs"
    _build_rootfs(root)

    evidence = collect_evidence(root, "FW-TEST")

    codes = {item.check_code for item in evidence}
    assert "CRED_DEFAULT_SERVICE_LOGIN" in codes
    assert "CRED_HARDCODED_SECRET" in codes
    assert "CRED_DEFAULT_ADMIN_WEB" in codes
    assert "UNAUTH_MGMT_ENDPOINT" in codes
    assert "EGRESS_FIXED_CLOUD_ENDPOINT" in codes

    assert len({item.id for item in evidence}) == len(evidence)
    assert all(item.firmware_id == "FW-TEST" for item in evidence)
    assert all(item.level is EvidenceLevel.E3 for item in evidence)
    assert all(0.0 < item.confidence <= 1.0 for item in evidence)
    assert all(
        re.search(r":\d+$", item.raw_ref) or "@0x" in item.raw_ref for item in evidence
    )

    assert any(item.raw_ref == "etc/passwd:1" for item in evidence)
    assert any(item.raw_ref == "webroot/config.cfg:1" for item in evidence)
    assert any(item.raw_ref == "webroot/default.cfg:1" for item in evidence)
    assert any(
        item.check_code == "CRED_DEFAULT_SERVICE_LOGIN" and "usb.ftp.pwd" in item.detail
        for item in evidence
    )
    assert any(
        item.check_code == "CRED_DEFAULT_ADMIN_WEB" and "sys.baseuserpass" in item.detail
        for item in evidence
    )
    assert all("translate.json" not in item.raw_ref for item in evidence)
    assert any("usr/sbin/httpd@0x" in item.raw_ref for item in evidence)
    assert any("/goform/GetStatus" in item.detail for item in evidence)
    assert any("cloud.vendor.example" in item.detail for item in evidence)

    # 同一 host 只报一条；文本证据优先于二进制。
    egress = [item for item in evidence if item.check_code == "EGRESS_FIXED_CLOUD_ENDPOINT"]
    assert len(egress) == 1
    assert egress[0].raw_ref == "webroot/config.cfg:2"

    # 口令值不得进入 detail/raw_ref。
    assert all("admin123" not in item.detail for item in evidence)
    assert all("abc123" not in item.detail for item in evidence)
    assert all("admin123" not in item.raw_ref for item in evidence)


def test_collect_evidence_empty_rootfs_returns_empty(tmp_path: Path) -> None:
    root = tmp_path / "empty"
    root.mkdir()

    assert collect_evidence(root, "FW-EMPTY") == []


def test_collect_evidence_missing_rootfs_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        collect_evidence(tmp_path / "absent", "FW-ABSENT")


def test_rule_database_is_not_reported_as_egress(tmp_path: Path) -> None:
    root = tmp_path / "rootfs"
    lines = [
        f"ftg;{index};0;H;-1;80;-1;model:get;host:third-party{index}.example;"
        "http_user_agent:R:0:0:Android;"
        for index in range(30)
    ]
    _write(root / "etc/features.cfg", "\n".join(lines))

    evidence = collect_evidence(root, "FW-RULES")

    assert [item for item in evidence if item.check_code == "EGRESS_FIXED_CLOUD_ENDPOINT"] == []


def test_standard_documentation_urls_and_help_links_are_not_egress(
    tmp_path: Path,
) -> None:
    root = tmp_path / "rootfs"
    _write(
        root / "etc/protocols",
        "# http://www.iana.org/assignments/protocol-numbers\n",
    )
    _write(
        root / "etc/services",
        "# http://www.freebsd.org/cgi/cvsweb.cgi/services\n",
    )
    _write(
        root / "etc/ethertypes",
        "# http://www.iana.org/assignments/ethertypes\n",
    )
    _write(
        root / "etc/init.d/p910nd",
        "# http://www.lanana.org/docs/device-list/\n"
        "# http://www.linuxbase.org/navigator/\n",
    )
    (root / "sbin").mkdir(parents=True, exist_ok=True)
    (root / "sbin/tr069").write_bytes(
        b"\x7fELF" + b"\x00" * 16
        + b"http://www.broadband-forum.org/cwmp/tr-069.xml\x00"
    )
    _write(
        root / "web/cgi-bin/home.asp",
        '<a href="https://www.dlink.com/support">support</a>\n',
    )
    _write(
        root / "etc/rc.d/init.d/pppoe.sh",
        "PPPoEPWD=`userconfig -read NETWORK_V4 PPPoEPWD`\n",
    )
    _write(
        root / "etc/init.d/wlan-manager",
        'RADIO_PASS="radio:P;"\n',
    )
    _write(
        root / "webroot/config.cfg",
        'url="https://cloud.vendor.example/api"\nsecret=abc123\n',
    )

    evidence = collect_evidence(root, "FW-NOISE")

    egress = [item for item in evidence if item.check_code == "EGRESS_FIXED_CLOUD_ENDPOINT"]
    assert [item.detail for item in egress] == [
        "静态发现硬编码 https 外联地址 host=cloud.vendor.example；"
        "域名归属与外联行为未验证 TODO(measure)"
    ]
    creds = [item for item in evidence if item.check_code == "CRED_HARDCODED_SECRET"]
    assert any("secret" in item.detail for item in creds)
    assert not any("PPPoEPWD" in item.detail or "RADIO_PASS" in item.detail for item in creds)
    assert any(item.raw_ref == "webroot/config.cfg:1" for item in evidence)
    assert any("cloud.vendor.example" in item.detail for item in evidence)


def test_main_writes_json_and_reports_usage_errors(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "rootfs"
    _write(root / "etc/passwd", "root:x:0:0:root:/root:/bin/sh\n")
    output = tmp_path / "evidence.json"

    assert main([str(root), "--firmware-id", "FW-CLI", "--output", str(output)]) == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["firmware_id"] == "FW-CLI"
    assert payload["counts"]["CRED"] == 1
    assert payload["counts"]["UNAUTH"] == 0
    assert payload["counts"]["EGRESS"] == 0
    assert payload["evidence"][0]["level"] == "E3"
    assert payload["evidence"][0]["raw_ref"] == "etc/passwd:1"

    assert main([str(tmp_path / "absent"), "--firmware-id", "FW-CLI"]) == 2
    assert "取证失败" in capsys.readouterr().err
