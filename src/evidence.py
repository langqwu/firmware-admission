"""固件 rootfs 静态取证：默认口令、未授权接口、出向外联。

三条硬规则：
1. 本模块只产出 E3（静态）证据；E1/E2 必须由影子设备实测注入，禁止在这里冒充。
2. 每条证据都带 raw_ref：文本为 ``相对路径:行号``，二进制为 ``相对路径@0x偏移``。
3. 命中只是候选，detail 里写 TODO(measure)，把“是否可利用”留给实测。

置信度是静态初判（provisional），不是实测命中率：
0.6 = 账号与口令相同的字面量；0.5 = 口令字段/口令哈希；
0.4 = 硬编码 URL；0.3 = 账号存在/接口候选。
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
import sys
import urllib.parse
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from src.schema import Evidence, EvidenceLevel

__all__ = ["collect_evidence", "main"]

_MAX_TEXT_BYTES = 2_000_000
_MAX_BINARY_BYTES = 8_000_000
_MAX_SECRETS = 20
_MAX_ENDPOINTS = 30
_MAX_EGRESS = 30

_TEXT_SUFFIXES = frozenset(
    {
        ".asp",
        ".cfg",
        ".cgi",
        ".conf",
        ".default",
        ".htm",
        ".html",
        ".ini",
        ".js",
        ".json",
        ".lua",
        ".md",
        ".php",
        ".properties",
        ".sh",
        ".txt",
        ".xml",
    }
)
_BINARY_SUFFIXES = frozenset(
    {
        ".bin",
        ".gif",
        ".gz",
        ".ico",
        ".img",
        ".jpeg",
        ".jpg",
        ".ko",
        ".png",
        ".so",
        ".ttf",
        ".woff",
        ".xz",
    }
)
_CONFIG_TOPS = frozenset({"cfg", "etc", "etc_ro", "htdocs", "web", "webroot", "webroot_ro", "www"})
_CREDENTIAL_SUFFIXES = frozenset({"", ".cfg", ".conf", ".default", ".ini", ".properties", ".sh", ".txt"})
_DEFAULT_ACCOUNTS = frozenset({"admin", "default", "guest", "root", "support", "user"})
_NO_LOGIN_SHELLS = frozenset(
    {"", "/bin/false", "/bin/sync", "/sbin/nologin", "/usr/bin/false", "/usr/sbin/nologin"}
)
_EGRESS_BINARY_KEYWORDS = (
    "acs",
    "agent",
    "boa",
    "cloud",
    "cwmp",
    "ddns",
    "httpd",
    "lighttpd",
    "nginx",
    "tr069",
    "update",
)
_LIBRARY_PARTS = frozenset({"jquery", "jqueryui", "libs", "scripts"})
_LIBRARY_NAMES = frozenset({"json.js", "json2.js", "jquery.js", "jquery.min.js"})

_ENDPOINT_RE = re.compile(
    r"(?i)/(?:goform|cgi-bin|hnap|boafrm|setup\.cgi|apply\.cgi)/[A-Za-z0-9_.-]{2,}"
)
_ENDPOINT_BYTES_RE = re.compile(
    rb"(?i)/(?:goform|cgi-bin|hnap|boafrm|setup\.cgi|apply\.cgi)/[A-Za-z0-9_.-]{2,}"
)
_URL_RE = re.compile(r"(?i)https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]{3,200}")
_URL_BYTES_RE = re.compile(rb"(?i)https?://[\x21-\x7e]{3,200}")
_SECRET_RE = re.compile(
    r"(?i)\b(?P<key>[A-Za-z0-9_.-]*(?:pass(?:word|wd)?|pwd|secret|passphrase))\b"
    r"\s*[:=]\s*[\"']?(?P<value>[^\s\"'<>;]{1,64})"
)
_WEAK_PAIR_RE = re.compile(r"(?i)\b(root|admin|support|guest)\s*[:=]\s*\1\b")

# 只排除标准组织/许可证/前端库的 URL，避免把文档链接当外联；
# 厂商与第三方业务域名一律保留，归属留待实测核实。
_SKIP_HOSTS = frozenset(
    {
        "0.0.0.0",
        "127.0.0.1",
        "apache.org",
        "brandon.aaron.sh",
        "busybox.net",
        "code.google.com",
        "detectmobilebrowser.com",
        "dillerdesign.com",
        "example.com",
        "gnu.org",
        "gsgd.co.uk",
        "ietf.org",
        "iptc.org",
        "iana.org",
        "javascript.crockford.com",
        "johnculviner.com",
        "jquery.com",
        "jquery.org",
        "jqueryui.com",
        "json.org",
        "kernel.org",
        "lanana.org",
        "linuxbase.org",
        "freebsd.org",
        "localhost",
        "macromedia.com",
        "ns.adobe.com",
        "opensource.org",
        "pajhome.org.uk",
        "purl.org",
        "python.org",
        "reasyui.com",
        "redis.io",
        "schemas.xmlsoap.org",
        "sizzlejs.com",
        "steamdev.com",
        "w3.org",
        "www.apache.org",
        "www.busybox.net",
        "www.detectmobilebrowser.com",
        "www.dns-sd.org",
        "www.gnu.org",
        "www.highcharts.com",
        "www.ietf.org",
        "www.java.com",
        "www.johnculviner.com",
        "www.jquery.com",
        "www.jqueryui.com",
        "www.json.org",
        "www.kernel.org",
        "www.macromedia.com",
        "www.opensource.org",
        "www.python.org",
        "www.realtek.com",
        "www.rfc-editor.org",
        "www.w3.org",
        "yuiblog.com",
        "zlib.net",
        "antirez.com",
        "code.highcharts.com",
        "highcharts.com",
    }
)
_SKIP_HOST_SUFFIXES = (
    ".adobe.com",
    ".apache.org",
    ".busybox.net",
    ".broadband-forum.org",
    ".freebsd.org",
    ".gnu.org",
    ".iana.org",
    ".jquery.com",
    ".jquery.org",
    ".kernel.org",
    ".lanana.org",
    ".linuxbase.org",
    ".opensource.org",
    ".python.org",
    ".sizzlejs.com",
    ".w3.org",
    ".zlib.net",
)


@dataclass(frozen=True)
class _Finding:
    """取证中间结果；collect_evidence 再补 firmware_id 与连续 id。"""

    check_code: str
    confidence: float
    raw_ref: str
    detail: str


def _iter_files(root: Path):
    """确定性遍历普通文件：跳过符号链接，避免跟随到宿主机。"""
    for dirpath, dirnames, filenames in os.walk(root):
        base = Path(dirpath)
        dirnames[:] = sorted(
            name for name in dirnames if not (base / name).is_symlink()
        )
        for name in sorted(filenames):
            path = base / name
            if path.is_symlink():
                continue
            try:
                if path.is_file():
                    yield path
            except OSError:
                continue


def _read_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > _MAX_TEXT_BYTES:
            return None
        data = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in data[:8192]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1", "replace")


def _read_binary(path: Path) -> bytes | None:
    try:
        if path.stat().st_size > _MAX_BINARY_BYTES:
            return None
        return path.read_bytes()
    except OSError:
        return None


def _is_config_text(rel: Path) -> bool:
    parts = rel.parts
    if not parts or parts[0].lower() not in _CONFIG_TOPS:
        return False
    if any(part.lower() == "libs" for part in parts):
        return False
    suffix = rel.suffix.lower()
    if suffix in _BINARY_SUFFIXES:
        return False
    return not suffix or suffix in _TEXT_SUFFIXES


def _is_exec_candidate(rel: Path) -> bool:
    parts = rel.parts
    if not parts:
        return False
    if parts[0] in {"bin", "sbin"}:
        return True
    if len(parts) >= 2 and parts[0] == "usr" and parts[1] in {"bin", "sbin"}:
        return True
    return "cgi-bin" in parts


def _is_web_path(rel: Path) -> bool:
    return any(part.lower() in {"htdocs", "web", "webroot", "webroot_ro", "www"} for part in rel.parts)


def _is_credential_config(rel: Path) -> bool:
    """口令字面量只查配置文件，跳过 i18n/前端脚本，避免把界面文案当口令。"""
    if not _is_config_text(rel):
        return False
    if any(part.lower() in {"i18n", "lang", "locale", "locales"} for part in rel.parts):
        return False
    return rel.suffix.lower() in _CREDENTIAL_SUFFIXES


def _is_egress_binary(rel: Path) -> bool:
    """外联扫描只覆盖网络/云/更新类二进制，避免把第三方库的文档链接当设备外联。"""
    name = rel.name.lower()
    return any(keyword in name for keyword in _EGRESS_BINARY_KEYWORDS)


def _is_library_path(rel: Path) -> bool:
    """前端库/脚本目录里的 URL 是许可证或文档，不是设备外联。"""
    if any(part.lower() in _LIBRARY_PARTS for part in rel.parts):
        return True
    return rel.name.lower() in _LIBRARY_NAMES


def _is_egress_text(rel: Path) -> bool:
    """外联证据优先看配置/页面；JS 里的库文档链接噪声太大，单独排除。"""
    if not _is_config_text(rel) or _is_library_path(rel):
        return False
    return rel.suffix.lower() != ".js"


def _credential_check_code(key: str, rel: Path) -> str:
    key_l = key.lower()
    if any(token in key_l for token in ("ftp", "samba", "smb", "telnet", "ssh", "pptp", "l2tp", "ddns")):
        return "CRED_DEFAULT_SERVICE_LOGIN"
    if _is_web_path(rel) and any(
        token in key_l for token in ("admin", "baseuserpass", "http", "userpass", "web")
    ):
        return "CRED_DEFAULT_ADMIN_WEB"
    if key_l.endswith("password") or key_l.endswith("passwd"):
        return "CRED_DEFAULT_ADMIN_WEB" if _is_web_path(rel) else "CRED_HARDCODED_SECRET"
    return "CRED_HARDCODED_SECRET"


def _weak_pair_check_code(user: str, rel: Path) -> str:
    if _is_web_path(rel) and user == "admin":
        return "CRED_DEFAULT_ADMIN_WEB"
    if user in {"guest", "root", "support"}:
        return "CRED_DEFAULT_SERVICE_LOGIN"
    return "CRED_HARDCODED_SECRET"


def _is_rule_database(text: str) -> bool:
    """URL 过滤/DPI 规则库不是设备自身外联，整文件跳过。"""
    return text.count("ftg;") >= 20 or text.count("http_user_agent:") >= 20


def _is_login_account(name: str, uid: str, shell: str) -> bool:
    if shell.strip().lower() in _NO_LOGIN_SHELLS:
        return False
    return name in _DEFAULT_ACCOUNTS or uid == "0"


def _hash_algorithm(hashed: str) -> str | None:
    if hashed.startswith("$1$"):
        return "MD5-crypt"
    if hashed.startswith("$5$"):
        return "SHA-256-crypt"
    if hashed.startswith("$6$"):
        return "SHA-512-crypt"
    if hashed.startswith("$2"):
        return "bcrypt"
    if len(hashed) == 13:
        return "DES-crypt"
    return None


def _looks_like_placeholder(value: str) -> bool:
    value = value.strip().strip("\"'")
    if not value:
        return True
    if value.startswith(("`", "$(", "userconfig")):
        return True
    if value.lower() in {
        "change_me",
        "changeme",
        "false",
        "nil",
        "none",
        "null",
        "password",
        "passwd",
        "todo",
        "true",
        "x",
        "xx",
        "***",
    }:
        return True
    return any(ch in value for ch in "$%{}<>")


def _looks_like_status_token(value: str) -> bool:
    """排除 RADIO_PASS="radio:P;" 这类工厂测试/状态标记。"""
    value = value.strip().strip("\"'")
    if value.lower() in {"ok", "pass", "fail", "on", "off", "yes", "no"}:
        return True
    return re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*:[A-Za-z];?", value) is not None


def _is_help_link(rel: Path, line: str) -> bool:
    """HTML 帮助页里的 <a href=...> 是文档链接，不是设备外联端点。"""
    if rel.suffix.lower() not in {".asp", ".htm", ".html"}:
        return False
    return re.search(r"(?i)<a\b[^>]*\bhref\s*=", line) is not None


def _endpoint_clean(raw: str) -> str:
    return raw.rstrip("/.,;:)]}\"'")


def _clean_url(url: str) -> str:
    return url.rstrip(".,;:)]}\"'<>")


def _url_host(url: str) -> str | None:
    try:
        host = (urllib.parse.urlsplit(url).hostname or "").strip().lower().rstrip(".")
    except ValueError:
        return None
    if not host or "%" in host or "." not in host:
        return None
    if host in _SKIP_HOSTS or any(host.endswith(suffix) for suffix in _SKIP_HOST_SUFFIXES):
        return None
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return host
    if address.is_private or address.is_loopback or address.is_link_local or address.is_unspecified:
        return None
    return host


def _dedupe(findings: list[_Finding]) -> list[_Finding]:
    seen: set[tuple[str, str, str]] = set()
    unique: list[_Finding] = []
    for finding in findings:
        key = (finding.check_code, finding.raw_ref, finding.detail)
        if key in seen:
            continue
        seen.add(key)
        unique.append(finding)
    return unique


def _scan_accounts(root: Path) -> list[_Finding]:
    findings: list[_Finding] = []
    for path in _iter_files(root):
        if path.name != "passwd":
            continue
        rel = path.relative_to(root)
        text = _read_text(path)
        if text is None or _is_rule_database(text):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            fields = line.split(":")
            if len(fields) < 7:
                continue
            name, _, uid, _, _, _, shell = fields[:7]
            if not _is_login_account(name, uid, shell):
                continue
            findings.append(
                _Finding(
                    "CRED_DEFAULT_SERVICE_LOGIN",
                    0.3,
                    f"{rel.as_posix()}:{lineno}",
                    f"静态发现可登录账号 {name}（uid={uid}, shell={shell}）；"
                    "是否为默认口令待影子设备实测 TODO(measure)",
                )
            )
    return _dedupe(findings)


def _scan_shadow_hashes(root: Path) -> list[_Finding]:
    findings: list[_Finding] = []
    for path in _iter_files(root):
        if path.name != "shadow":
            continue
        rel = path.relative_to(root)
        text = _read_text(path)
        if text is None:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            fields = line.split(":")
            if len(fields) < 2:
                continue
            name, hashed = fields[0], fields[1]
            if name not in _DEFAULT_ACCOUNTS or hashed in {"", "!", "!!", "*", "x"}:
                continue
            algorithm = _hash_algorithm(hashed)
            if algorithm is None:
                continue
            findings.append(
                _Finding(
                    "CRED_HARDCODED_SECRET",
                    0.4,
                    f"{rel.as_posix()}:{lineno}",
                    f"静态发现 {name} 口令哈希（算法 {algorithm}）；"
                    "弱口令/默认口令待实测 TODO(measure)",
                )
            )
    return _dedupe(findings)


def _scan_literal_secrets(root: Path) -> list[_Finding]:
    findings: list[_Finding] = []
    seen_keys: set[tuple[str, str]] = set()
    for path in _iter_files(root):
        rel = path.relative_to(root)
        if not _is_credential_config(rel) or path.name in {"passwd", "shadow"}:
            continue
        text = _read_text(path)
        if text is None or _is_rule_database(text):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if len(line) > 1000:
                continue
            weak_pair = _WEAK_PAIR_RE.search(line)
            if weak_pair is not None:
                user = weak_pair.group(1).lower()
                check_code = _weak_pair_check_code(user, rel)
                dedupe_key = (check_code, f"weak:{user}")
                if dedupe_key in seen_keys:
                    continue
                seen_keys.add(dedupe_key)
                findings.append(
                    _Finding(
                        check_code,
                        0.6,
                        f"{rel.as_posix()}:{lineno}",
                        f"静态发现账号与口令相同的字面量（{user}:{user}）；"
                        "是否生效待影子设备实测 TODO(measure)",
                    )
                )
                continue
            match = _SECRET_RE.search(line)
            if match is None:
                continue
            value = match.group("value")
            if _looks_like_placeholder(value) or _looks_like_status_token(value):
                continue
            key = match.group("key").lower()
            check_code = _credential_check_code(key, rel)
            dedupe_key = (check_code, key)
            if dedupe_key in seen_keys:
                continue
            seen_keys.add(dedupe_key)
            findings.append(
                _Finding(
                    check_code,
                    0.5,
                    f"{rel.as_posix()}:{lineno}",
                    f"静态发现口令字段 {key}（值已脱敏，长度 {len(value)}）；"
                    "是否默认/可用待实测 TODO(measure)",
                )
            )
    return _dedupe(findings)[:_MAX_SECRETS]


def _collect_default_credentials(rootfs: str | Path) -> list[_Finding]:
    """默认口令类静态取证：可登录账号、口令哈希、口令字面量。"""
    root = Path(rootfs)
    return _dedupe(
        _scan_accounts(root) + _scan_shadow_hashes(root) + _scan_literal_secrets(root)
    )


def _scan_text_endpoints(root: Path, seen: set[str]) -> list[_Finding]:
    findings: list[_Finding] = []
    for path in _iter_files(root):
        rel = path.relative_to(root)
        if not _is_config_text(rel):
            continue
        text = _read_text(path)
        if text is None or _is_rule_database(text):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for match in _ENDPOINT_RE.finditer(line):
                endpoint = _endpoint_clean(match.group())
                if not endpoint or endpoint in seen:
                    continue
                seen.add(endpoint)
                findings.append(
                    _Finding(
                        "UNAUTH_MGMT_ENDPOINT",
                        0.3,
                        f"{rel.as_posix()}:{lineno}",
                        f"静态发现接口 {endpoint}；鉴权状态未验证，需影子设备实测 TODO(measure)",
                    )
                )
                if len(findings) >= _MAX_ENDPOINTS:
                    return findings
    return findings


def _scan_binary_endpoints(root: Path, seen: set[str], limit: int) -> list[_Finding]:
    findings: list[_Finding] = []
    for path in _iter_files(root):
        rel = path.relative_to(root)
        if not _is_exec_candidate(rel):
            continue
        data = _read_binary(path)
        if data is None or data[:4] != b"\x7fELF":
            continue
        for match in _ENDPOINT_BYTES_RE.finditer(data):
            endpoint = _endpoint_clean(match.group().decode("ascii", "replace"))
            if not endpoint or endpoint in seen:
                continue
            seen.add(endpoint)
            findings.append(
                _Finding(
                    "UNAUTH_MGMT_ENDPOINT",
                    0.3,
                    f"{rel.as_posix()}@0x{match.start():x}",
                    f"静态发现接口 {endpoint}；鉴权状态未验证，需影子设备实测 TODO(measure)",
                )
            )
            if len(findings) >= limit:
                return findings
    return findings


def _collect_unauthorized_interfaces(rootfs: str | Path) -> list[_Finding]:
    """未授权接口类静态取证：只报接口路径候选，鉴权结论留给实测。"""
    root = Path(rootfs)
    seen: set[str] = set()
    findings = _scan_text_endpoints(root, seen)
    if len(findings) < _MAX_ENDPOINTS:
        findings += _scan_binary_endpoints(root, seen, _MAX_ENDPOINTS - len(findings))
    return _dedupe(findings)


def _scan_text_egress(root: Path, seen_hosts: set[str]) -> list[_Finding]:
    findings: list[_Finding] = []
    for path in _iter_files(root):
        rel = path.relative_to(root)
        if not _is_egress_text(rel):
            continue
        text = _read_text(path)
        if text is None or _is_rule_database(text):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if _is_help_link(rel, line):
                continue
            for match in _URL_RE.finditer(line):
                url = _clean_url(match.group())
                host = _url_host(url)
                if host is None or host in seen_hosts:
                    continue
                seen_hosts.add(host)
                scheme = url.split(":", 1)[0].lower()
                findings.append(
                    _Finding(
                        "EGRESS_FIXED_CLOUD_ENDPOINT",
                        0.4,
                        f"{rel.as_posix()}:{lineno}",
                        f"静态发现硬编码 {scheme} 外联地址 host={host}；"
                        "域名归属与外联行为未验证 TODO(measure)",
                    )
                )
                if len(findings) >= _MAX_EGRESS:
                    return findings
    return findings


def _scan_binary_egress(root: Path, seen_hosts: set[str], limit: int) -> list[_Finding]:
    findings: list[_Finding] = []
    for path in _iter_files(root):
        rel = path.relative_to(root)
        if not _is_exec_candidate(rel) or not _is_egress_binary(rel):
            continue
        data = _read_binary(path)
        if data is None or data[:4] != b"\x7fELF":
            continue
        for match in _URL_BYTES_RE.finditer(data):
            url = _clean_url(match.group().decode("ascii", "replace"))
            host = _url_host(url)
            if host is None or host in seen_hosts:
                continue
            seen_hosts.add(host)
            scheme = url.split(":", 1)[0].lower()
            findings.append(
                _Finding(
                    "EGRESS_FIXED_CLOUD_ENDPOINT",
                    0.3,
                    f"{rel.as_posix()}@0x{match.start():x}",
                    f"静态发现二进制内 {scheme} 外联地址 host={host}；"
                    "域名归属与外联行为未验证 TODO(measure)",
                )
            )
            if len(findings) >= limit:
                return findings
    return findings


def _collect_egress(rootfs: str | Path) -> list[_Finding]:
    """出向外联类静态取证：只报硬编码地址，实际连通性留给实测。"""
    root = Path(rootfs)
    seen_hosts: set[str] = set()
    findings = _scan_text_egress(root, seen_hosts)
    if len(findings) < _MAX_EGRESS:
        findings += _scan_binary_egress(root, seen_hosts, _MAX_EGRESS - len(findings))
    return _dedupe(findings)


def collect_evidence(rootfs: str | Path, firmware_id: str) -> list[Evidence]:
    """扫描 rootfs 并返回带连续 id 的 Evidence 列表（全部为 E3）。"""
    if not firmware_id or not firmware_id.strip():
        raise ValueError("firmware_id 不能为空")
    root = Path(rootfs)
    if not root.exists():
        raise FileNotFoundError(f"rootfs 不存在: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"rootfs 不是目录: {root}")
    root = root.resolve()

    findings = [
        *_collect_default_credentials(root),
        *_collect_unauthorized_interfaces(root),
        *_collect_egress(root),
    ]
    findings = _dedupe(findings)
    findings.sort(key=lambda item: (item.check_code, item.raw_ref, item.detail))
    return [
        Evidence(
            id=f"E-{firmware_id}-{index:04d}",
            firmware_id=firmware_id,
            check_code=finding.check_code,
            level=EvidenceLevel.E3,
            confidence=finding.confidence,
            raw_ref=finding.raw_ref,
            detail=finding.detail,
        )
        for index, finding in enumerate(findings, 1)
    ]


def main(argv: list[str] | None = None) -> int:
    """CLI：输出取证 JSON；0 成功，2 用法/rootfs 错误。"""
    parser = argparse.ArgumentParser(description="rootfs 三类静态取证（E3）")
    parser.add_argument("rootfs", help="解包后的文件系统根目录")
    parser.add_argument("--firmware-id", default=None, help="固件标识，默认取目录名")
    parser.add_argument("--output", default=None, help="JSON 输出路径；省略则打到 stdout")
    args = parser.parse_args(argv)

    firmware_id = args.firmware_id or Path(args.rootfs).name
    try:
        evidence = collect_evidence(args.rootfs, firmware_id)
    except (OSError, ValueError) as exc:
        print(f"取证失败: {exc}", file=sys.stderr)
        return 2

    counts = Counter(item.check_code.split("_", 1)[0] for item in evidence)
    payload = {
        "firmware_id": firmware_id,
        "rootfs": str(Path(args.rootfs)),
        "counts": {key: counts.get(key, 0) for key in ("CRED", "UNAUTH", "EGRESS")},
        "evidence": [asdict(item) for item in evidence],
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
