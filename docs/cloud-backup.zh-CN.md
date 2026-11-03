# 云端 JSONL 备份

查看器仍可离线、免登录使用。点击首页、查看器工具栏或会话库的「云端备份」后，才会连接同源 `/api/` 接口；用户使用 GitHub 登录后，主动选择文件上传，或备份当前已打开的会话。每次上传创建一个新副本，不会自动同步或覆盖旧备份。面板支持分页列表、恢复阅读、下载原始 JSONL 和删除。恢复阅读会保存一份本地会话库副本，删除云端备份不会删除本地副本。

## 首次启用

1. 当前部署使用 Cloudflare 账号 `6278c618c2116c56eaca62247e0b1871` 中已创建的 R2 bucket `ccviewer`，无需重复创建。自建其他部署时可创建自己的 bucket，并更新 `wrangler.jsonc` 的账号和 bucket 名称：

   ```bash
   pnpm dlx wrangler@4.151.1 r2 bucket create ccviewer
   ```

   `wrangler.jsonc` 已将 `ccviewer` 绑定为 `BACKUPS`。Worker 通过绑定直接访问 R2，无需 S3 endpoint 或 S3 Access Key。S3 endpoint 仅供外部 S3 客户端使用，不需写入前端。保持 bucket 私有，**不要启用 r2.dev 公共访问或绑定公共自定义域名**，其中同时存储备份文件和登录会话。

2. 在 [GitHub Developer settings](https://github.com/settings/developers) 创建 OAuth App：

   - Homepage URL：`https://ccviewer.top`
   - Authorization callback URL：`https://ccviewer.top/api/auth/github/callback`

   应用只读取 GitHub 的基本公开身份，不申请仓库、邮箱或 gist 权限。使用 GitHub 不变的数字用户 ID 隔离数据，修改用户名不会丢失备份。

   当前已创建的 OAuth App 为 `CCViewer`，Client ID 已写入 `wrangler.jsonc` 的 `vars.GITHUB_CLIENT_ID`。Client ID 是公开标识；自建部署时替换为自己的应用 ID。

3. 为 OAuth App 生成 Client Secret，并在部署的 Cloudflare Worker（当前名称为 `ccpeek`）中添加同名 Secret，或使用交互式命令输入：

   ```bash
   pnpm dlx wrangler@4.151.1 secret put GITHUB_CLIENT_SECRET
   ```

   不要将 Secret 写入源码、命令参数、提交记录或静态资源。自定义部署域名时同步修改 `wrangler.jsonc` 的 `APP_ORIGIN`（只有 origin，不带尾部 `/`）、GitHub Homepage URL 和 callback URL。

4. 在 R2 bucket 的 Settings → Object lifecycle rules 设置清理规则：

   | 前缀 | 删除时间 | 用途 |
   | --- | --- | --- |
   | `auth/flows/` | 上传 1 天后 | 清理未完成的 OAuth 登录流程；应用内 10 分钟即失效 |
   | `auth/sessions/` | 上传 7 天后 | 清理过期登录会话；应用内同样校验有效期 |

   **不要对 `backups/` 设置上述清理规则。** 备份保留至用户主动删除。生命周期清理用于回收对象，登录有效期由应用校验，不依赖清理任务何时执行。

5. 构建、校验并部署：

   ```bash
   python3 claude-code-session-viewer/build.py
   node --test tests/cloud-backup.mjs
   node tests/cloud-backup-ui.cjs
   pnpm dlx wrangler@4.151.1 deploy --dry-run
   pnpm dlx wrangler@4.151.1 deploy
   ```

   缺少 R2 或 OAuth 配置时，页面会显示尚未配置，本地查看仍可使用。普通静态托管（如 GitHub Pages、Python HTTP Server）只能使用本地查看功能；云端备份需要此 Worker 后端。

## 本地开发

在项目根目录创建 `.dev.vars`（已加入 `.gitignore` 和 `.assetsignore`）：

```dotenv
APP_ORIGIN="http://127.0.0.1:8787"
GITHUB_CLIENT_ID="本地测试 OAuth App 的 Client ID"
GITHUB_CLIENT_SECRET="本地测试 OAuth App 的 Client Secret"
```

本地 OAuth App 的 callback URL 应为 `http://127.0.0.1:8787/api/auth/github/callback`。本地与线上使用不同 OAuth App，避免修改线上回调。启动：

```bash
pnpm dlx wrangler@4.151.1 dev --local --port 8787
# 打开 http://127.0.0.1:8787/claude-code-session-viewer/zh/
```

R2 默认使用本地模拟存储，不会读取线上备份。浏览器必须使用与 `APP_ORIGIN` 完全相同的 origin。

## 实现和边界

- 后端：`worker/index.mjs`；前端：`claude-code-session-viewer/src/cloud-backup.js`，构建时内联到 10 个语言页面，保持单 HTML 离线副本。
- 每个文件最大 20 MiB（实际字节数），必须为非空 UTF-8 `.jsonl`，每个非空行必须是 JSON 对象；保留上传原始字节。JSON 数组和损坏/未写完的 JSONL 会被拒绝，本地查看仍使用原来的宽松解析器。
- R2 路径：`backups/github-<用户数字 ID>/<随机 UUID>.jsonl`。客户端不能传 owner 或完整对象 key。文件名、记录数保存为对象元数据，不额外引入数据库。
- OAuth 使用随机 state 和 PKCE；登录流程绑定浏览器 Cookie。GitHub access token 只用于回调中读取身份，不存入 R2、不返回浏览器。登录会话使用随机令牌，R2 仅保存令牌的 SHA-256 摘要作为 key。
- 线上 Cookie 为 `__Host-`、`Secure`、`HttpOnly`、`SameSite=Lax`；7 天到期，退出登录立即删除服务端会话。HTTP 本地开发使用不带 `__Host-` 的 Cookie。
- 写操作要求同源 Origin 和自定义请求头；所有 API 响应均 `Cache-Control: no-store`，不开放 CORS。下载通过已登录接口流式返回，无公开文件 URL。
- 面板中的账号、文件名和备份列表标记了 Clarity masking；不添加文件名或内容到统计事件。页面仍沿用项目已有的 Clarity 配置。
- 本版本未实现用户总容量/文件数量配额、付费套餐、批量同步、端到端加密或找回已删除的云端文件。存储费用由部署账号承担；面向公众大规模开放前，可按业务需求增加配额与限流。

## 验证

`tests/cloud-backup.mjs` 使用内存存储和模拟 GitHub 响应验证接口行为，不需要真实账号或线上存储；`tests/cloud-backup-ui.cjs` 验证前端按需请求、错误处理、上传、恢复和退出流程。真实 GitHub 授权回跳需要完成上述 OAuth 配置后验证。

参考：[GitHub OAuth 流程](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps)、[R2 Workers API](https://developers.cloudflare.com/r2/api/workers/workers-api-reference/)、[R2 生命周期](https://developers.cloudflare.com/r2/buckets/object-lifecycles/)。
