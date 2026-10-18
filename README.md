<p align="center">
  <img src="assets/logo.svg" width="110" alt="CCViewer logo">
</p>

# CCViewer — Claude Code Session Viewer

**[中文文档](README.zh-CN.md)**

A free, open-source viewer for [Claude Code](https://claude.com/claude-code) session files. Drop a `.jsonl` history file (or a whole project folder) into your browser and replay any conversation — Markdown, thinking blocks, tool calls, token usage and cost, all rendered locally.

> 🔒 **100% client-side.** Session files are parsed and rendered locally without upload. The hosted site supports optional Microsoft Clarity analytics on public pages, loaded only after consent. Recording stops before local sessions are displayed. Offline copies do not load analytics. Your session files never leave your computer — they contain your code, file paths and sometimes secrets, which is exactly why this tool exists.

**Try it online:** <https://ccviewer.top> (the site serves the exact same code as this repo)

## Screenshots

| Landing | Session viewer |
|:---:|:---:|
| ![Landing page](assets/screenshot-landing.png) | ![Session viewer with thinking, tool calls and stats](assets/screenshot-viewer.png) |

*Landing page (left) and the viewer (right): user prompts, collapsible thinking blocks, tool calls, Markdown replies, plus per-session stats — tokens, duration, cost — in the sidebar.*

**Folder mode** — open a folder such as `~/.claude/projects/` and every session is imported, persisted in your browser (IndexedDB) and grouped by project in the sidebar:

![Folder mode: sessions grouped by project](assets/screenshot-library.png)

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

This builds all 60 localized application, help and guide pages. See [analytics setup](docs/analytics.md) for the optional Clarity configuration.

CI runs this build on every PR, so a broken build shows up as a red ✗ before merge.

The Cloudflare deployment uses extensionless guide URLs. `build.py` also regenerates the root `_redirects` and `sitemap.xml`; deploy these together with the HTML pages. To test the production routing locally, run `pnpm dlx wrangler@4.151.1 dev --local --port 8787`, then `python3 tests/check_routing.py --base http://127.0.0.1:8787`. Python's basic HTTP server is sufficient for the viewer but does not implement Cloudflare's extensionless guide routes. See [domain and redirect setup](docs/domain-routing.zh-CN.md) for DNS, HTTPS and GSC verification.

### Contributing

PRs are welcome. If you add or change UI text, update **all 10** language files (the build bakes every key; a missing key falls back to its raw name). Keep the app dependency-free and 100% client-side — session content must never be sent to analytics or any external service. Optional public-page analytics must retain consent controls and stop before local sessions are displayed.

## FAQ

**Where are my session files?** Claude Code stores them at `~/.claude/projects/<project>/<sessionId>.jsonl` (one JSON object per line).

**Is anything uploaded?** No. Parsing, rendering and storage (IndexedDB) all happen in your browser. You can verify by opening DevTools → Network with the page open.

## Disclaimer

CCViewer is an independent community project and is not affiliated with, endorsed by, or connected to Anthropic. "Claude Code" is a trademark of Anthropic, used here descriptively.

## License

[MIT](LICENSE)
