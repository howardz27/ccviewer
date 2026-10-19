# CCViewer 产品目录提交记录

核验日期：2026-10-19。只把有明确成功回执的操作记为“已提交”；审核通过并能访问公开详情页后，才能记为“已收录 / 新增公开外链”。本轮未付费。

## 本轮状态

| 渠道 | 实际动作 | 状态与下一步 |
| --- | --- | --- |
| [Future Tools](https://futuretools.io/submit-a-tool) | 提交 CCViewer、规范产品 URL、真实功能介绍，类别 Productivity，定价 Open Source，未订阅 newsletter | **已提交，待人工审核**。页面显示“Tool Submitted!”；未获得公开产品页，新增公开外链数暂计 0。 |
| [Product Hunt](https://www.producthunt.com/products/ccviewer?launch=ccviewer) | Google 登录成功；填写名称、tagline、427 字符简介、首条介绍、开源属性和免费定价，添加源码及 3 张真实截图，设置 Howard Zhu 为 Maker | **已提交并预约发布**。后台 Launch status 显示 Scheduled；选定最早时段 2026-10-20 12:01am PT，即北京时间 **2026-10-20 15:01**。尚未到正式发布时间。 |
| [Uneed](https://www.uneed.best/submit-a-tool) | 生成产品预览；本人完成 Google 验证后，Uneed 返回 OAuth state expired，已重新打开登录页 | **等待服务条款确认**。登录页明确写明登录即同意 Terms of Service；已向用户请求本次确认，尚未再次登录或提交。 |
| [ToolDirectory.AI](https://tooldirectory.ai/submit-tool) | 查看真实提交表单 | 页面写明提交进入 Stripe checkout，但显示总额 $0，未能确认免费路径，未提交或付款。 |
| [Toolify](https://www.toolify.ai/submit) | 核对官方提交页面 | 当前页面显示 $99 提交费用，本轮跳过。 |

Future Tools [提交成功截图](evidence/future-tools-submitted.png)。其他平台的预览、Google 账户选择或登录尝试都不计作已发布外链。

Product Hunt [产品页截图](evidence/product-hunt-created.png)、[预约成功回执](evidence/product-hunt-scheduled.png)。后台地址：[Pre-Launch Dashboard](https://www.producthunt.com/products/ccviewer/ccviewer/prelaunch)。只记录产品已创建和正式发布已预约，不将登录态页面可见误写成已经被搜索引擎收录。本次公开抓取工具暂时无法访问该新产品页，独立公开可访问性尚未验证。

图库最初自动抓取了 2 张图片，已替换为官网首页、会话查看器和会话库 3 张截图。本地批量上传停留在 Uploading，改用产品官网的公开图片 URL 添加成功；保存后的产品页核验到 3 张图库图片。缩略图由仓库原有 SVG 标志转换为 240×240 PNG，未生成新品牌图像。

## 复用提交材料

- 名称：CCViewer
- 规范产品链接：<https://ccviewer.top/claude-code-session-viewer/>
- 中文产品链接：<https://ccviewer.top/claude-code-session-viewer/zh/>
- 源码：<https://github.com/howardz27/ccviewer>
- 定价：Free / Open Source，MIT，无需注册或 API key。
- 类别：Developer Tools / Open Source / Productivity；它读取 AI 编程会话记录，本身不生成代码、不运行模型。
- 标签：Claude Code、JSONL、session history、developer tools、open source、Markdown export。
- 截图：[首页](../assets/screenshot-landing.png)、[查看器](../assets/screenshot-viewer.png)、[会话库](../assets/screenshot-library.png)。

Product Hunt tagline（60 字符以内）：

> Read Claude Code sessions locally, export Markdown

英文简介（500 字符以内）：

> CCViewer is a free, MIT-licensed browser viewer for saved Claude Code JSONL sessions. Import files or folders to read Markdown, thinking blocks and tool calls, inspect recorded token usage and costs, and export Markdown. Supports 10 languages and a single-file offline version. Files are processed locally. The hosted site loads Microsoft Clarity analytics and recordings; offline copies do not. No account or API key required.

首次介绍（已写入 Product Hunt 发布内容）：

> CCViewer makes saved Claude Code session files easier to review. Drop in a JSONL file or a project folder to explore messages, thinking blocks and tool calls, organize a local session library, and export Markdown.
>
> It is free and MIT licensed, with 10 interface languages and a downloadable single-file version. Statistics depend on what the imported file contains. CCViewer cannot resume conversations or recover missing records.
>
> Session files are processed locally. The hosted website loads Microsoft Clarity analytics and recordings; the offline copy does not. CCViewer is an independent community project with no affiliation to Anthropic.
>
> Feedback on file compatibility and reviewing long sessions is welcome. Source: https://github.com/howardz27/ccviewer

## 本轮站内增量与核验

发布基线为远端 main 的 `36bf166`；同步该版本后追加本轮改动，保留它已有的指南事实修订、隐私描述、实体图、示例与 llms.txt。

- 10 个工具页补充软件别名、分享图片、真实截图信息，并用 `describedby` 链接已有的 llms.txt。
- 40 篇文章通过 `about` 指向对应语言的 WebApplication 标识，使文章和产品的关系明确。
- 扩展原有静态验收，检查实体关联、图片存在性和纯文本资料入口；未改动统计策略。
- 本轮再次读取 GSC：sitemap 成功，发现 60 页；索引报告更新日期仍为 2026-10-12，不能当作今天的实时收录结果。详细基线见 [此前实施记录](seo-geo-2026-10-19.zh-CN.md)。

llms.txt 是可选资料入口，不是 AI 搜索收录保证。Google 明确说明 AI 搜索仍依赖可收录内容和通常的 SEO 基础，无需特殊 AI 文件：[Google AI 搜索说明](https://developers.google.com/search/docs/appearance/ai-features)。
