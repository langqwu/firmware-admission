# 机器初标证据审计（A 预填）

> 生成规则：某 check_code 在 evidence 中有至少一条记录 → `found`；否则 `not_tested`。
> 没有 `clear`：当前没有逐项 runtime test 记录，不能用“未发现”冒充“已测清”。
> A 必须逐条核对 `raw_ref`；B 不得看本文件，必须独立标注。

| 固件 | 检查项 | 状态 | E1 | E2 | E3 | 证据 ID | raw_ref |
|---|---|---|---|---|---|---|---|
| A1 | CRED_DEFAULT_ADMIN_WEB | found | 0 | 0 | 1 | E-A1-0001 | `webroot_ro/default.cfg:48` |
| A1 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 1 | E-A1-0002 | `etc_ro/passwd:1` |
| A1 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-A1-0003 | `etc_ro/shadow:1` |
| A1 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 24 | E-A1-0008<br>E-A1-0009<br>E-A1-0010<br>E-A1-0011<br>E-A1-0012<br>E-A1-0013<br>E-A1-0014<br>E-A1-0015<br>E-A1-0016<br>E-A1-0017<br>E-A1-0018<br>E-A1-0019<br>E-A1-0020<br>E-A1-0021<br>E-A1-0022<br>E-A1-0023<br>E-A1-0024<br>E-A1-0025<br>E-A1-0026<br>E-A1-0027<br>E-A1-0028<br>E-A1-0029<br>E-A1-0030<br>E-A1-0031 | `bin/httpd@0x6e27c`<br>`bin/httpd@0x75be8`<br>`bin/httpd@0x75bf4`<br>`bin/httpd@0x75c10`<br>`bin/httpd@0x75c20`<br>`bin/httpd@0x75c48`<br>`bin/httpd@0x75c58`<br>`bin/httpd@0x75c6c`<br>`bin/httpd@0x75c84`<br>`bin/httpd@0x75c9c`<br>`bin/httpd@0x75cd4`<br>`bin/httpd@0x75cf0`<br>`bin/httpd@0x75d0c`<br>`bin/httpd@0x75d28`<br>`bin/httpd@0x75d3c`<br>`bin/httpd@0x75d50`<br>`bin/httpd@0x75d98`<br>`webroot_ro/app.js:338`<br>`webroot_ro/goform/clearSyslog/index.html:2`<br>`webroot_ro/goform/test/index.html:2`<br>`webroot_ro/js/system_config.js:177`<br>`webroot_ro/js/system_status.js:31`<br>`webroot_ro/js/wrl_advance.js:138`<br>`webroot_ro/js/wrl_basic.js:896` |
| A1 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| A1 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| A1 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 4 | E-A1-0004<br>E-A1-0005<br>E-A1-0006<br>E-A1-0007 | `bin/httpd@0x751f8`<br>`bin/httpd@0x75218`<br>`bin/httpd@0x75238`<br>`webroot_ro/goform/getCloud/index.html:6` |
| A1 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| A1 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| A2 | CRED_DEFAULT_ADMIN_WEB | found | 1 | 0 | 0 | E-A2-E1-0001 | `materials/firmae/dcs_login_home_headers.txt:1` |
| A2 | CRED_DEFAULT_SERVICE_LOGIN | not_tested | 0 | 0 | 0 | — | — |
| A2 | CRED_HARDCODED_SECRET | not_tested | 0 | 0 | 0 | — | — |
| A2 | UNAUTH_MGMT_ENDPOINT | found | 0 | 1 | 2 | E-A2-E2-0001<br>E-A2-0001<br>E-A2-0002 | `materials/firmae/dcs_login_hnap.txt:1`<br>`etc/httpd.ini:2`<br>`usr/sbin/eventd@0x22690` |
| A2 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| A2 | UNAUTH_INFO_DISCLOSURE | found | 0 | 1 | 0 | E-A2-E2-0002 | `materials/firmae/dcs_login_hnap.txt:1` |
| A2 | EGRESS_FIXED_CLOUD_ENDPOINT | not_tested | 0 | 0 | 0 | — | — |
| A2 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| A2 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| A3 | CRED_DEFAULT_ADMIN_WEB | found | 0 | 0 | 1 | E-A3-0001 | `webroot_ro/default.cfg:262` |
| A3 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 8 | E-A3-0002<br>E-A3-0003<br>E-A3-0004<br>E-A3-0005<br>E-A3-0006<br>E-A3-0007<br>E-A3-0008<br>E-A3-0009 | `etc_ro/passwd:1`<br>`etc_ro/passwd:2`<br>`etc_ro/passwd:3`<br>`etc_ro/passwd:4`<br>`etc_ro/passwd:5`<br>`webroot_ro/default.cfg:315`<br>`webroot_ro/default.cfg:323`<br>`webroot_ro/default.cfg:328` |
| A3 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-A3-0010 | `etc_ro/shadow:1` |
| A3 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 21 | E-A3-0014<br>E-A3-0015<br>E-A3-0016<br>E-A3-0017<br>E-A3-0018<br>E-A3-0019<br>E-A3-0020<br>E-A3-0021<br>E-A3-0022<br>E-A3-0023<br>E-A3-0024<br>E-A3-0025<br>E-A3-0026<br>E-A3-0027<br>E-A3-0028<br>E-A3-0029<br>E-A3-0030<br>E-A3-0031<br>E-A3-0032<br>E-A3-0033<br>E-A3-0034 | `bin/httpd@0xd4220`<br>`bin/httpd@0xd4238`<br>`bin/httpd@0xd4250`<br>`bin/httpd@0xd4268`<br>`bin/httpd@0xd4b6c`<br>`bin/httpd@0xd4b88`<br>`bin/httpd@0xd4ba0`<br>`bin/httpd@0xd4bac`<br>`bin/httpd@0xd4bd0`<br>`bin/httpd@0xd4bec`<br>`bin/httpd@0xd4c00`<br>`bin/httpd@0xd4cd4`<br>`bin/httpd@0xd4cec`<br>`bin/httpd@0xd4d08`<br>`bin/httpd@0xd4d58`<br>`etc_ro/nginx/conf/nginx.conf:48`<br>`webroot_ro/directupgrade.html:27`<br>`webroot_ro/js/dlna.js:134`<br>`webroot_ro/system_backup.html:15`<br>`webroot_ro/system_password.html:15`<br>`webroot_ro/system_reboot.html:15` |
| A3 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| A3 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| A3 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 3 | E-A3-0011<br>E-A3-0012<br>E-A3-0013 | `bin/phddns@0xd3f5`<br>`webroot_ro/default.cfg:86`<br>`webroot_ro/goform/WifiPowerGet.txt:4` |
| A3 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| A3 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| A3-19 | CRED_DEFAULT_ADMIN_WEB | found | 0 | 0 | 1 | E-A3-19-0001 | `webroot_ro/default.cfg:262` |
| A3-19 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 8 | E-A3-19-0002<br>E-A3-19-0003<br>E-A3-19-0004<br>E-A3-19-0005<br>E-A3-19-0006<br>E-A3-19-0007<br>E-A3-19-0008<br>E-A3-19-0009 | `etc_ro/passwd:1`<br>`etc_ro/passwd:2`<br>`etc_ro/passwd:3`<br>`etc_ro/passwd:4`<br>`etc_ro/passwd:5`<br>`webroot_ro/default.cfg:315`<br>`webroot_ro/default.cfg:323`<br>`webroot_ro/default.cfg:328` |
| A3-19 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-A3-19-0010 | `etc_ro/shadow:1` |
| A3-19 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 16 | E-A3-19-0014<br>E-A3-19-0015<br>E-A3-19-0016<br>E-A3-19-0017<br>E-A3-19-0018<br>E-A3-19-0019<br>E-A3-19-0020<br>E-A3-19-0021<br>E-A3-19-0022<br>E-A3-19-0023<br>E-A3-19-0024<br>E-A3-19-0025<br>E-A3-19-0026<br>E-A3-19-0027<br>E-A3-19-0028<br>E-A3-19-0029 | `bin/httpd@0xd4080`<br>`bin/httpd@0xd4098`<br>`bin/httpd@0xd40b0`<br>`bin/httpd@0xd40c8`<br>`bin/httpd@0xd4a20`<br>`bin/httpd@0xd4a30`<br>`bin/httpd@0xd4a84`<br>`bin/httpd@0xd4a9c`<br>`bin/httpd@0xd4ab8`<br>`bin/httpd@0xd4b20`<br>`etc_ro/nginx/conf/nginx.conf:48`<br>`webroot_ro/directupgrade.html:27`<br>`webroot_ro/js/dlna.js:134`<br>`webroot_ro/system_backup.html:15`<br>`webroot_ro/system_password.html:15`<br>`webroot_ro/system_reboot.html:15` |
| A3-19 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| A3-19 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| A3-19 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 3 | E-A3-19-0011<br>E-A3-19-0012<br>E-A3-19-0013 | `bin/phddns@0xd3f5`<br>`webroot_ro/default.cfg:86`<br>`webroot_ro/goform/WifiPowerGet.txt:4` |
| A3-19 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| A3-19 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| R1 | CRED_DEFAULT_ADMIN_WEB | found | 0 | 0 | 1 | E-R1-0001 | `webroot_ro/default.cfg:267` |
| R1 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 8 | E-R1-0002<br>E-R1-0003<br>E-R1-0004<br>E-R1-0005<br>E-R1-0006<br>E-R1-0007<br>E-R1-0008<br>E-R1-0009 | `etc_ro/passwd:1`<br>`etc_ro/passwd:2`<br>`etc_ro/passwd:3`<br>`etc_ro/passwd:4`<br>`etc_ro/passwd:5`<br>`webroot_ro/default.cfg:320`<br>`webroot_ro/default.cfg:328`<br>`webroot_ro/default.cfg:330` |
| R1 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-R1-0010 | `etc_ro/shadow:1` |
| R1 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 21 | E-R1-0014<br>E-R1-0015<br>E-R1-0016<br>E-R1-0017<br>E-R1-0018<br>E-R1-0019<br>E-R1-0020<br>E-R1-0021<br>E-R1-0022<br>E-R1-0023<br>E-R1-0024<br>E-R1-0025<br>E-R1-0026<br>E-R1-0027<br>E-R1-0028<br>E-R1-0029<br>E-R1-0030<br>E-R1-0031<br>E-R1-0032<br>E-R1-0033<br>E-R1-0034 | `bin/httpd@0xd2578`<br>`bin/httpd@0xd2590`<br>`bin/httpd@0xd25a8`<br>`bin/httpd@0xd25c0`<br>`bin/httpd@0xd2ec4`<br>`bin/httpd@0xd2ee0`<br>`bin/httpd@0xd2ef8`<br>`bin/httpd@0xd2f04`<br>`bin/httpd@0xd2f28`<br>`bin/httpd@0xd2f44`<br>`bin/httpd@0xd2f58`<br>`bin/httpd@0xd302c`<br>`bin/httpd@0xd3044`<br>`bin/httpd@0xd3060`<br>`bin/httpd@0xd30b0`<br>`etc_ro/nginx/conf/nginx.conf:48`<br>`webroot_ro/directupgrade.html:27`<br>`webroot_ro/js/dlna.js:134`<br>`webroot_ro/system_backup.html:15`<br>`webroot_ro/system_password.html:15`<br>`webroot_ro/system_reboot.html:15` |
| R1 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| R1 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| R1 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 3 | E-R1-0011<br>E-R1-0012<br>E-R1-0013 | `bin/phddns@0xd3f5`<br>`webroot_ro/default.cfg:87`<br>`webroot_ro/goform/WifiPowerGet.txt:4` |
| R1 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| R1 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| R2 | CRED_DEFAULT_ADMIN_WEB | found | 0 | 0 | 1 | E-R2-0001 | `webroot_ro/default.cfg:264` |
| R2 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 8 | E-R2-0002<br>E-R2-0003<br>E-R2-0004<br>E-R2-0005<br>E-R2-0006<br>E-R2-0007<br>E-R2-0008<br>E-R2-0009 | `etc_ro/passwd:1`<br>`etc_ro/passwd:2`<br>`etc_ro/passwd:3`<br>`etc_ro/passwd:4`<br>`etc_ro/passwd:5`<br>`webroot_ro/default.cfg:318`<br>`webroot_ro/default.cfg:326`<br>`webroot_ro/default.cfg:331` |
| R2 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-R2-0010 | `etc_ro/shadow:1` |
| R2 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 20 | E-R2-0014<br>E-R2-0015<br>E-R2-0016<br>E-R2-0017<br>E-R2-0018<br>E-R2-0019<br>E-R2-0020<br>E-R2-0021<br>E-R2-0022<br>E-R2-0023<br>E-R2-0024<br>E-R2-0025<br>E-R2-0026<br>E-R2-0027<br>E-R2-0028<br>E-R2-0029<br>E-R2-0030<br>E-R2-0031<br>E-R2-0032<br>E-R2-0033 | `bin/httpd@0xd048c`<br>`bin/httpd@0xd04a4`<br>`bin/httpd@0xd04bc`<br>`bin/httpd@0xd04d4`<br>`bin/httpd@0xd0dd8`<br>`bin/httpd@0xd0df4`<br>`bin/httpd@0xd0e0c`<br>`bin/httpd@0xd0e18`<br>`bin/httpd@0xd0e3c`<br>`bin/httpd@0xd0e58`<br>`bin/httpd@0xd0e6c`<br>`bin/httpd@0xd0f40`<br>`bin/httpd@0xd0f58`<br>`bin/httpd@0xd0f74`<br>`bin/httpd@0xd0fc4`<br>`webroot_ro/directupgrade.html:27`<br>`webroot_ro/js/dlna.js:134`<br>`webroot_ro/system_backup.html:15`<br>`webroot_ro/system_password.html:15`<br>`webroot_ro/system_reboot.html:15` |
| R2 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| R2 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| R2 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 3 | E-R2-0011<br>E-R2-0012<br>E-R2-0013 | `bin/phddns@0xd3f5`<br>`webroot_ro/default.cfg:86`<br>`webroot_ro/goform/WifiPowerGet.txt:4` |
| R2 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| R2 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| R3 | CRED_DEFAULT_ADMIN_WEB | not_tested | 0 | 0 | 0 | — | — |
| R3 | CRED_DEFAULT_SERVICE_LOGIN | not_tested | 0 | 0 | 0 | — | — |
| R3 | CRED_HARDCODED_SECRET | not_tested | 0 | 0 | 0 | — | — |
| R3 | UNAUTH_MGMT_ENDPOINT | not_tested | 0 | 0 | 0 | — | — |
| R3 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| R3 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| R3 | EGRESS_FIXED_CLOUD_ENDPOINT | not_tested | 0 | 0 | 0 | — | — |
| R3 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| R3 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| C1 | CRED_DEFAULT_ADMIN_WEB | not_tested | 0 | 0 | 0 | — | — |
| C1 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 1 | E-C1-0001 | `etc/passwd:1` |
| C1 | CRED_HARDCODED_SECRET | not_tested | 0 | 0 | 0 | — | — |
| C1 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 1 | E-C1-0002 | `usr/sbin/uhttpd@0xeff0` |
| C1 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| C1 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| C1 | EGRESS_FIXED_CLOUD_ENDPOINT | not_tested | 0 | 0 | 0 | — | — |
| C1 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| C1 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| C2 | CRED_DEFAULT_ADMIN_WEB | not_tested | 0 | 0 | 0 | — | — |
| C2 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 1 | E-C2-0001 | `etc/passwd:1` |
| C2 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-C2-0002 | `etc/init.d/wlan-manager:118` |
| C2 | UNAUTH_MGMT_ENDPOINT | not_tested | 0 | 0 | 0 | — | — |
| C2 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| C2 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| C2 | EGRESS_FIXED_CLOUD_ENDPOINT | not_tested | 0 | 0 | 0 | — | — |
| C2 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| C2 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| C3 | CRED_DEFAULT_ADMIN_WEB | not_tested | 0 | 0 | 0 | — | — |
| C3 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 1 | E-C3-0001 | `etc/passwd:1` |
| C3 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-C3-0002 | `etc/init.d/wlan-manager:118` |
| C3 | UNAUTH_MGMT_ENDPOINT | not_tested | 0 | 0 | 0 | — | — |
| C3 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| C3 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| C3 | EGRESS_FIXED_CLOUD_ENDPOINT | not_tested | 0 | 0 | 0 | — | — |
| C3 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| C3 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| C4 | CRED_DEFAULT_ADMIN_WEB | not_tested | 0 | 0 | 0 | — | — |
| C4 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 1 | E-C4-0001 | `etc/passwd:1` |
| C4 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-C4-0002 | `etc/init.d/wlan-manager:118` |
| C4 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 1 | E-C4-0003 | `usr/sbin/uhttpd@0xda55` |
| C4 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| C4 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| C4 | EGRESS_FIXED_CLOUD_ENDPOINT | not_tested | 0 | 0 | 0 | — | — |
| C4 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| C4 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| C5 | CRED_DEFAULT_ADMIN_WEB | not_tested | 0 | 0 | 0 | — | — |
| C5 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 1 | E-C5-0001 | `etc/passwd:1` |
| C5 | CRED_HARDCODED_SECRET | not_tested | 0 | 0 | 0 | — | — |
| C5 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 1 | E-C5-0002 | `usr/sbin/uhttpd@0xef70` |
| C5 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| C5 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| C5 | EGRESS_FIXED_CLOUD_ENDPOINT | not_tested | 0 | 0 | 0 | — | — |
| C5 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| C5 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |

## 汇总

| 固件 | found | not_tested |
|---|---|---|
| A1 | 5 | 4 |
| A2 | 3 | 6 |
| A3 | 5 | 4 |
| A3-19 | 5 | 4 |
| R1 | 5 | 4 |
| R2 | 5 | 4 |
| R3 | 0 | 9 |
| C1 | 2 | 7 |
| C2 | 2 | 7 |
| C3 | 2 | 7 |
| C4 | 3 | 6 |
| C5 | 2 | 7 |
| **合计** | **39** | **69** |
