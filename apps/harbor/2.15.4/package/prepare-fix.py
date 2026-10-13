# -*- coding: utf-8 -*-
# harbor 安装后配置校正（prepare 之后、组件启动之前运行）。
# 背景：外部 TLS 终结场景（面板反代 443 → harbor-nginx:8080）下，prepare 按 http external_url
# 生成的两处配置会让 docker daemon 的 Bearer token 流程全挂（拉取一律 401）：
#   1) registry auth 被生成为 htpasswd（basic）——必须为 Harbor 标准的 token 模式；
#   2) core 的 EXT_ENDPOINT 带安装映射端口（http://host:port）——realm 随之错误，且 daemon 不跟随
#      http→https 重定向取匿名 token。
# 本脚本幂等：已是目标状态时原样通过。
import re

HARBOR_HOSTNAME = '${HARBOR_HOSTNAME}'  # compose 变量替换后为真实主机名

# 1) registry auth: htpasswd -> token（root.crt 已由 compose 挂载，与 core 私钥同批生成配对）
p = '/config/registry/config.yml'
s = open(p).read()
if 'rootcertbundle' not in s:
    tok = (
        'auth:\n'
        '  token:\n'
        '    realm: "https://' + HARBOR_HOSTNAME + '/service/token"\n'
        '    service: "harbor-registry"\n'
        '    issuer: "harbor-token-issuer"\n'
        '    rootcertbundle: /etc/registry/root.crt\n'
    )
    pat = (
        'auth:\n'
        '  htpasswd:\n'
        '    realm: harbor-registry-basic-realm\n'
        '    path: /etc/registry/passwd\n'
    )
    assert pat in s, 'registry auth anchor miss（prepare 模板可能已变更，请人工核对）'
    s = s.replace(pat, tok, 1)
    open(p, 'w').write(s)
    print('registry auth -> token mode')
else:
    print('registry auth already token mode')

# 2) core EXT_ENDPOINT -> https 主机名（realm 与对外入口一致）
e = '/config/core/env'
s = open(e).read()
if 'EXT_ENDPOINT=https://' in s:
    print('EXT_ENDPOINT already https')
else:
    s = re.sub(r'EXT_ENDPOINT=.*', 'EXT_ENDPOINT=https://' + HARBOR_HOSTNAME, s)
    open(e, 'w').write(s)
    print('EXT_ENDPOINT -> https')
