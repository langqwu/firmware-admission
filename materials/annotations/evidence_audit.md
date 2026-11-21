# 机器初标证据审计（A 预填）

> 生成规则：某 check_code 在 evidence 中有至少一条记录 → `found`；否则 `not_tested`。
> 没有 `clear`：当前没有逐项 runtime test 记录，不能用“未发现”冒充“已测清”。
> A 必须逐条核对 `raw_ref`；B 不得看本文件，必须独立标注。

| 固件 | 检查项 | 状态 | E1 | E2 | E3 | 证据 ID | raw_ref |
|---|---|---|---|---|---|---|---|
| A1 | CRED_DEFAULT_ADMIN_WEB | found | 0 | 0 | 1 | E-A1-0001 | `webroot_ro/default.cfg:48` |
| A1 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 1 | E-A1-0002 | `etc_ro/passwd:1` |
| A1 | CRED_HARDCODED_SECRET | found | 0 | 0 | 2 | E-A1-0003<br>E-A1-0004 | `etc_ro/prod-script:363`<br>`etc_ro/shadow:1` |
| A1 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 24 | E-A1-0009<br>E-A1-0010<br>E-A1-0011<br>E-A1-0012<br>E-A1-0013<br>E-A1-0014<br>E-A1-0015<br>E-A1-0016<br>E-A1-0017<br>E-A1-0018<br>E-A1-0019<br>E-A1-0020<br>E-A1-0021<br>E-A1-0022<br>E-A1-0023<br>E-A1-0024<br>E-A1-0025<br>E-A1-0026<br>E-A1-0027<br>E-A1-0028<br>E-A1-0029<br>E-A1-0030<br>E-A1-0031<br>E-A1-0032 | `bin/httpd@0x6e27c`<br>`bin/httpd@0x75be8`<br>`bin/httpd@0x75bf4`<br>`bin/httpd@0x75c10`<br>`bin/httpd@0x75c20`<br>`bin/httpd@0x75c48`<br>`bin/httpd@0x75c58`<br>`bin/httpd@0x75c6c`<br>`bin/httpd@0x75c84`<br>`bin/httpd@0x75c9c`<br>`bin/httpd@0x75cd4`<br>`bin/httpd@0x75cf0`<br>`bin/httpd@0x75d0c`<br>`bin/httpd@0x75d28`<br>`bin/httpd@0x75d3c`<br>`bin/httpd@0x75d50`<br>`bin/httpd@0x75d98`<br>`webroot_ro/app.js:338`<br>`webroot_ro/goform/clearSyslog/index.html:2`<br>`webroot_ro/goform/test/index.html:2`<br>`webroot_ro/js/system_config.js:177`<br>`webroot_ro/js/system_status.js:31`<br>`webroot_ro/js/wrl_advance.js:138`<br>`webroot_ro/js/wrl_basic.js:896` |
| A1 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| A1 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| A1 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 4 | E-A1-0005<br>E-A1-0006<br>E-A1-0007<br>E-A1-0008 | `bin/httpd@0x751f8`<br>`bin/httpd@0x75218`<br>`bin/httpd@0x75238`<br>`webroot_ro/goform/getCloud/index.html:6` |
| A1 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| A1 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| A2 | CRED_DEFAULT_ADMIN_WEB | found | 1 | 0 | 0 | E-A2-E1-0001 | `materials/firmae/dcs_login_home_headers.txt:1` |
| A2 | CRED_DEFAULT_SERVICE_LOGIN | not_tested | 0 | 0 | 0 | — | — |
| A2 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-A2-0001 | `etc/rc.d/init.d/pppoe.sh:8` |
| A2 | UNAUTH_MGMT_ENDPOINT | found | 0 | 1 | 2 | E-A2-E2-0001<br>E-A2-0003<br>E-A2-0004 | `materials/firmae/dcs_login_hnap.txt:1`<br>`etc/httpd.ini:2`<br>`usr/sbin/eventd@0x22690` |
| A2 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| A2 | UNAUTH_INFO_DISCLOSURE | found | 0 | 1 | 0 | E-A2-E2-0002 | `materials/firmae/dcs_login_hnap.txt:1` |
| A2 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 1 | E-A2-0002 | `web/cgi-bin/home.asp:619` |
| A2 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| A2 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| A3 | CRED_DEFAULT_ADMIN_WEB | found | 0 | 0 | 1 | E-A3-0001 | `webroot_ro/default.cfg:262` |
| A3 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 8 | E-A3-0002<br>E-A3-0003<br>E-A3-0004<br>E-A3-0005<br>E-A3-0006<br>E-A3-0007<br>E-A3-0008<br>E-A3-0009 | `etc_ro/passwd:1`<br>`etc_ro/passwd:2`<br>`etc_ro/passwd:3`<br>`etc_ro/passwd:4`<br>`etc_ro/passwd:5`<br>`webroot_ro/default.cfg:315`<br>`webroot_ro/default.cfg:323`<br>`webroot_ro/default.cfg:328` |
| A3 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-A3-0010 | `etc_ro/shadow:1` |
| A3 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 21 | E-A3-0016<br>E-A3-0017<br>E-A3-0018<br>E-A3-0019<br>E-A3-0020<br>E-A3-0021<br>E-A3-0022<br>E-A3-0023<br>E-A3-0024<br>E-A3-0025<br>E-A3-0026<br>E-A3-0027<br>E-A3-0028<br>E-A3-0029<br>E-A3-0030<br>E-A3-0031<br>E-A3-0032<br>E-A3-0033<br>E-A3-0034<br>E-A3-0035<br>E-A3-0036 | `bin/httpd@0xd4220`<br>`bin/httpd@0xd4238`<br>`bin/httpd@0xd4250`<br>`bin/httpd@0xd4268`<br>`bin/httpd@0xd4b6c`<br>`bin/httpd@0xd4b88`<br>`bin/httpd@0xd4ba0`<br>`bin/httpd@0xd4bac`<br>`bin/httpd@0xd4bd0`<br>`bin/httpd@0xd4bec`<br>`bin/httpd@0xd4c00`<br>`bin/httpd@0xd4cd4`<br>`bin/httpd@0xd4cec`<br>`bin/httpd@0xd4d08`<br>`bin/httpd@0xd4d58`<br>`etc_ro/nginx/conf/nginx.conf:48`<br>`webroot_ro/directupgrade.html:27`<br>`webroot_ro/js/dlna.js:134`<br>`webroot_ro/system_backup.html:15`<br>`webroot_ro/system_password.html:15`<br>`webroot_ro/system_reboot.html:15` |
| A3 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| A3 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| A3 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 5 | E-A3-0011<br>E-A3-0012<br>E-A3-0013<br>E-A3-0014<br>E-A3-0015 | `bin/phddns@0xd3f5`<br>`webroot_ro/default.cfg:86`<br>`webroot_ro/goform/WifiPowerGet.txt:4`<br>`webroot_ro/index.html:399`<br>`webroot_ro/xunleiDownload.html:40` |
| A3 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| A3 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| A3-19 | CRED_DEFAULT_ADMIN_WEB | found | 0 | 0 | 1 | E-A3-19-0001 | `webroot_ro/default.cfg:262` |
| A3-19 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 8 | E-A3-19-0002<br>E-A3-19-0003<br>E-A3-19-0004<br>E-A3-19-0005<br>E-A3-19-0006<br>E-A3-19-0007<br>E-A3-19-0008<br>E-A3-19-0009 | `etc_ro/passwd:1`<br>`etc_ro/passwd:2`<br>`etc_ro/passwd:3`<br>`etc_ro/passwd:4`<br>`etc_ro/passwd:5`<br>`webroot_ro/default.cfg:315`<br>`webroot_ro/default.cfg:323`<br>`webroot_ro/default.cfg:328` |
| A3-19 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-A3-19-0010 | `etc_ro/shadow:1` |
| A3-19 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 16 | E-A3-19-0016<br>E-A3-19-0017<br>E-A3-19-0018<br>E-A3-19-0019<br>E-A3-19-0020<br>E-A3-19-0021<br>E-A3-19-0022<br>E-A3-19-0023<br>E-A3-19-0024<br>E-A3-19-0025<br>E-A3-19-0026<br>E-A3-19-0027<br>E-A3-19-0028<br>E-A3-19-0029<br>E-A3-19-0030<br>E-A3-19-0031 | `bin/httpd@0xd4080`<br>`bin/httpd@0xd4098`<br>`bin/httpd@0xd40b0`<br>`bin/httpd@0xd40c8`<br>`bin/httpd@0xd4a20`<br>`bin/httpd@0xd4a30`<br>`bin/httpd@0xd4a84`<br>`bin/httpd@0xd4a9c`<br>`bin/httpd@0xd4ab8`<br>`bin/httpd@0xd4b20`<br>`etc_ro/nginx/conf/nginx.conf:48`<br>`webroot_ro/directupgrade.html:27`<br>`webroot_ro/js/dlna.js:134`<br>`webroot_ro/system_backup.html:15`<br>`webroot_ro/system_password.html:15`<br>`webroot_ro/system_reboot.html:15` |
| A3-19 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| A3-19 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| A3-19 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 5 | E-A3-19-0011<br>E-A3-19-0012<br>E-A3-19-0013<br>E-A3-19-0014<br>E-A3-19-0015 | `bin/phddns@0xd3f5`<br>`webroot_ro/default.cfg:86`<br>`webroot_ro/goform/WifiPowerGet.txt:4`<br>`webroot_ro/index.html:406`<br>`webroot_ro/xunleiDownload.html:40` |
| A3-19 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| A3-19 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| R1 | CRED_DEFAULT_ADMIN_WEB | found | 0 | 0 | 1 | E-R1-0001 | `webroot_ro/default.cfg:267` |
| R1 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 8 | E-R1-0002<br>E-R1-0003<br>E-R1-0004<br>E-R1-0005<br>E-R1-0006<br>E-R1-0007<br>E-R1-0008<br>E-R1-0009 | `etc_ro/passwd:1`<br>`etc_ro/passwd:2`<br>`etc_ro/passwd:3`<br>`etc_ro/passwd:4`<br>`etc_ro/passwd:5`<br>`webroot_ro/default.cfg:320`<br>`webroot_ro/default.cfg:328`<br>`webroot_ro/default.cfg:330` |
| R1 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-R1-0010 | `etc_ro/shadow:1` |
| R1 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 21 | E-R1-0016<br>E-R1-0017<br>E-R1-0018<br>E-R1-0019<br>E-R1-0020<br>E-R1-0021<br>E-R1-0022<br>E-R1-0023<br>E-R1-0024<br>E-R1-0025<br>E-R1-0026<br>E-R1-0027<br>E-R1-0028<br>E-R1-0029<br>E-R1-0030<br>E-R1-0031<br>E-R1-0032<br>E-R1-0033<br>E-R1-0034<br>E-R1-0035<br>E-R1-0036 | `bin/httpd@0xd2578`<br>`bin/httpd@0xd2590`<br>`bin/httpd@0xd25a8`<br>`bin/httpd@0xd25c0`<br>`bin/httpd@0xd2ec4`<br>`bin/httpd@0xd2ee0`<br>`bin/httpd@0xd2ef8`<br>`bin/httpd@0xd2f04`<br>`bin/httpd@0xd2f28`<br>`bin/httpd@0xd2f44`<br>`bin/httpd@0xd2f58`<br>`bin/httpd@0xd302c`<br>`bin/httpd@0xd3044`<br>`bin/httpd@0xd3060`<br>`bin/httpd@0xd30b0`<br>`etc_ro/nginx/conf/nginx.conf:48`<br>`webroot_ro/directupgrade.html:27`<br>`webroot_ro/js/dlna.js:134`<br>`webroot_ro/system_backup.html:15`<br>`webroot_ro/system_password.html:15`<br>`webroot_ro/system_reboot.html:15` |
| R1 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| R1 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| R1 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 5 | E-R1-0011<br>E-R1-0012<br>E-R1-0013<br>E-R1-0014<br>E-R1-0015 | `bin/phddns@0xd3f5`<br>`webroot_ro/default.cfg:87`<br>`webroot_ro/goform/WifiPowerGet.txt:4`<br>`webroot_ro/index.html:399`<br>`webroot_ro/xunleiDownload.html:40` |
| R1 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| R1 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| R2 | CRED_DEFAULT_ADMIN_WEB | found | 0 | 0 | 1 | E-R2-0001 | `webroot_ro/default.cfg:264` |
| R2 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 8 | E-R2-0002<br>E-R2-0003<br>E-R2-0004<br>E-R2-0005<br>E-R2-0006<br>E-R2-0007<br>E-R2-0008<br>E-R2-0009 | `etc_ro/passwd:1`<br>`etc_ro/passwd:2`<br>`etc_ro/passwd:3`<br>`etc_ro/passwd:4`<br>`etc_ro/passwd:5`<br>`webroot_ro/default.cfg:318`<br>`webroot_ro/default.cfg:326`<br>`webroot_ro/default.cfg:331` |
| R2 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-R2-0010 | `etc_ro/shadow:1` |
| R2 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 20 | E-R2-0016<br>E-R2-0017<br>E-R2-0018<br>E-R2-0019<br>E-R2-0020<br>E-R2-0021<br>E-R2-0022<br>E-R2-0023<br>E-R2-0024<br>E-R2-0025<br>E-R2-0026<br>E-R2-0027<br>E-R2-0028<br>E-R2-0029<br>E-R2-0030<br>E-R2-0031<br>E-R2-0032<br>E-R2-0033<br>E-R2-0034<br>E-R2-0035 | `bin/httpd@0xd048c`<br>`bin/httpd@0xd04a4`<br>`bin/httpd@0xd04bc`<br>`bin/httpd@0xd04d4`<br>`bin/httpd@0xd0dd8`<br>`bin/httpd@0xd0df4`<br>`bin/httpd@0xd0e0c`<br>`bin/httpd@0xd0e18`<br>`bin/httpd@0xd0e3c`<br>`bin/httpd@0xd0e58`<br>`bin/httpd@0xd0e6c`<br>`bin/httpd@0xd0f40`<br>`bin/httpd@0xd0f58`<br>`bin/httpd@0xd0f74`<br>`bin/httpd@0xd0fc4`<br>`webroot_ro/directupgrade.html:27`<br>`webroot_ro/js/dlna.js:134`<br>`webroot_ro/system_backup.html:15`<br>`webroot_ro/system_password.html:15`<br>`webroot_ro/system_reboot.html:15` |
| R2 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| R2 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| R2 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 5 | E-R2-0011<br>E-R2-0012<br>E-R2-0013<br>E-R2-0014<br>E-R2-0015 | `bin/phddns@0xd3f5`<br>`webroot_ro/default.cfg:86`<br>`webroot_ro/goform/WifiPowerGet.txt:4`<br>`webroot_ro/index.html:399`<br>`webroot_ro/xunleiDownload.html:40` |
| R2 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| R2 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| R3 | CRED_DEFAULT_ADMIN_WEB | not_tested | 0 | 0 | 0 | — | — |
| R3 | CRED_DEFAULT_SERVICE_LOGIN | not_tested | 0 | 0 | 0 | — | — |
| R3 | CRED_HARDCODED_SECRET | not_tested | 0 | 0 | 0 | — | — |
| R3 | UNAUTH_MGMT_ENDPOINT | not_tested | 0 | 0 | 0 | — | — |
| R3 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| R3 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| R3 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 5 | E-R3-0001<br>E-R3-0002<br>E-R3-0003<br>E-R3-0004<br>E-R3-0005 | `etc/ethertypes:7`<br>`etc/init.d/p910nd:113`<br>`etc/init.d/p910nd:28`<br>`etc/services:8`<br>`sbin/tr069@0x65c40` |
| R3 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| R3 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| C1 | CRED_DEFAULT_ADMIN_WEB | not_tested | 0 | 0 | 0 | — | — |
| C1 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 1 | E-C1t-0001 | `etc/passwd:1` |
| C1 | CRED_HARDCODED_SECRET | not_tested | 0 | 0 | 0 | — | — |
| C1 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 1 | E-C1t-0003 | `usr/sbin/uhttpd@0xeff0` |
| C1 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| C1 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| C1 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 1 | E-C1t-0002 | `etc/protocols:3` |
| C1 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| C1 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| C2 | CRED_DEFAULT_ADMIN_WEB | not_tested | 0 | 0 | 0 | — | — |
| C2 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 1 | E-C2t-0001 | `etc/passwd:1` |
| C2 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-C2t-0002 | `etc/init.d/wlan-manager:6` |
| C2 | UNAUTH_MGMT_ENDPOINT | not_tested | 0 | 0 | 0 | — | — |
| C2 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| C2 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| C2 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 1 | E-C2t-0003 | `etc/protocols:3` |
| C2 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| C2 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| C3 | CRED_DEFAULT_ADMIN_WEB | not_tested | 0 | 0 | 0 | — | — |
| C3 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 1 | E-C3t-0001 | `etc/passwd:1` |
| C3 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-C3t-0002 | `etc/init.d/wlan-manager:6` |
| C3 | UNAUTH_MGMT_ENDPOINT | not_tested | 0 | 0 | 0 | — | — |
| C3 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| C3 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| C3 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 1 | E-C3t-0003 | `etc/protocols:3` |
| C3 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| C3 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| C4 | CRED_DEFAULT_ADMIN_WEB | not_tested | 0 | 0 | 0 | — | — |
| C4 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 1 | E-C4t-0001 | `etc/passwd:1` |
| C4 | CRED_HARDCODED_SECRET | found | 0 | 0 | 1 | E-C4t-0002 | `etc/init.d/wlan-manager:6` |
| C4 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 1 | E-C4t-0004 | `usr/sbin/uhttpd@0xda55` |
| C4 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| C4 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| C4 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 1 | E-C4t-0003 | `etc/protocols:3` |
| C4 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| C4 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |
| C5 | CRED_DEFAULT_ADMIN_WEB | not_tested | 0 | 0 | 0 | — | — |
| C5 | CRED_DEFAULT_SERVICE_LOGIN | found | 0 | 0 | 1 | E-C5-0001 | `etc/passwd:1` |
| C5 | CRED_HARDCODED_SECRET | not_tested | 0 | 0 | 0 | — | — |
| C5 | UNAUTH_MGMT_ENDPOINT | found | 0 | 0 | 1 | E-C5-0003 | `usr/sbin/uhttpd@0xef70` |
| C5 | UNAUTH_COMMAND_EXEC | not_tested | 0 | 0 | 0 | — | — |
| C5 | UNAUTH_INFO_DISCLOSURE | not_tested | 0 | 0 | 0 | — | — |
| C5 | EGRESS_FIXED_CLOUD_ENDPOINT | found | 0 | 0 | 1 | E-C5-0002 | `etc/protocols:3` |
| C5 | EGRESS_PLAINTEXT_CHANNEL | not_tested | 0 | 0 | 0 | — | — |
| C5 | EGRESS_UNREGISTERED_THIRD_PARTY | not_tested | 0 | 0 | 0 | — | — |

