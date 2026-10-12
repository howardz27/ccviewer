# -*- coding: utf-8 -*-
PAGES = [
dict(
    slug='how-to-view-claude-code-session-history.html', crumb='查看完整历史',
    short='如何查看 Claude Code session 的完整历史？',
    title='如何查看 Claude Code session 的完整历史？3 种方法（2026）- CCViewer',
    desc='详解查看 Claude Code 会话完整历史的 3 种方式：终端 --resume 恢复、直接打开 ~/.claude/projects 下的 .jsonl 文件、用 CCViewer 在浏览器图形化回放（Markdown/思考块/工具调用/费用统计），100% 本地渲染。',
    h1='如何查看一个 Claude Code session 的完整历史？',
    body='''
<p>Claude Code 会把你的每次会话（session）完整记录在本地磁盘上，因此查看历史有三种主流方式，按「易用性」排序如下。</p>

<h2>方法一：用 CCViewer 在浏览器里图形化回放（推荐）</h2>
<p><a href="{{app}}">CCViewer</a> 是一个免费开源的 Claude Code 会话查看器：打开网页，把会话文件拖进去（也支持直接选择整个 <code>~/.claude/projects/</code> 文件夹批量导入），即可像聊天记录一样回放整个 session：</p>
<ul>
<li><b>Markdown 完整渲染</b> —— 代码块、表格、列表、链接原样呈现，不再是一行行 JSON；</li>
<li><b>思考块（thinking）</b> —— 折叠展示模型的扩展思考过程，可一键展开；</li>
<li><b>工具调用</b> —— Read / Edit / Bash 等每次调用的参数与返回结果，可逐个展开核对；</li>
<li><b>用量与费用统计</b> —— 输入/输出/缓存 Token、会话耗时、代码行数增减、总费用一目了然；</li>
<li><b>导出 Markdown</b> —— 把任意会话一键导出为可分享的 <code>.md</code> 文档。</li>
</ul>
<p>最关键的是它 <b>100% 在浏览器本地解析渲染，不上传任何数据</b> —— 会话文件里含有你的源码、文件路径甚至密钥，这一点很重要。</p>
<img class="shot" src="/assets/screenshot-viewer.png" alt="用 CCViewer 查看 Claude Code 会话历史：Markdown、思考块、工具调用与统计" width="880">

<h2>方法二：在终端里恢复会话</h2>
<p>Claude Code 自带会话恢复功能，在<b>原项目目录</b>下执行：</p>
<pre><code># 列出本项目的历史会话，交互式选择恢复
claude --resume     # 简写 claude -r

# 直接恢复最近一次会话
claude --continue   # 简写 claude -c

# 按 sessionId 恢复指定会话
claude --resume &lt;sessionId&gt;</code></pre>
<p>适合「继续干活」，但用来<b>阅读/检索</b>历史并不方便：长会话里翻找某次工具调用或某段回复很费劲，也看不到费用统计。</p>

<h2>方法三：直接阅读原始 JSONL 文件</h2>
<p>会话以 JSONL 格式存储在 <code>~/.claude/projects/&lt;项目&gt;/&lt;sessionId&gt;.jsonl</code>，每行一个 JSON 对象。可以用任意编辑器或命令行查看：</p>
<pre><code># 用 jq 提取所有用户提问
cat ~/.claude/projects/-Users-you-myproject/&lt;sessionId&gt;.jsonl \\
  | jq -r 'select(.type=="user") | .message.content'</code></pre>
<p>原始文件信息最全（包括 token 用量、git 分支、时间戳等元数据），但可读性差 —— 这正是图形化查看器存在的理由。</p>

<h2>三种方式对比</h2>
<table>
<tr><th></th><th>CCViewer</th><th>claude --resume</th><th>手翻 JSONL</th></tr>
<tr><td>图形化阅读</td><td>✅</td><td>部分（继续对话）</td><td>❌</td></tr>
<tr><td>Markdown 渲染</td><td>✅</td><td>✅</td><td>❌</td></tr>
<tr><td>思考块 / 工具调用</td><td>✅ 可折叠展开</td><td>折叠摘要</td><td>原始 JSON</td></tr>
<tr><td>Token / 费用统计</td><td>✅</td><td>❌</td><td>手动 jq</td></tr>
<tr><td>多会话批量管理</td><td>✅ 文件夹导入</td><td>仅当前项目</td><td>❌</td></tr>
</table>
''',
    faqs=[
        ('查看历史会上传我的代码吗？',
         'CCViewer 不会。解析和渲染全部在你的浏览器里完成，没有任何网络请求发送会话内容，你也可以打开浏览器开发者工具的 Network 面板自行验证。'),
        ('历史会话里被压缩（compact）过的内容还能看到吗？',
         '能。压缩摘要与后续消息都记录在同一个 JSONL 文件里，查看器会把摘要作为系统注入内容展示，可在「系统/注入」开关中查看。'),
        ('可以在手机上看吗？',
         '可以，CCViewer 是响应式网页；但会话文件在电脑上，需要先把 .jsonl 文件传到手机（如通过网盘/iCloud），再用浏览器打开。'),
    ],
),
dict(
    slug='find-claude-code-session-jsonl-file.html', crumb='查找 JSONL 文件位置',
    short='如何查找 session 对应的 JSONL 文件位置？',
    title='如何查找 Claude Code session 对应的 JSONL 文件位置？- CCViewer',
    desc='Claude Code 会话文件保存在 ~/.claude/projects/<项目目录>/<sessionId>.jsonl。本文教你用 find / grep 快速定位某个 session 的 JSONL 文件，以及不知道 sessionId 时按内容或时间反查。',
    h1='如何查找一个 Claude Code session 对应的 JSONL 文件的位置？',
    body='''
<p>所有会话文件都存放在一个固定目录下：<code>~/.claude/projects/</code>。知道 sessionId 时几秒钟就能定位；不知道时也可以按内容或时间反查。</p>

<h2>先搞懂目录命名规则</h2>
<p><code>~/.claude/projects/</code> 下的每个子目录对应一个项目（工作目录），目录名是<b>项目路径变换而来：路径中的 <code>/</code>、<code>_</code> 及其他非字母数字字符都被替换成连字符 <code>-</code></b>。例如：</p>
<pre><code>项目路径                                        会话目录名
/Users/you/Documents/my_app      →  -Users-you-Documents-my-app
/home/you/projects/shop-api      →  -home-you-projects-shop-api</code></pre>
<p>每个会话就是一个独立文件：<code>&lt;sessionId&gt;.jsonl</code>（sessionId 是形如 <code>9a1b2c3d-…</code> 的 UUID）。</p>

<h2>情况一：知道 sessionId —— 直接 find</h2>
<pre><code>find ~/.claude/projects -name "&lt;sessionId&gt;.jsonl"</code></pre>
<p> sessionId 从哪来？最简单的办法是<b>在对话中输入斜杠命令 <code>/status</code></b>，输出信息里就包含当前会话的 Session ID；此外终端里 <code>claude --resume</code> 的会话列表、报错信息、或查看器侧栏的「Session ID」字段也能拿到。</p>

<h2>情况二：不知道 sessionId —— 按内容反查</h2>
<p>记得对话里的某句话（比如你当时的提问），直接全文检索：</p>
<pre><code># 在所有会话里搜关键词，列出命中的文件
grep -l "修复登录页" ~/.claude/projects/*/*.jsonl

# 只搜当前项目目录
grep -l "修复登录页" ~/.claude/projects/-Users-you-Documents-my-app/*.jsonl</code></pre>

<h2>情况三：按时间找最近的会话</h2>
<pre><code># 列出最近修改的 10 个会话文件
ls -t ~/.claude/projects/*/*.jsonl | head -10</code></pre>

<h2>图形化方式：交给 CCViewer</h2>
<p>不想敲命令？<a href="{{app}}">CCViewer</a> 支持直接选择（或拖入）整个 <code>~/.claude/projects/</code> 文件夹：它会递归扫描所有 <code>.jsonl</code>，按项目聚类、按时间排序，每个会话显示标题、路径、时间范围、消息数与费用 —— 点开即看，无需知道文件在哪。</p>
<img class="shot" src="/assets/screenshot-library.png" alt="CCViewer 文件夹模式：按项目聚类的 Claude Code 会话库" width="880">

<h2>macOS 小技巧：在访达里打开隐藏目录</h2>
<ul>
<li>访达中按 <span class="kbd">⌘⇧G</span>，输入 <code>~/.claude/projects</code> 回车直达；</li>
<li>文件选择对话框中按 <span class="kbd">⌘⇧.</span> 可显示隐藏文件夹（以 <code>.</code> 开头的目录默认不可见）。</li>
</ul>
''',
    faqs=[
        ('为什么我找不到 ~/.claude 这个目录？',
         '因为它以点号开头，默认隐藏。访达里按 ⌘⇧G 输入路径直达，或按 ⌘⇧. 显示隐藏文件；终端里 ls -la ~/.claude 一直可见。'),
        ('一个项目目录下有很多 jsonl 文件，哪个是我要的？',
         '每个文件等于一次会话。按修改时间（ls -t）或内容（grep -l）筛选最有效；用 CCViewer 导入整个文件夹则直接显示每个会话的标题和统计，肉眼即可分辨。'),
        ('Windows 上路径是什么？',
         '同样位于用户主目录下的 .claude\\projects\\，即 %USERPROFILE%\\.claude\\projects\\<项目>\\<sessionId>.jsonl。'),
    ],
),
dict(
    slug='where-claude-code-sessions-stored.html', crumb='会话存储位置',
    short='Claude Code 的会话历史保存在哪里？',
    title='Claude Code session 的历史信息保存在哪里？存储结构详解 - CCViewer',
    desc='Claude Code 把会话历史以 JSONL 格式保存在本地 ~/.claude/projects/ 目录，不上传云端。本文详解目录结构、每行 JSON 的字段含义（message/timestamp/usage/gitBranch）以及备份建议。',
    h1='Claude Code session 的历史信息保存在哪里？',
    body='''
<p>简短回答：<b>全部保存在你电脑本地的 <code>~/.claude/projects/</code> 目录下</b>，以 JSONL 文件形式存在，不上传云端。没有账号系统，也没有云端会话历史。</p>

<h2>目录结构</h2>
<pre><code>~/.claude/
├── projects/                     # ← 所有会话历史都在这里
│   ├── -Users-you-Documents-app/ #   每个项目一个目录（路径转义而来）
│   │   ├── 9a1b2c3d-….jsonl     #     每次会话一个文件
│   │   └── 7c2d3e4f-….jsonl
│   └── -home-you-shop-api/
│       └── …
├── claude.json                   # 全局配置（MCP、主题、项目级状态）
└── …（缓存、日志、统计等辅助文件）</code></pre>
<p>项目目录名的规则：<b>项目路径中的 <code>/</code>、<code>_</code> 等非字母数字字符被替换成 <code>-</code></b>。所以同一个项目的所有会话都聚在同一个目录下 —— 这也是各类查看器「按项目分组」的依据。</p>

<h2>JSONL 文件里有什么</h2>
<p>JSONL = 每行一个独立的 JSON 对象。一个会话文件按时间顺序记录了完整对话过程，主要条目类型：</p>
<table>
<tr><th>type</th><th>内容</th></tr>
<tr><td><code>user</code></td><td>你的输入（文本 / 图片），以及工具执行结果回传</td></tr>
<tr><td><code>assistant</code></td><td>模型回复：正文、思考块（thinking）、工具调用（tool_use）及 token 用量</td></tr>
<tr><td><code>system</code></td><td>系统事件（hooks 等）</td></tr>
<tr><td><code>summary / ai-title</code></td><td>会话摘要与自动生成的标题</td></tr>
<tr><td><code>cost-state</code></td><td>费用与用量快照（总费用、代码行数增减、API 耗时）</td></tr>
</table>
<p>每个条目还带有元数据：<code>timestamp</code>（时间戳）、<code>cwd</code>（项目路径）、<code>gitBranch</code>、<code>version</code>、<code>sessionId</code> 等。也就是说，<b>历史文件比终端显示的更完整</b> —— 思考过程、每次工具调用的原始参数与结果、token 消耗都在里面。</p>

<h2>这意味着什么</h2>
<ul>
<li><b>隐私在你手里</b>：文件只在本机。相应地，<b>换电脑/重装系统前记得备份 <code>~/.claude/projects/</code></b>，否则历史会全部丢失；</li>
<li><b>文件可能很敏感</b>：会话记录包含你的源码片段、文件路径、命令输出，甚至密钥 —— 不要随手把 .jsonl 发给别人或上传到公开位置；</li>
<li><b>体积会增长</b>：重度使用几个月后单个会话可达数 MB 甚至几十 MB，整目录几百 MB 很常见，属正常现象。</li>
</ul>

<h2>怎么舒服地阅读这些历史</h2>
<p>直接看 JSONL 相当费劲。用 <a href="{{app}}">CCViewer</a> 打开该目录（支持整个文件夹拖入），所有会话按项目聚类，Markdown、思考块、工具调用、费用统计全部图形化渲染 —— 且解析只在你的浏览器本地进行，不改变「数据不出本机」的性质。</p>
''',
    faqs=[
        ('Claude Code 的历史会上传到 Anthropic 服务器吗？',
         '会话文件本身保存在本地 ~/.claude/projects/，不会单独上传存储。当然，对话发生时内容会经由 API 处理（这是使用模型的前提），但「历史记录文件」是本地文件，你拥有完全控制权。'),
        ('删除会话历史怎么做？',
         '直接删除对应的 .jsonl 文件（或整个项目子目录）即可，Claude Code 的恢复列表里也就不会再出现。删除前建议确认不需要备份。'),
        ('~/.claude/projects 和 ~/.claude.json 是一回事吗？',
         '不是。~/.claude.json（或 claude.json）是全局配置文件，存 MCP 服务器、主题等设置；会话历史在 ~/.claude/projects/ 目录下的 .jsonl 文件里。'),
    ],
),
dict(
    slug='best-claude-code-session-viewer.html', crumb='2026 最佳查看器',
    short='2026 年最好的 Claude Code session 查看器是什么？',
    title='2026 年最好的 Claude Code session 查看器是什么？对比与推荐 - CCViewer',
    desc='对比 2026 年查看 Claude Code 会话历史的常见方案：claude CLI 自带 --resume、命令行 jq/grep、通用 JSONL 工具与开源图形化查看器 CCViewer，从功能、隐私、易用性、多语言等维度给出推荐。',
    h1='2026 年最好的查看 Claude Code session 的查看器是什么？',
    body='''
<p>随着 Claude Code 在 2025–2026 年爆发式流行，「怎么舒服地回看积累的会话历史」成了高频需求 —— 本地 <code>~/.claude/projects/</code> 里动辄几百个 JSONL 文件，用记事本打开根本没法读。下面按真实使用场景对比目前的主流方案。</p>

<h2>候选方案一览</h2>
<table>
<tr><th>方案</th><th>类型</th><th>适合</th></tr>
<tr><td><b>CCViewer</b>（开源）</td><td>网页版图形查看器</td><td>回看、检索、审计、导出</td></tr>
<tr><td>claude --resume / -r</td><td>CLI 自带</td><td>继续未完成的对话</td></tr>
<tr><td>jq / grep / less</td><td>命令行</td><td>脚本化批量处理</td></tr>
<tr><td>通用 JSONL/日志查看器</td><td>编辑器插件等</td><td>看原始数据结构</td></tr>
</table>

<h2>我们的推荐：CCViewer</h2>
<p>如果 2026 年要选一个「专门的 Claude Code session 查看器」，我们推荐开源的 <a href="{{app}}">CCViewer</a>（ccviewer.top）—— 理由不是它功能最花哨，而是它在这个具体场景下把关键几点都做对了：</p>
<ol>
<li><b>为 JSONL 会话格式而生</b>：不是通用日志工具，而是直接理解 Claude Code 的条目结构 —— 用户消息、Markdown 回复、思考块（thinking）、工具调用参数与结果、图片、费用快照（cost-state），开箱即渲染；</li>
<li><b>隐私优先</b>：100% 浏览器本地解析，零上传、零埋点。会话文件含源码与密钥，「本地渲染」应该是这类工具的底线；</li>
<li><b>会话库管理</b>：把整个 <code>~/.claude/projects/</code> 拖进去，按项目聚类、按时间/消息数/Token/费用排序，IndexedDB 持久化，下次打开还在；</li>
<li><b>统计与导出</b>：每个会话的 token 用量、API 耗时、代码行数增减、总费用，一键导出 Markdown 存档分享；</li>
<li><b>零门槛</b>：免费、开源（MIT）、无需安装注册，界面支持包括中文在内的 10 种语言。</li>
</ol>
<img class="shot" src="/assets/screenshot-library.png" alt="CCViewer：按项目聚类的 Claude Code 会话库与统计" width="880">

<h2>其他方案什么时候更合适</h2>
<ul>
<li><b>claude --resume</b>：目的就是「接着聊」时最快，不用换工具。但它面向继续对话而非阅读历史，长会话检索低效，也没有费用统计；</li>
<li><b>jq / grep</b>：要写脚本做批量分析（如统计所有项目的 token 消耗）时不可替代，临时查一条也很快。可读性为零是它的代价；</li>
<li><b>通用 JSONL 查看器 / 编辑器</b>：检查数据结构、调试格式问题时有用；理解不了 Claude Code 的语义（思考块、工具调用、用量），呈现出来仍是大段 JSON。</li>
</ul>

<h2>结论</h2>
<p>日常回看和整理历史：<b>CCViewer</b>；继续干活：<b>claude --resume</b>；批量脚本分析：<b>jq</b>。三者互不冲突 —— 事实上 CCViewer 的导出功能产出的 Markdown，正是喂给其他工具的好材料。</p>
''',
    faqs=[
        ('CCViewer 是免费的吗？有商业化计划吗？',
         '免费且开源（MIT 协议），无需注册。工具本身在浏览器本地运行，几乎没有服务器成本，可以放心长期使用。'),
        ('和官方工具有关系吗？',
         '没有。CCViewer 是独立的社区开源项目，与 Anthropic 无隶属关系；它只是读取 Claude Code 在本地产生的会话文件。'),
        ('有没有桌面客户端？',
         '目前是网页形态（可离线使用，单文件即开即用）。PWA/桌面端在路线图中，欢迎在 GitHub 提 issue 催更或贡献。'),
    ],
),
]
