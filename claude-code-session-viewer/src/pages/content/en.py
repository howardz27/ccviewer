# -*- coding: utf-8 -*-
PAGES = [
dict(
    slug='how-to-view-claude-code-session-history.html', crumb='View full history',
    short='How to view the full history of a Claude Code session',
    title='How to View the Full History of a Claude Code Session — 3 Methods (2026) | CCViewer',
    desc='Three ways to view your complete Claude Code session history: claude --resume in the terminal, opening the .jsonl files under ~/.claude/projects, or replaying them visually in the browser with CCViewer (Markdown, thinking blocks, tool calls, cost stats) — 100% local rendering.',
    h1='How do I view the full history of a Claude Code session?',
    body='''
<p>Claude Code records every session completely on your local disk, so there are three main ways to view the history — ranked by ease of use below.</p>

<h2>Method 1: Replay it visually in the browser with CCViewer (recommended)</h2>
<p><a href="{{app}}">CCViewer</a> is a free, open-source Claude Code session viewer. Open the page, drop in a session file (you can also pick the whole <code>~/.claude/projects/</code> folder to import everything), and replay the session like a chat transcript:</p>
<ul>
<li><b>Full Markdown rendering</b> — code blocks, tables, lists and links rendered as-is, no more walls of JSON;</li>
<li><b>Thinking blocks</b> — the model\u2019s extended reasoning, collapsible with one click;</li>
<li><b>Tool calls</b> — parameters and results of every Read / Edit / Bash call, expandable for inspection;</li>
<li><b>Usage &amp; cost stats</b> — input/output/cache tokens, session duration, lines added/removed, total cost at a glance;</li>
<li><b>Markdown export</b> — turn any session into a shareable <code>.md</code> document in one click.</li>
</ul>
<p>Crucially, it <b>parses and renders 100% locally in your browser — nothing is uploaded</b>. That matters: session files contain your source code, file paths and sometimes secrets.</p>
<img class="shot" src="/assets/screenshot-viewer.png" alt="Viewing Claude Code session history with CCViewer: Markdown, thinking blocks, tool calls and stats" width="880">

<h2>Method 2: Resume the session in the terminal</h2>
<p>Claude Code has built-in session resume. Run this in the <b>original project directory</b>:</p>
<pre><code># List this project's sessions and pick one interactively
claude --resume     # shorthand: claude -r

# Resume the most recent session directly
claude --continue   # shorthand: claude -c

# Resume a specific session by ID
claude --resume &lt;sessionId&gt;</code></pre>
<p>Great for "keep working", but inconvenient for <b>reading or searching</b> history: digging through a long session for one tool call is painful, and there are no cost stats.</p>

<h2>Method 3: Read the raw JSONL file</h2>
<p>Sessions are stored as JSONL at <code>~/.claude/projects/&lt;project&gt;/&lt;sessionId&gt;.jsonl</code> — one JSON object per line. You can inspect them with any editor or the command line:</p>
<pre><code># Extract all user prompts with jq
cat ~/.claude/projects/-Users-you-myproject/&lt;sessionId&gt;.jsonl \\
  | jq -r 'select(.type=="user") | .message.content'</code></pre>
<p>The raw file is the most complete source (token usage, git branch, timestamps and other metadata), but readability is poor — which is exactly why graphical viewers exist.</p>

<h2>Comparison</h2>
<table>
<tr><th></th><th>CCViewer</th><th>claude --resume</th><th>Raw JSONL</th></tr>
<tr><td>Graphical reading</td><td>✅</td><td>Partial (continue chat)</td><td>❌</td></tr>
<tr><td>Markdown rendering</td><td>✅</td><td>✅</td><td>❌</td></tr>
<tr><td>Thinking / tool calls</td><td>✅ collapsible</td><td>Collapsed summary</td><td>Raw JSON</td></tr>
<tr><td>Token / cost stats</td><td>✅</td><td>❌</td><td>Manual jq</td></tr>
<tr><td>Multi-session library</td><td>✅ folder import</td><td>Current project only</td><td>❌</td></tr>
</table>
''',
    faqs=[
        ('Does viewing history upload my code?',
         'No. CCViewer parses and renders everything in your browser; no network request ever carries session content. You can verify this yourself in the DevTools Network panel.'),
        ('Can I still see compacted parts of a session?',
         'Yes. Compaction summaries and subsequent messages live in the same JSONL file; the viewer shows summaries as injected context, visible via the "System/Injected" toggle.'),
        ('Does it work on mobile?',
         'Yes — CCViewer is a responsive web page. The session files live on your computer though, so you first need to copy the .jsonl to your phone (e.g. via iCloud/cloud drive) and open it in a browser.'),
    ],
),
dict(
    slug='find-claude-code-session-jsonl-file.html', crumb='Find the JSONL file',
    short='How to find the JSONL file for a session',
    title='How to Find the JSONL File Location of a Claude Code Session | CCViewer',
    desc='Claude Code session files live at ~/.claude/projects/<project-dir>/<sessionId>.jsonl. Learn how to locate a session\u2019s JSONL file quickly with find/grep, and how to search by content or time when you don\u2019t know the sessionId.',
    h1='How do I find the JSONL file location of a Claude Code session?',
    body='''
<p>All session files live under one fixed directory: <code>~/.claude/projects/</code>. If you know the sessionId, locating the file takes seconds; if you don\u2019t, you can search by content or time.</p>

<h2>First, understand the directory naming</h2>
<p>Each subdirectory of <code>~/.claude/projects/</code> corresponds to one project (working directory). The name is <b>derived from the project path: <code>/</code>, <code>_</code> and other non-alphanumeric characters are replaced with hyphens <code>-</code></b>. For example:</p>
<pre><code>Project path                       Session directory
/Users/you/Documents/my_app      →  -Users-you-Documents-my-app
/home/you/projects/shop-api      →  -home-you-projects-shop-api</code></pre>
<p>Each session is one file: <code>&lt;sessionId&gt;.jsonl</code> (a UUID like <code>9a1b2c3d-…</code>).</p>

<h2>Case 1: you know the sessionId — just find it</h2>
<pre><code>find ~/.claude/projects -name "&lt;sessionId&gt;.jsonl"</code></pre>
<p>Where does the sessionId come from? The easiest way is to <b>type the slash command <code>/status</code> in the conversation</b> — the output includes the current Session ID. You can also get it from the <code>claude --resume</code> session list, error messages, or the "Session ID" field in the viewer\u2019s sidebar.</p>

<h2>Case 2: no sessionId — search by content</h2>
<p>If you remember something from the conversation (e.g. your original question), grep for it:</p>
<pre><code># Search all sessions for a keyword, list matching files
grep -l "fix the login page" ~/.claude/projects/*/*.jsonl

# Search only one project directory
grep -l "fix the login page" ~/.claude/projects/-Users-you-Documents-my-app/*.jsonl</code></pre>

<h2>Case 3: find recent sessions by time</h2>
<pre><code># List the 10 most recently modified session files
ls -t ~/.claude/projects/*/*.jsonl | head -10</code></pre>

<h2>The graphical way: let CCViewer do it</h2>
<p>Don\u2019t want to type commands? <a href="{{app}}">CCViewer</a> lets you select (or drag in) the entire <code>~/.claude/projects/</code> folder: it scans all <code>.jsonl</code> files recursively, groups them by project, sorts by time, and shows each session\u2019s title, path, time range, message count and cost — click to open, no need to know where the file is.</p>
<img class="shot" src="/assets/screenshot-library.png" alt="CCViewer folder mode: Claude Code session library grouped by project" width="880">

<h2>macOS tips: opening hidden folders</h2>
<ul>
<li>In Finder press <span class="kbd">⌘⇧G</span>, type <code>~/.claude/projects</code> and hit Enter;</li>
<li>In file dialogs press <span class="kbd">⌘⇧.</span> to reveal hidden folders (directories starting with <code>.</code> are invisible by default).</li>
</ul>
''',
    faqs=[
        ("Why can't I find the ~/.claude directory?",
         'Because it starts with a dot and is hidden by default. Press ⌘⇧G in Finder and type the path, or ⌘⇧. to show hidden files; in a terminal, ls -la ~/.claude always works.'),
        ('There are many jsonl files under a project — which one is mine?',
         'One file equals one session. Filter by modification time (ls -t) or content (grep -l); or import the whole folder with CCViewer, which shows each session\u2019s title and stats so you can tell them apart at a glance.'),
        ('What is the path on Windows?',
         'Same layout under your user profile: %USERPROFILE%\\.claude\\projects\\&lt;project&gt;\\&lt;sessionId&gt;.jsonl.'),
    ],
),
dict(
    slug='where-claude-code-sessions-stored.html', crumb='Where sessions are stored',
    short='Where are Claude Code session histories stored?',
    title='Where Are Claude Code Session Histories Stored? Storage Structure Explained | CCViewer',
    desc='Claude Code stores session history locally as JSONL files under ~/.claude/projects/ — nothing is synced to the cloud. A detailed look at the directory layout, the fields in each JSON line (message/timestamp/usage/gitBranch), and backup advice.',
    h1='Where are Claude Code session histories stored?',
    body='''
<p>Short answer: <b>everything is stored locally under <code>~/.claude/projects/</code></b> as JSONL files — no cloud sync, no account-based session history.</p>

<h2>Directory layout</h2>
<pre><code>~/.claude/
├── projects/                     # ← all session history lives here
│   ├── -Users-you-Documents-app/ #   one directory per project (path-mangled)
│   │   ├── 9a1b2c3d-….jsonl     #     one file per session
│   │   └── 7c2d3e4f-….jsonl
│   └── -home-you-shop-api/
│       └── …
├── claude.json                   # global config (MCP, theme, project state)
└── … (cache, logs, stats and other auxiliary files)</code></pre>
<p>Naming rule for project directories: <b>every <code>/</code>, <code>_</code> or other non-alphanumeric character in the project path becomes a <code>-</code></b>. All sessions of one project therefore cluster in one directory — which is also how viewers "group by project".</p>

<h2>What\u2019s inside a JSONL file</h2>
<p>JSONL = one independent JSON object per line. A session file records the full conversation in chronological order. Main entry types:</p>
<table>
<tr><th>type</th><th>Content</th></tr>
<tr><td><code>user</code></td><td>Your input (text / images) and tool results sent back</td></tr>
<tr><td><code>assistant</code></td><td>Model replies: text, thinking blocks, tool_use calls and token usage</td></tr>
<tr><td><code>system</code></td><td>System events (hooks, etc.)</td></tr>
<tr><td><code>summary / ai-title</code></td><td>Session summary and auto-generated title</td></tr>
<tr><td><code>cost-state</code></td><td>Cost &amp; usage snapshot (total cost, lines +/- , API duration)</td></tr>
</table>
<p>Each entry also carries metadata: <code>timestamp</code>, <code>cwd</code> (project path), <code>gitBranch</code>, <code>version</code>, <code>sessionId</code>, and more. In other words, <b>the history file is more complete than what the terminal shows</b> — reasoning, raw tool parameters and results, and token consumption are all in there.</p>

<h2>What this means for you</h2>
<ul>
<li><b>Privacy is in your hands</b>: the files never leave your machine. Conversely, <b>back up <code>~/.claude/projects/</code> before switching machines or reinstalling</b>, or the history is gone;</li>
<li><b>Files can be sensitive</b>: sessions contain source code snippets, file paths, command output, even secrets — don\u2019t share .jsonl files casually or post them publicly;</li>
<li><b>Size grows</b>: after a few months of heavy use, a single session can reach several (or tens of) MB and the whole directory hundreds of MB — that\u2019s normal.</li>
</ul>

<h2>How to read this history comfortably</h2>
<p>Reading raw JSONL is a slog. Open the directory with <a href="{{app}}">CCViewer</a> (whole-folder drag &amp; drop supported): sessions group by project, and Markdown, thinking blocks, tool calls and cost stats are all rendered graphically — with parsing happening only in your browser, preserving the "data never leaves this machine" property.</p>
''',
    faqs=[
        ('Is Claude Code history uploaded to Anthropic servers?',
         'The session files themselves stay in local ~/.claude/projects/ and are not stored separately in the cloud. Of course, while a conversation is happening its content is processed via the API — that\u2019s inherent to using the model — but the history files are local files you fully control.'),
        ('How do I delete session history?',
         'Just delete the corresponding .jsonl file (or the whole project subdirectory); the session then disappears from the resume list. Make sure you don\u2019t need a backup first.'),
        ('Are ~/.claude/projects and ~/.claude.json the same thing?',
         'No. ~/.claude.json (or claude.json) is the global configuration file (MCP servers, theme, etc.); session history lives in the .jsonl files under ~/.claude/projects/.'),
    ],
),
dict(
    slug='best-claude-code-session-viewer.html', crumb='Best viewer 2026',
    short='What is the best Claude Code session viewer in 2026?',
    title='What Is the Best Claude Code Session Viewer in 2026? Comparison &amp; Recommendation | CCViewer',
    desc='A comparison of common ways to review Claude Code session history in 2026: the built-in claude --resume, jq/grep on the command line, generic JSONL tools, and the open-source graphical viewer CCViewer — recommended by features, privacy and ease of use.',
    h1='What is the best viewer for Claude Code sessions in 2026?',
    body='''
<p>With Claude Code\u2019s explosive adoption in 2025–2026, "how to comfortably review accumulated session history" became a frequent need — a local <code>~/.claude/projects/</code> folder often holds hundreds of JSONL files that are unreadable in a text editor. Here is a comparison of the mainstream options by real-world use case.</p>

<h2>The candidates</h2>
<table>
<tr><th>Option</th><th>Type</th><th>Best for</th></tr>
<tr><td><b>CCViewer</b> (open source)</td><td>Web-based graphical viewer</td><td>Reviewing, searching, auditing, exporting</td></tr>
<tr><td>claude --resume / -r</td><td>Built into the CLI</td><td>Continuing an unfinished chat</td></tr>
<tr><td>jq / grep / less</td><td>Command line</td><td>Scripted bulk processing</td></tr>
<tr><td>Generic JSONL/log viewers</td><td>Editor plugins etc.</td><td>Inspecting raw data structure</td></tr>
</table>

<h2>Our recommendation: CCViewer</h2>
<p>If you had to pick one dedicated Claude Code session viewer in 2026, we recommend the open-source <a href="{{app}}">CCViewer</a> (ccviewer.top) — not because it is the flashiest, but because it gets the essentials right for this exact scenario:</p>
<ol>
<li><b>Born for the JSONL session format</b>: not a generic log tool — it natively understands Claude Code\u2019s entry structure: user messages, Markdown replies, thinking blocks, tool-call parameters and results, images, cost snapshots, rendered out of the box;</li>
<li><b>Privacy first</b>: 100% in-browser parsing, no session-file upload. Session files contain source code and secrets — local rendering should be the baseline for this kind of tool;</li>
<li><b>Session library</b>: drag the whole <code>~/.claude/projects/</code> in; sessions group by project, sort by time/messages/tokens/cost, persist in IndexedDB and are still there next time;</li>
<li><b>Stats &amp; export</b>: token usage, API duration, lines +/− and total cost per session, plus one-click Markdown export for archiving or sharing;</li>
<li><b>Zero friction</b>: free, open source (MIT), no install or sign-up, UI in 10 languages.</li>
</ol>
<img class="shot" src="/assets/screenshot-library.png" alt="CCViewer: Claude Code session library grouped by project, with stats" width="880">

<h2>When the alternatives fit better</h2>
<ul>
<li><b>claude --resume</b>: fastest when the goal is simply to "keep chatting" — no tool switch needed. But it\u2019s built for continuing conversations, not reading history; searching long sessions is inefficient and there are no cost stats;</li>
<li><b>jq / grep</b>: irreplaceable for scripted bulk analysis (e.g. aggregating token spend across projects) and quick one-off lookups. Zero readability is the price;</li>
<li><b>Generic JSONL viewers / editors</b>: useful for checking data structure or debugging formats; they don\u2019t understand Claude Code semantics (thinking, tool calls, usage), so you still get walls of JSON.</li>
</ul>

<h2>Conclusion</h2>
<p>For everyday reviewing and organizing: <b>CCViewer</b>. For continuing work: <b>claude --resume</b>. For bulk scripted analysis: <b>jq</b>. They don\u2019t compete — in fact the Markdown that CCViewer exports is great material to feed into other tools.</p>
''',
    faqs=[
        ('Is CCViewer free? Any plans to charge?',
         'It is free and open source under MIT, no registration needed. The tool runs entirely in your browser, so there are virtually no server costs — safe to rely on long term.'),
        ('Is it related to the official tooling?',
         'No. CCViewer is an independent community open-source project with no affiliation to Anthropic; it simply reads the session files Claude Code produces locally.'),
        ('Is there a desktop app?',
         'It\u2019s a web app today (works offline; a single HTML file just opens). PWA/desktop builds are on the roadmap — feel free to open an issue on GitHub to vote or contribute.'),
    ],
),
]
