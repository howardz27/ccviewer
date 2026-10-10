# CCViewer — Claude Code Session Viewer

**[中文文档](README.zh-CN.md)**

A free, open-source viewer for [Claude Code](https://claude.com/claude-code) session files. Drop a `.jsonl` history file (or a whole project folder) into your browser and replay any conversation — Markdown, thinking blocks, tool calls, token usage and cost, all rendered locally.

> 🔒 **100% client-side.** No upload, no API calls, no telemetry. Your session files never leave your computer — they contain your code, file paths and sometimes secrets, which is exactly why this tool exists.

**Try it online:** <https://ccviewer.top> (the site serves the exact same code as this repo)

## Features

- 📁 **Session library** — import an entire folder (e.g. `~/.claude/projects/`), sessions persist in IndexedDB, grouped by project, sortable by recency / messages / tokens / cost
- 💬 **Full-fidelity rendering** — Markdown (code blocks, tables, lists), collapsible extended thinking, tool-call inputs & results, images
- 📊 **Usage & cost stats** — input/output/cache tokens, API duration, lines +/−, total cost per session
- 🌍 **10 languages** — English, 中文, 日本語, 한국어, Español, Français, Deutsch, Português, Русский, हिन्दी
- 📤 **Export to Markdown** — turn any session into a shareable `.md` document
- 🪶 **Zero dependencies** — one HTML file, no framework, no build required to *use* (only to rebuild)

## Usage

### Just open it

Download `claude-code-session-viewer/index.html` and open it in your browser. That's it — it works offline from `file://`.

### Or run locally

```bash
python3 -m http.server 8765 -d claude-code-session-viewer
# open http://localhost:8765
```

### Deploy your own

The site is a set of static files — any static host works:

- **Cloudflare Pages / Workers** — a `wrangler.jsonc` is included
- **GitHub Pages** — point it at the `claude-code-session-viewer/` directory
- **Anything else** — upload the `claude-code-session-viewer/` folder

## Development

The entire app lives in a single source file: `claude-code-session-viewer/src/template.html`. UI strings live in `claude-code-session-viewer/src/i18n/*.json` (10 languages).

```bash
python3 claude-code-session-viewer/build.py   # bakes i18n into static HTML pages
```

CI runs this build on every PR, so a broken build shows up as a red ✗ before merge.

### Contributing

PRs are welcome. If you add or change UI text, update **all 10** language files (the build bakes every key; a missing key falls back to its raw name). Keep the app dependency-free and 100% client-side — code that sends data anywhere will not be merged.

## FAQ

**Where are my session files?** Claude Code stores them at `~/.claude/projects/<project>/<sessionId>.jsonl` (one JSON object per line).

**Is anything uploaded?** No. Parsing, rendering and storage (IndexedDB) all happen in your browser. You can verify by opening DevTools → Network with the page open.

## Disclaimer

CCViewer is an independent community project and is not affiliated with, endorsed by, or connected to Anthropic. "Claude Code" is a trademark of Anthropic, used here descriptively.

## License

[MIT](LICENSE)
