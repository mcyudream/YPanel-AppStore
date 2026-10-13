# -*- coding: utf-8 -*-
# harbor 安装后配置校正（prepare 之后、组件启动之前运行）。
#
# 生产实证（2026-10-13，Harbor 2.15.4 + 外部 TLS 终结/面板反代 443）：
#   1) registry auth 必须保持 prepare 生成的 htpasswd 模式（改为 token 模式是死路——该部署 /v2/
#      经 core，core 验签后以 REGISTRY_CREDENTIALS basic 转发 registry，token 模式的 registry 会
#      拒绝 basic 转发导致一切拉取/推送 401）；
#   2) registry 的 passwd（包内静态 bcrypt）与 prepare 生成的 core REGISTRY_CREDENTIAL_PASSWORD
#      （安装时随机）互不校验且不一致——必须用 core 的随机密码重新生成 passwd 条目，否则 core
#      代理 /v2/ 的 basic 转发全部 401；
#   3) core 的 EXT_ENDPOINT 去掉 http 端口改为 https 主机名（token realm 与对外入口一致）。
# 幂等；仅用 python3 标准库（prepare 容器无 bcrypt，passwd 条目用 {SHA} 格式，distribution 原生支持）。
import base64
import hashlib
import re

HARBOR_HOSTNAME = '${HARBOR_HOSTNAME}'  # compose 变量替换后为真实主机名

# 1) registry auth 保持/回滚为 htpasswd 模式
p = '/config/registry/config.yml'
s = open(p).read()
if 'rootcertbundle' in s:
    htpasswd = (
        'auth:\n'
        '  htpasswd:\n'
        '    realm: harbor-registry-basic-realm\n'
        '    path: /etc/registry/passwd\n'
    )
    s = re.sub(
        r'auth:\n  token:\n    realm: "[^"]*"\n    service: "harbor-registry"\n    issuer: "harbor-token-issuer"\n    rootcertbundle: /etc/registry/root.crt\n',
        htpasswd, s)
    open(p, 'w').write(s)
    print('registry auth -> htpasswd mode (corrected from token)')
else:
    print('registry auth already htpasswd mode')

# 2) core EXT_ENDPOINT -> https 主机名
e = '/config/core/env'
s = open(e).read()
if 'EXT_ENDPOINT=https://' in s:
    print('EXT_ENDPOINT already https')
else:
    s = re.sub(r'EXT_ENDPOINT=.*', 'EXT_ENDPOINT=https://' + HARBOR_HOSTNAME, s)
    open(e, 'w').write(s)
    print('EXT_ENDPOINT -> https')

# 3) passwd 与 core REGISTRY_CREDENTIAL_PASSWORD 对齐（{SHA} 条目替换包内静态 bcrypt 行）
m = re.search(r'^REGISTRY_CREDENTIAL_PASSWORD=(.*)$', open('/config/core/env').read(), re.M)
if not m:
    raise SystemExit('REGISTRY_CREDENTIAL_PASSWORD not found in core env')
pw = m.group(1).strip()
sha1 = hashlib.sha1(pw.encode()).digest()
entry = 'harbor_registry_user:{SHA}' + base64.b64encode(sha1).decode()
pe = '/config/registry/passwd'
lines = [l for l in open(pe).read().splitlines() if l and not l.startswith('harbor_registry_user:')]
lines.insert(0, entry)
open(pe, 'w').write('\n'.join(lines) + '\n')
print('passwd aligned with core credentials ({SHA} entry)')
