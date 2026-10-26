# -*- coding: utf-8 -*-
PAGES = [
dict(
    slug='how-to-view-claude-code-session-history.html',
    crumb='View full history',
    short='How to View Claude Code Session History: 3 Methods',
    title='How to View Claude Code Session History: 3 Methods | CCViewer',
    desc='Read saved Claude Code JSONL sessions, resume work in the CLI, or inspect raw records. Includes a fictional sample, export steps and hosted/offline limitations.',
    h1='How to View Claude Code Session History: 3 Methods',
    body=r'''
<p>To read a saved Claude Code conversation, open its <code>.jsonl</code> transcript in CCViewer. To continue the work, use <code>claude --resume</code>. To inspect raw records or automate analysis, use a text editor or <code>jq</code>. A viewer can only show records present in the file.</p>
<h2>Read a session in the browser</h2>
<ol><li>Find a transcript under your Claude Code configuration directory, usually <code>~/.claude/projects/</code>.</li><li>Open <a href="{{app}}">CCViewer</a> and choose the file, paste JSONL text, or select a project folder.</li><li>Expand tool calls and thinking blocks, inspect the available usage fields, then export Markdown if you need a readable archive.</li></ol>
<p>Folder imports are stored in this browser's IndexedDB. Clearing site data can remove the imported library; keep the original files as a backup. Token totals reflect records in the file; cost snapshots, when present, are not a billing statement.</p>
<img class="shot" src="/assets/screenshot-viewer.png" alt="CCViewer displaying messages, tool calls and usage fields" width="880">
<h2>Continue a session in the terminal</h2>
<pre><code>claude --resume
claude --continue
claude --resume SESSION_ID</code></pre>
<p>Run these in the relevant project. Resume continues the conversation; CCViewer is a reader and does not send a new prompt to Claude. See the official session guide below for the current picker behavior.</p>
<h2>Inspect the original JSONL</h2>
<pre><code>jq -r 'select(.type == "user") | .message.content' session.jsonl</code></pre>
<p>Some user records contain tool results rather than a human prompt. Inspect the content type when scripting. A malformed line can cause jq to stop; keep an untouched copy before attempting repairs.</p>
<h2>Try a fictional sample</h2>
<p>Download the <a href="/assets/example-session.jsonl" download>synthetic JSONL sample</a>, then import it. It contains one prompt, a thinking block, fictional Read and Edit calls with results, and a Markdown reply. It contains no real conversation or credentials. The 2,150 input and 384 output tokens are illustrative values.</p>
<h2>Hosted and offline use</h2>
<p>Parsing and rendering happen locally. The hosted site automatically loads Microsoft Clarity for analytics and recordings. Remote images in a transcript can also cause requests. For disconnected use, download the HTML from the repository and open it with networking disabled; offline copies do not load Clarity.</p>
''',
    faqs=[('Can a viewer recover deleted messages?', 'No. A viewer can only render supported records that remain in the selected file.'), ('Is the hosted viewer network-free?', 'No. Processing is local, but the hosted site loads Microsoft Clarity analytics and recordings. Remote images may also make requests.')],
),
dict(
    slug='find-claude-code-session-jsonl-file.html',
    crumb='Find the JSONL file',
    short='Find Claude Code JSONL Files on macOS, Linux & Windows',
    title='Find Claude Code JSONL Files on macOS, Linux & Windows | CCViewer',
    desc='Locate Claude Code session JSONL files with macOS, Linux and PowerShell commands. Check custom config paths, WSL and missing transcripts.',
    h1='Find Claude Code JSONL Files on macOS, Linux & Windows',
    body=r'''
<p>Start in <code>~/.claude/projects/</code>, or the <code>projects</code> directory inside your custom <code>CLAUDE_CONFIG_DIR</code>. Search recursively rather than guessing a folder name. These instructions concern transcripts on the machine that ran the local session.</p>
<h2>macOS and Linux: list transcript files</h2>
<pre><code>session_root="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects"
find "$session_root" -type f -name '*.jsonl'
# Replace SESSION_ID with the identifier you already know.
find "$session_root" -type f -name 'SESSION_ID.jsonl'</code></pre>
<p>In macOS Finder, press Command–Shift–G and enter <code>~/.claude/projects/</code>. Use your custom configuration directory if set.</p>
<h2>Search by a remembered phrase</h2>
<pre><code>find "$session_root" -type f -name '*.jsonl' \
  -exec grep -lF -- 'fix the login page' {} +</code></pre>
<p>The command prints matching file names. It handles spaces in paths and searches text literally. Encoded text, images and missing transcripts will not necessarily match.</p>
<h2>Windows PowerShell: show recent files</h2>
<pre><code>$sessionRoot = if ($env:CLAUDE_CONFIG_DIR) {
  Join-Path $env:CLAUDE_CONFIG_DIR 'projects'
} else {
  Join-Path $env:USERPROFILE '.claude/projects'
}
Get-ChildItem -LiteralPath $sessionRoot -Filter *.jsonl -Recurse -File |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 10 FullName, LastWriteTime</code></pre>
<p>For a session run inside WSL, check that Linux environment's home directory instead of assuming the Windows profile contains it.</p>
<h2>If no file appears</h2>
<ul><li>Check the account, machine, container or remote environment where the session ran.</li><li>Check <code>CLAUDE_CONFIG_DIR</code>, hidden folders and directory permissions.</li><li>Check whether persistence was disabled or retention cleanup removed the transcript. A missing file cannot be recovered by importing the folder into a viewer.</li></ul>
<p>Once located, open the file in <a href="{{app}}">CCViewer</a>. For the distinction between prompt history and full transcripts, see the storage guide in Related guides.</p>
''',
    faqs=[('Why is the default folder empty?', 'Check the runtime environment, custom configuration path, disabled persistence and retention cleanup. The transcript may live on another machine.'), ('Can I import a folder?', 'Yes. CCViewer imports JSONL files into a local browser library grouped by project.')],
),
dict(
    slug='where-claude-code-sessions-stored.html',
    crumb='Where sessions are stored',
    short='Where Claude Code Sessions Are Stored: Paths & Retention',
    title='Where Claude Code Sessions Are Stored: Paths & Retention | CCViewer',
    desc='Understand local Claude Code transcripts, prompt history, config paths and retention. Learn what a JSONL viewer can read and what it cannot restore.',
    h1='Where Claude Code Sessions Are Stored: Paths & Retention',
    body=r'''
<p>For local Claude Code sessions, the default transcript location is <code>~/.claude/projects/&lt;project&gt;/&lt;session-id&gt;.jsonl</code>. A custom configuration directory changes the base path. This local layout is not a claim that all Claude Code interfaces or model requests stay on your machine.</p>
<h2>Transcript, prompt history and configuration</h2>
<table><tr><th>Default path</th><th>Purpose</th></tr><tr><td><code>~/.claude/projects/</code></td><td>Project transcripts and related project data</td></tr><tr><td><code>~/.claude/history.jsonl</code></td><td>Prompt history; not a replacement for a conversation transcript</td></tr><tr><td><code>~/.claude/settings.json</code></td><td>User settings</td></tr><tr><td><code>~/.claude.json</code></td><td>State/configuration outside the .claude directory</td></tr></table>
<p>On Windows, the default base is <code>%USERPROFILE%\.claude</code>. See the official directory documentation for environment and version differences.</p>
<h2>Records a viewer can read</h2>
<p>JSONL stores one JSON value per line. CCViewer recognizes user and assistant messages, tool calls and results, and some system and cost records. Fields such as <code>timestamp</code>, <code>sessionId</code>, <code>cwd</code> and <code>message.usage</code> may be present. The log is an evolving implementation format: every record is not guaranteed to contain every field.</p>
<h2>Retention and missing history</h2>
<p>Transcripts are not a permanent backup. Claude Code has retention settings and modes that disable persistence. Cleanup behavior can vary by version and interface; consult the application-data documentation for the applicable settings. Compaction and missing records also limit what can be reconstructed.</p>
<h2>Back up and read safely</h2>
<p>Copy the transcripts you need to an access-controlled backup before migrating or clearing data. They can contain source code, paths and command output. Keep original files even when importing into a browser library, which can be cleared by browser storage controls.</p>
<p><a href="{{app}}">CCViewer</a> reads the files locally. Its hosted site also loads Clarity analytics and recordings; a local transcript does not imply that the hosted viewer or Claude Code model calls are network-free.</p>
''',
    faqs=[('Is history.jsonl the full transcript?', 'No. Prompt history and project conversation transcripts serve different purposes.'), ('Does local storage mean Claude Code is offline?', 'No. Local transcript storage is separate from model requests and cloud or remote session features.')],
),
dict(
    slug='best-claude-code-session-viewer.html',
    crumb='Best viewer 2026',
    short='Claude Code Session Viewers Compared by Task',
    title='Claude Code Session Viewers Compared by Task | CCViewer',
    desc='Compare CCViewer, claude --resume, jq and text editors by task. A product-authored guide with a reproducible sample and clear feature and privacy limits.',
    h1='Claude Code Session Viewers Compared by Task',
    body=r'''
<p>The best method depends on the job: use CCViewer for visual reading and Markdown export, Claude Code's resume command to continue work, and jq or an editor for raw-data inspection. This guide is written by the CCViewer project; it is a product-authored comparison of workflows, not an independent ranking or benchmark.</p>
<h2>Choose by task</h2>
<table><tr><th>Task</th><th>Option</th><th>Boundary</th></tr><tr><td>Read messages and expand tool calls</td><td>CCViewer</td><td>Only supported records present in the imported file</td></tr><tr><td>Continue coding with existing context</td><td><code>claude --resume</code></td><td>Starts or continues a Claude Code interaction</td></tr><tr><td>Filter or aggregate records in scripts</td><td>jq / grep</td><td>Requires understanding the record structure</td></tr><tr><td>Inspect or repair malformed JSON</td><td>Text editor</td><td>Work on a copy of the original</td></tr></table>
<h2>What CCViewer currently does</h2>
<p>It renders Markdown, available thinking blocks and tool records, imports folders into a browser library, sorts sessions, and exports Markdown. The interface has 10 languages and the source is MIT licensed. It does not resume a Claude conversation, restore deleted logs or provide built-in full-text search across the library. Usage totals depend on the input records.</p>
<h2>Reproduce the comparison</h2>
<ol><li>Download the <a href="/assets/example-session.jsonl" download>fictional sample</a>.</li><li>Import it into <a href="{{app}}">CCViewer</a>. Check the user message, thinking block, tool calls, tool results and Markdown reply.</li><li>Open the same file in an editor and compare the visible text and 2,150/384 sample token counts.</li><li>Export Markdown and inspect the result. This synthetic file is for reading tests; do not use it as a resumable Claude Code session.</li></ol>
<h2>Privacy and practical limits</h2>
<p>The hosted site runs Clarity analytics and recordings. Offline copies do not load analytics. Remote transcript images may still request external URLs when connected. Large files can block the UI during parsing, and clearing browser storage removes the local library. Keep your source files and choose a disconnected offline copy when that matches your needs.</p>
''',
    faqs=[('Is this an independent review?', 'No. It is written by the CCViewer project and compares workflows, not an exhaustive list of products.'), ('Does CCViewer search across all sessions?', 'No built-in full-text search across the session library is currently provided. Use a text search tool for that task.')],
),
]
