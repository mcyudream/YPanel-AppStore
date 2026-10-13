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

# 3) registry htpasswd 与 core REGISTRY_CREDENTIAL_PASSWORD 对齐（两者由 prepare 独立生成但互不校验，
#    实测会不一致导致 core 代理 /v2/ 时 basic 转发全部 401）。此处以 core 的密码为准重生成 passwd 条目。
#    注意：本脚本在 prepare 容器内执行（挂载 /config），passwd 经 bcrypt 生成需要容器内 python3+bcrypt；
#    prepare 镜像无 bcrypt 时，请部署后在宿主机执行（面板 /tmp 脚本通道）：
#      PW=$(docker exec app-harbor-core sh -c "env | grep '^REGISTRY_CREDENTIAL_PASSWORD=' | cut -d= -f2-")
#      HASH=$(python3 -c "import bcrypt,sys; print(bcrypt.hashpw(sys.argv[1].encode(), bcrypt.gensalt(10).decode())" "$PW")
#      echo "harbor_registry_user:$HASH" > common/config/registry/passwd && docker restart app-harbor-registry
e = '/config/registry/passwd'
s2 = open(e).read()
core_user = 'harbor_registry_user'
line_ok = False
try:
    import bcrypt  # noqa
    m = re.search(r'REGISTRY_CREDENTIAL_PASSWORD=(.*)', open('/config/core/env').read())
    if m:
        pw = m.group(1).strip()
        h = bcrypt.hashpw(pw.encode(), bcrypt.gensalt(rounds=10)).decode()
        s2 = re.sub(r'^' + re.escape(core_user) + r':.*$', core_user + ':' + h, s2, flags=re.M)
        if core_user + ':' not in s2:
            s2 += core_user + ':' + h + '
'
        open(e, 'w').write(s2)
        line_ok = True
except ImportError:
    pass  # prepare 镜像无 bcrypt：按上方注释在宿主机手工对齐
print('passwd aligned:', line_ok)
