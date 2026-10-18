# 域名与 GSC 重定向修复

2026-10-18 线上检查确认：

**实施结果：** 已添加 www 的代理 DNS 记录，已启用 `CCViewer canonical HTTPS and non-www` 301 规则，并将 70 个发布文件部署到现有 `ccpeek` Worker。手动部署版本 `478ccb67`（此前为 `83608c29`）。生产环境 196 项 HTTP 检查全部通过，覆盖 60 个规范页、133 个永久别名、查询参数保留和真实 404；www 的 HTTPS 证书校验通过。公共 DNS 已恢复解析，本机路由器此前缓存的 NXDOMAIN 可能短时保留。

| 地址 | 修复前实际响应 | 原因 |
| --- | --- | --- |
| `https://www.ccviewer.top/` | DNS NXDOMAIN | 没有 www 解析记录，尚未进入 HTTP 或证书阶段 |
| `https://ccviewer.top/` | HTTP 200，HTML 内 meta refresh + JS 跳转 | 用浏览器跳转到工具子目录 |
| `http://ccviewer.top/` | HTTP 200 | 没有强制统一为 HTTPS |
| `/claude-code-session-viewer/help.html` | 307 → `/claude-code-session-viewer/help` | Workers 默认 HTML 处理去除单文件的 `.html` 后缀 |
| `/claude-code-session-viewer/help` | HTTP 200，但 canonical 仍为 `.html` | canonical/sitemap 与实际路由冲突；文章页同样受影响 |

## 仓库中的修复

- 保持已有非 www 主域和工具首页路径，避免再次迁移 10 个语言首页。
- 帮助页和文章页统一使用无后缀 URL；对应的 canonical、hreflang、OG、JSON-LD、首页入口、相关阅读、语言切换和 sitemap 同步修改。
- `build.py` 同时生成 `_redirects` 和 sitemap。50 个 `.html` 旧地址、对应的多余尾斜杠及 10 个首页的 `index` 别名使用 301，直接到最终规范地址；不存在跳转环或 sitemap 指向跳转源的问题。
- 根路径 `/`、`/index`、`/index.html` 使用 `_redirects` 的服务器 301 到工具首页；根 HTML 移除 meta refresh 和 JS 跳转，保留普通链接作为不支持服务器规则时的后备。
- `wrangler.jsonc` 明确 `html_handling: auto-trailing-slash` 和 `not_found_handling: none`，不把不存在的文章伪装成首页 200。
- 静态测试覆盖 60 个规范地址与重定向目标一致；`tests/check_routing.py` 检查实际 HTTP 响应、旧地址 301、查询参数保留和 404。

## Cloudflare 账户配置（已执行，供以后核查）

仅修改 HTML 无法修复 NXDOMAIN。以下 DNS 和规则已在用户登录后实际配置并通过线上验证。

1. 进入 `ccviewer.top` 区域 → DNS → Records，添加 **A 记录**：Name `www`，IPv4 `192.0.2.0`，Proxy **开启（橙云）**，TTL Auto。该保留地址仅用于 Cloudflare 直接执行重定向，不作为真实源站；不可切成灰云直连。若已有 www 记录，先检查现有目标和绑定，避免覆盖其他服务。
2. Rules → Redirect Rules，添加 301 动态跳转，仅匹配该站点的 HTTP 或 www：

   ```text
   (http.host in {"ccviewer.top" "www.ccviewer.top"} and
     (http.host eq "www.ccviewer.top" or not ssl))
   ```

   目标表达式：`concat("https://ccviewer.top", http.request.uri.path)`；勾选 **Preserve query string**。同域 HTTPS 不匹配，不会形成循环。www 的根路径会先统一主域，再由项目规则跳到工具首页；最多两次永久跳转。
3. 检查 SSL/TLS → Edge Certificates 的证书覆盖 `www.ccviewer.top`，等待状态 Active。不能用禁用 HTTPS 或降低 SSL 模式替代证书修复。
4. 用现有 `ccpeek` Worker 的发布流程部署本仓库更新，保持静态资源目录为仓库根目录，确保根 `_redirects`、sitemap 和生成页面一起上传。如果控制台名称与配置不符，以实际绑定 `ccviewer.top` 的项目为准，不能新建同名部署冒充修复。
5. 发布后运行 `python3 tests/check_routing.py --base https://ccviewer.top`，再确认 `https://www.ccviewer.top/claude-code-session-viewer/zh/help?utm_source=check` 经 301 后保留路径/参数并最终 200，且 HTTP 也统一到 HTTPS。

DNS 和重定向规则保存在 Cloudflare 区域中，不由 HTML 构建覆盖。`.assetsignore` 排除源码、文档、测试与本地状态，确保后续仓库自动部署的公开资产与本次上传范围一致。

## GSC 如何验收

- 提交 `https://ccviewer.top/sitemap.xml`，其中 60 个 URL 都应直接返回 200，canonical 指向自身。
- 对规范工具首页和一篇无后缀帮助页使用“测试实际网址”，确认可访问；必要时申请编入索引。
- 根路径、www、旧 `.html`、`index.html` 仍可能显示“网页会自动重定向”，这是别名 URL 的预期状态。目标是规范页可收录，不是让每个别名都收录，也不能保证报告立即清零。
- 没有读取账户中的具体 GSC 样例列表；上述根因由公开 DNS/HTTP 与仓库配置直接验证。

参考：[Cloudflare HTML 路由](https://developers.cloudflare.com/workers/static-assets/routing/advanced/html-handling/)、[www 与根域](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/#redirect-between-www-and-root-domain)、[静态重定向规则](https://developers.cloudflare.com/workers/static-assets/redirects/)、[Google Page with redirect 说明](https://support.google.com/webmasters/answer/7440203?hl=en#page_with_redirect)。