## 汇总

| 固件 | found | not_tested |
|---|---|---|
| A1 | 5 | 4 |
| A2 | 5 | 4 |
| A3 | 5 | 4 |
| A3-19 | 5 | 4 |
| R1 | 5 | 4 |
| R2 | 5 | 4 |
| R3 | 1 | 8 |
| C1 | 3 | 6 |
| C2 | 3 | 6 |
| C3 | 3 | 6 |
| C4 | 4 | 5 |
| C5 | 3 | 6 |
| **合计** | **47** | **61** |

---

## 人工核验补记（A 侧，2026-11-21）

- 核验人：标注员 A；仓库 HEAD `33660ed`。
- 方法：下载 12 台固件（SHA-256 与 `materials/固件获取记录.md` 全对）→ WSL binwalk 解包 12/12 → 198 条 evidence 的 `raw_ref` 逐条打开原文核对 token（行号/`@0x` 偏移）；A2 运行时 3 条核对 `materials/firmae/dcs_*.txt`。
- 结果：108 格 **47 found / 61 not_tested / 0 clear / 0 TODO**；本表 108 行 ID 集合、E1/E2/E3 计数、raw_ref 与 evidence 完全一致（0 差异）；A 文件标签 **0 处需改**；198/198 raw_ref 可定位、198/198 token 命中。
- 证据质量（不属本表数据错误，属 `src/evidence.py` 提取规则误报）：27 条 EGRESS/CRED_HARDCODED 证据把标准文档 URL（iana/lanana/linuxbase/freebsd/broadband-forum）、HTML 超链接/帮助文本、工厂测试标记当成风险证据；其中 **11 格 found 仅靠误报证据**、4 格部分可疑。建议修规则并重生成 evidence 后再算双人标注。
- 明细：`materials/annotations/annotator_A_核验记录.md`、`materials/annotations/annotator_A_核验明细.json`。
