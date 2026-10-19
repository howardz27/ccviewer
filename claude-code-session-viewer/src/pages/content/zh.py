# -*- coding: utf-8 -*-
PAGES = [
dict(
    slug='how-to-view-claude-code-session-history.html',
    crumb='查看完整历史',
    short='如何查看 Claude Code 会话历史：3 种方法',
    title='如何查看 Claude Code 会话历史：3 种方法 | CCViewer',
    desc='通过 CCViewer 阅读 JSONL、在终端恢复会话或用 jq 检查记录。附虚构示例、Markdown 导出步骤及线上和离线使用边界。',
    h1='如何查看 Claude Code 会话历史：3 种方法',
    body=r'''
<p>阅读已保存的 Claude Code 对话，可以把 <code>.jsonl</code> 会话文件导入 CCViewer；继续原来的工作，用 <code>claude --resume</code>；检查原始记录或批量分析，用编辑器或 jq。查看器只能显示文件中仍然存在且受支持的记录。</p>
<h2>在浏览器里阅读和导出</h2>
<ol><li>找到会话文件，默认位于 <code>~/.claude/projects/</code> 下。</li><li>打开 <a href="{{app}}">CCViewer</a>，选择文件、粘贴 JSONL 文本，或导入整个项目文件夹。</li><li>展开工具调用和思考块，查看可用的用量字段，再按需导出 Markdown。</li></ol>
<p>文件夹导入后保存在当前浏览器的 IndexedDB 中。清理站点数据可能删除会话库，请保留原文件。Token 汇总依赖文件中的记录；存在费用快照时可以展示，但不能将其视为账单。</p>
<img class="shot" src="/assets/screenshot-viewer.png" alt="CCViewer 中的消息、工具调用和用量字段" width="880">
<h2>在终端继续会话</h2>
<pre><code>claude --resume
claude --continue
claude --resume SESSION_ID</code></pre>
<p>在相关项目目录运行。resume 用于继续交互；CCViewer 是阅读工具，不会向 Claude 发送新提示。当前会话选择器的行为以文末官方指南为准。</p>
<h2>检查原始 JSONL</h2>
<pre><code>jq -r 'select(.type == "user") | .message.content' session.jsonl</code></pre>
<p>部分 user 记录实际包含工具结果，编写脚本时需区分内容类型。损坏的 JSON 行可能使 jq 停止，修复前先保存原始副本。</p>
<h2>用虚构示例复现</h2>
<p>下载<a href="/assets/example-session.jsonl" download>人工构造的 JSONL 示例</a>后导入。示例包含提问、虚构的 Read 调用与结果、Markdown 回复，没有真实会话或凭据。120 个输入 Token 和 45 个输出 Token 均为演示数据。</p>
<h2>线上和离线版本的区别</h2>
<p>解析与渲染在本地完成。线上网站自动加载 Microsoft Clarity，进行统计和交互录制；会话中的远程图片也可能触发请求。需要断网使用时，从仓库下载 HTML 并在断网环境打开；离线副本不加载 Clarity。</p>
''',
    faqs=[('查看器能恢复已删除消息吗？', '不能。只能展示所选文件中仍然存在且受支持的记录。'), ('线上版本完全不联网吗？', '不是。文件本地处理，但线上站点加载 Microsoft Clarity 统计与交互录制，远程图片也可能触发请求。')],
),
dict(
    slug='find-claude-code-session-jsonl-file.html',
    crumb='查找 JSONL 文件位置',
    short='查找 Claude Code JSONL 文件：macOS、Linux、Windows',
    title='查找 Claude Code JSONL 文件：macOS、Linux、Windows | CCViewer',
    desc='用 macOS、Linux 和 PowerShell 命令查找 Claude Code JSONL 文件，排查自定义配置目录、WSL 和会话记录缺失。',
    h1='查找 Claude Code JSONL 文件：macOS、Linux、Windows',
    body=r'''
<p>先检查 <code>~/.claude/projects/</code>；如果设置了 <code>CLAUDE_CONFIG_DIR</code>，则检查该目录中的 <code>projects</code>。递归搜索比猜项目目录名更可靠。以下步骤适用于实际运行本地会话的机器。</p>
<h2>macOS / Linux：列出会话文件</h2>
<pre><code>session_root="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects"
find "$session_root" -type f -name '*.jsonl'
# 将 SESSION_ID 替换为已知的会话标识。
find "$session_root" -type f -name 'SESSION_ID.jsonl'</code></pre>
<p>macOS 访达可按 Command–Shift–G，输入 <code>~/.claude/projects/</code>。使用自定义配置目录时替换为实际路径。</p>
<h2>按记得的内容反查</h2>
<pre><code>find "$session_root" -type f -name '*.jsonl' \
  -exec grep -lF -- '修复登录页' {} +</code></pre>
<p>命令输出匹配的文件名，支持路径空格，按字面文本匹配。编码后的文本、图片或已经不存在的记录不一定能匹配到。</p>
<h2>Windows PowerShell：列出最近文件</h2>
<pre><code>$sessionRoot = if ($env:CLAUDE_CONFIG_DIR) {
  Join-Path $env:CLAUDE_CONFIG_DIR 'projects'
} else {
  Join-Path $env:USERPROFILE '.claude/projects'
}
Get-ChildItem -LiteralPath $sessionRoot -Filter *.jsonl -Recurse -File |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 10 FullName, LastWriteTime</code></pre>
<p>在 WSL 中运行的会话应检查对应 Linux 环境的主目录，不能默认认为它位于 Windows 用户目录。</p>
<h2>找不到文件时检查什么</h2>
<ul><li>确认运行会话的账号、机器、容器或远程环境。</li><li>检查自定义配置目录、隐藏文件和访问权限。</li><li>检查是否关闭了持久化，或者保留策略已清理记录。查看器不能通过导入文件夹恢复不存在的文件。</li></ul>
<p>定位后用 <a href="{{app}}">CCViewer</a> 打开。提示词历史与完整会话文件的区别见下方存储指南。</p>
''',
    faqs=[('默认目录为空怎么办？', '检查实际运行环境、自定义配置目录、持久化设置与保留策略。会话可能位于另一台机器上。'), ('可以直接导入文件夹吗？', '可以。CCViewer 将 JSONL 文件导入本地浏览器会话库，并按项目分组。')],
),
dict(
    slug='where-claude-code-sessions-stored.html',
    crumb='会话存储位置',
    short='Claude Code 会话保存在哪里？路径、结构与保留策略',
    title='Claude Code 会话保存在哪里？路径、结构与保留策略 | CCViewer',
    desc='区分 Claude Code 本地会话、提示词历史和配置目录，了解 JSONL 记录、保留策略、备份以及查看器的能力边界。',
    h1='Claude Code 会话保存在哪里？路径、结构与保留策略',
    body=r'''
<p>本地 Claude Code 会话的默认路径为 <code>~/.claude/projects/&lt;项目&gt;/&lt;会话ID&gt;.jsonl</code>。自定义配置目录会改变基础路径。这个本地存储结构不代表所有 Claude Code 界面或模型请求都只在本机运行。</p>
<h2>区分会话、提示词历史和配置</h2>
<table><tr><th>默认路径</th><th>用途</th></tr><tr><td><code>~/.claude/projects/</code></td><td>项目会话记录及相关数据</td></tr><tr><td><code>~/.claude/history.jsonl</code></td><td>提示词历史，不能替代完整对话文件</td></tr><tr><td><code>~/.claude/settings.json</code></td><td>用户设置</td></tr><tr><td><code>~/.claude.json</code></td><td>位于 .claude 目录外的状态或配置</td></tr></table>
<p>Windows 默认基础目录为 <code>%USERPROFILE%\.claude</code>。不同环境与版本的细节以官方目录文档为准。</p>
<h2>查看器能读取哪些记录</h2>
<p>JSONL 每行保存一个 JSON 值。CCViewer 识别用户和助手消息、工具调用与结果，以及部分系统和费用记录。文件中可能包含 <code>timestamp</code>、<code>sessionId</code>、<code>cwd</code>、<code>message.usage</code> 等字段。日志是持续变化的实现格式，不能保证每条记录都含所有字段。</p>
<h2>保留策略和缺失历史</h2>
<p>会话文件不能当作永久备份。Claude Code 有保留设置，也有关闭持久化的运行方式。清理行为可能随版本、界面和设置变化，请核对官方应用数据文档。压缩与缺失记录也会限制可还原的内容。</p>
<h2>备份与阅读</h2>
<p>迁移或清理前，把需要保留的会话复制到受访问控制的备份位置。文件可能包含源码、路径和命令输出。导入浏览器会话库后也应保留原件，因为清理浏览器数据会影响本地副本。</p>
<p><a href="{{app}}">CCViewer</a> 在本地读取文件，但线上版本仍加载 Clarity 统计和交互录制。本地有会话文件，不等于线上查看器或 Claude Code 模型请求完全不联网。</p>
''',
    faqs=[('history.jsonl 就是完整对话吗？', '不是。提示词历史和项目会话记录用途不同。'), ('本地保存意味着 Claude Code 离线吗？', '不是。本地会话存储与模型请求、云端或远程功能是不同的事情。')],
),
dict(
    slug='best-claude-code-session-viewer.html',
    crumb='2026 最佳查看器',
    short='Claude Code 会话查看工具对比：按任务选择',
    title='Claude Code 会话查看工具对比：按任务选择 | CCViewer',
    desc='按阅读、继续编程、脚本分析等任务比较 CCViewer、claude --resume、jq 和编辑器，提供可复现示例并说明功能与隐私边界。',
    h1='Claude Code 会话查看工具对比：按任务选择',
    body=r'''
<p>最佳方法取决于任务：图形化阅读和 Markdown 导出可用 CCViewer；继续工作用 Claude Code 的 resume；检查原始结构用 jq 或编辑器。本文由 CCViewer 项目编写，是作者对工作方式的比较，不是独立评测、性能基准或完整产品排行榜。</p>
<h2>按任务选择</h2>
<table><tr><th>任务</th><th>工具</th><th>边界</th></tr><tr><td>阅读消息、展开工具调用</td><td>CCViewer</td><td>依赖导入文件中受支持的记录</td></tr><tr><td>继续已有上下文的编程任务</td><td><code>claude --resume</code></td><td>进入 Claude Code 交互</td></tr><tr><td>脚本筛选或汇总记录</td><td>jq / grep</td><td>需要理解记录结构</td></tr><tr><td>检查或修复损坏的 JSON</td><td>文本编辑器</td><td>应操作副本，保留原件</td></tr></table>
<h2>CCViewer 当前的能力</h2>
<p>支持 Markdown、已有思考块和工具记录的渲染、文件夹导入、会话排序和 Markdown 导出；界面有 10 种语言，代码采用 MIT 许可。目前不能继续 Claude 对话、恢复已删除日志，也没有跨会话库的内置全文搜索。用量汇总取决于输入记录。</p>
<h2>如何复现比较</h2>
<ol><li>下载<a href="/assets/example-session.jsonl" download>虚构示例文件</a>。</li><li>导入 <a href="{{app}}">CCViewer</a>，检查提问、Read 调用、工具结果和 Markdown 回复。</li><li>在编辑器中打开同一文件，比较文本与示例中的 120/45 Token 数字。</li><li>导出 Markdown，检查结果。示例只用于阅读验证，不应用作可恢复的 Claude Code 会话。</li></ol>
<h2>隐私和使用边界</h2>
<p>线上网站加载 Clarity 统计与交互录制；离线副本不加载统计。联网时，记录中的远程图片仍可能触发外部请求。大文件同步解析可能阻塞界面，清理浏览器存储会删除本地会话库。请保留原件，并按需要选择断网运行的离线副本。</p>
''',
    faqs=[('这是一份独立评测吗？', '不是。本文由 CCViewer 项目编写，比较工作方式，并未穷尽所有产品。'), ('CCViewer 支持跨会话全文搜索吗？', '目前没有内置的跨会话库全文搜索，需要这项能力时可使用文本搜索工具。')],
),
]
