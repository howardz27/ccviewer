# Microsoft Clarity 接入

配置文件：`claude-code-session-viewer/analytics.json`。

当前已配置站点所有者提供的 Project ID `yzkymu6lyt`。允许域名上的 HTTPS 公开页面会显示统计同意提示，用户允许后才加载 Clarity。将 `projectId` 清空并重新构建、发布即可关闭接入。

```json
{
  "projectId": "yzkymu6lyt",
  "allowedHosts": ["ccviewer.top", "www.ccviewer.top"]
}
```

填写后运行 `python3 claude-code-session-viewer/build.py`，再通过现有部署流程发布生成的 HTML。配置烘焙进全部 60 个页面，单文件下载不依赖额外 JS 文件。Project ID 是公开的客户端标识，不需要 API 密钥。

## 采集范围

- 仅允许配置域名上的 HTTPS 页面；localhost、预览域名、`file://`、带查询参数或片段的页面不加载统计。
- 用户明确允许后才下载 SDK。支持拒绝、撤回、180 天同意过期、Do Not Track 和 Global Privacy Control。
- 使用 Consent V2：`analytics_Storage: granted`、`ad_Storage: denied`。不调用 Identify API，不传递自定义用户、会话标识或文件属性。
- 记录公开首页和帮助页交互。允许的自定义事件仅为 `file_picker_open`、`folder_picker_open`、`paste_open`、`help_open`、`github_open`。
- 打开文件/目录选择器、粘贴框、读取已有会话库或导入文件时调用 `clarity('stop')`，此文档内不再恢复。取消选择也保持停止，重新加载公开页面后才重新判断许可。
- 查看器、会话库、粘贴区额外使用 `data-clarity-mask="true"`。正文、文件名、路径、提示词、token、费用、错误详情和 JSONL 不作为自定义事件参数。
- 撤回会清除第一方 Clarity cookie 并重新加载页面；这也会移除已下载的脚本。撤回不删除已经收集到的历史记录。其他标签页撤回时，本页也会停止并重新加载。

因此这些数据适合分析公开页面到文件入口的点击转化，不能据此推断导入成功率、会话阅读行为或导出成功率。Clarity 运行于页面内，这些保护依赖其 SDK 的停止与遮蔽行为，并不构成独立的安全沙箱。

## 发布前验证

1. 在 Clarity 项目设置启用 Consent Mode，Masking 建议选择 Strict。使用真实 ID 构建并部署到允许域名。
2. 新隐私窗口打开首页，拒绝前和拒绝后，Network 都不应出现 Clarity 请求。
3. 清除本站同意选择后允许统计，应只加载一次 `https://www.clarity.ms/tag/<ProjectID>`。确认 Consent V2 中广告为 denied。
4. 用不含敏感信息的测试 JSONL 验证文件、目录、粘贴、拖放、刷新恢复会话库入口；检查停止后不再录制新会话内容。停止时 SDK 可能发送此前已缓冲的公开页面数据。
5. 在 Clarity 仪表盘验证公开页录屏/热力图以及入口事件；不能仅凭脚本请求成功判定数据已入库。检查录屏没有本地会话内容。
6. 统计设置中撤回，再检查 cookie、重新加载后无 SDK 请求。验证 DNT/GPC、离线文件和 localhost 均不加载。

本地验证：`node tests/analytics.cjs`、`python3 tests/check_pages.py`。这些检查不代替真实项目的仪表盘验收。

参考：[Consent V2](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-consent-api-v2)、[遮蔽 API](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-masking)、[SDK stop 实现](https://github.com/microsoft/clarity/blob/master/packages/clarity-js/src/clarity.ts)。
