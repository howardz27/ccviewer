# CCViewer 功能、SEO 与外链建议

基于本仓库源码检查，2026-10-17。以下优先级是代码审查推断，尚无 Search Console、真实用户转化率或性能采样数据。

## 本次已完成

- Clarity 同意控制、生产域名开关、公开页面事件和本地会话停止录制；2026-10-18 已配置站点所有者提供的 Project ID `yzkymu6lyt`，仅在访客同意后加载。
- 60 个页面统一构建；CI 检查应用页和全部帮助文章，避免源代码改动未发布。
- 首页的帮助/文章链接烘焙为真实 href，关闭 JavaScript 也可发现；补充语言切换超链接，移除按浏览器语言强制跳转。
- 修复帮助页日语 OG locale `ja_JA` → `ja_JP`，补充 Twitter 分享卡；文章 BreadcrumbList 加入帮助中心，与可见面包屑保持一致。
- 10 种语言增加官方资源入口：Claude Code 工作原理、CLI 参考、JSON Lines、项目问题反馈。这些是本站出站链接。
- **实际新增站外反向链接**：在 [GitHub 仓库 About](https://github.com/howardz27/ccviewer) 的 Website 字段保存 `https://ccviewer.top/claude-code-session-viewer/`。此前该字段为空；[截图](evidence/github-backlink.png) 留存证据。是否被搜索引擎发现及其排名影响需后续观察。

## 功能优化

| 优先级 | 建议 | 当前依据与验收方式 |
| --- | --- | --- |
| P1 | 大文件分块解析、Web Worker、消息列表虚拟化 | 当前 `parse` 同步解析、`renderAll` 遍历全部条目，目录导入还重复解析与汇总。用 10/50/100 MB 人工生成文件测导入耗时、长任务及峰值内存，再确定阈值。 |
| P1 | 全文搜索 + 用户/助手/工具/时间范围筛选 | 当前可以排序和显示/隐藏类型，缺少明确的全文搜索入口。匹配片段高亮，并可直接跳到对应消息；先做单会话搜索，再做跨会话本地索引。 |
| P1 | 离线示例会话按钮 | 现在必须先找到真实 JSONL 才能体验。提供完全虚构、仓库内置示例，展示思考块、工具调用与费用；示例也沿用私有查看模式。 |
| P1 | 导入报告与失败反馈 | 读取失败会跳过部分文件，用户不易判断结果。显示成功/跳过/损坏数量、行号和可操作提示；原始路径/错误详情保留本地。 |
| P2 | 可选加载远程图片、导出脱敏预览 | Markdown 图片目前可直接请求远程地址；导出会带出源码和路径。增加远程图片加载开关，导出前预览并选择隐藏路径/密钥。 |
| P2 | 存储容量与备份入口 | IndexedDB 可能被浏览器回收。显示存储估计、按项目删除、备份/恢复；批量删除应可撤销或确认。 |

## SEO 下一步

1. **Search Console / Bing Webmaster 验证与提交 sitemap**：现有 sitemap 已覆盖 60 个规范地址。需要站点账户权限查看索引、搜索词、抓取及页面体验报告；不能凭页面存在认定已经收录。
2. **根路径改为服务器 301**：2026-10-18 已部署根路径 301、无后缀文章规范地址与 sitemap 统一，并修复 www DNS 与 HTTPS 主域跳转；线上 196 项 HTTP 检查通过。详见 [域名与重定向修复](domain-routing.zh-CN.md)。
3. **文章事实核查和搜索意图区分**：两篇“找文件 / 文件保存位置”有重叠；前者聚焦系统操作与排错，后者聚焦数据结构。核对会话保留、compaction、Web/桌面模式、配置路径等版本差异，替换绝对化的“完整保存 / 无云端历史”描述。只有实质修改时更新日期。
4. **提高内容独立价值**：对“best viewer”页标注由 CCViewer 作者撰写，公开比较标准和可复现示例，避免把自荐当独立测评；优先完善中英文再复核其他翻译。
5. **体验指标先测再改**：确认 LCP/INP/CLS；字体是否值得外部请求、文章截图尺寸/懒加载、长会话交互卡顿分别测量。不要未经数据支持承诺性能提升。
6. **结构化数据保持真实**：现有 WebApplication/Article/BreadcrumbList 可维护，FAQ 标记可作为页面语义保留，但 Google 已自 2026-05-07 停止展示 FAQ 富媒体结果，不能把它作为流量承诺；见 [Google 2026 年更新记录](https://developers.google.com/search/updates#june-2026)。

[Google 多语言指南](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites) 建议避免按推测语言强制跳转，并提供可点击语言链接；本次已落实。

## 后续外链与发布材料

已落实 GitHub About 外链；README 原有官网链接保留。可先完善 GitHub topics、正式 release、可复现演示，再发布实际使用案例。以下材料为草稿，尚未向第三方平台发布，也不代表收录成功。

| 渠道 | 内容与动作 | 当前状态 |
| --- | --- | --- |
| GitHub 仓库 About | 官网链接直接指向工具规范地址 | 已保存并验证 |
| Awesome Claude Code | 以真实使用和维护记录满足筛选条件后，由作者通过 issue 表单推荐 | 已核对贡献规则；尚未提交 |
| DEV Community / Hashnode | 发“如何本地回看 Claude Code JSONL”实测文章，包含安装、示例、隐私设计及源码链接 | 下方有简介草稿；尚未发布 |
| Product Hunt / Show HN | 准备真实演示、更新记录、产品截图及作者声明，发布时回应技术问题 | 尚未提交 |

Awesome Claude Code 当前要求项目至少 14 天且持续维护，或至少 100 stars，并要求推荐由人类通过网页 issue 表单提交，不能用 PR/gh 代替；[贡献规则](https://github.com/hesreallyhim/awesome-claude-code/blob/main/CONTRIBUTING.md)。本次没有绕过规则提交。

英文简介草稿：

> CCViewer is a free, MIT-licensed browser viewer for Claude Code JSONL session files. It renders Markdown, thinking blocks, tool calls, token usage and cost statistics, supports folder import and local session storage, and exports Markdown. Session files are processed locally. The hosted site offers opt-in analytics on public pages; offline copies do not load analytics. Available in 10 languages.

中文简介草稿：

> CCViewer 是免费、MIT 开源的 Claude Code JSONL 会话查看器，支持 Markdown、思考块、工具调用、Token 与费用统计、文件夹导入和 Markdown 导出。会话在浏览器本地处理，支持 10 种语言。线上公开页面提供可选统计，离线版本不加载统计。

产品地址：<https://ccviewer.top/claude-code-session-viewer/>；中文工具：<https://ccviewer.top/claude-code-session-viewer/zh/>；源码：<https://github.com/howardz27/ccviewer>。

外链质量应以相关用户是否获得帮助为准。付费买链接、自动评论和批量目录堆砌可能构成 [Google link spam](https://developers.google.com/search/docs/essentials/spam-policies#link-spam)，没有必要为此牺牲项目声誉。
