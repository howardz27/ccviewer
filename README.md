<p align="center">
  <img src="assets/logo.svg" width="110" alt="CCViewer logo">
</p>

# CCViewer — Claude Code Session Viewer

**[中文文档](README.zh-CN.md)**

A free, open-source viewer for [Claude Code](https://claude.com/claude-code) session files. Drop a `.jsonl` history file (or a whole project folder) into your browser and replay any conversation — Markdown, thinking blocks, tool calls, token usage and cost, all rendered locally.

> **Client-side viewer.** Session files are parsed, rendered and stored locally in the browser. The hosted site automatically loads Microsoft Clarity for page analytics and recordings. Offline copies do not load analytics.

**Try it online:** [CCViewer](https://ccviewer.top/claude-code-session-viewer/)

## Guides and sample

- [Read and export session history](https://ccviewer.top/claude-code-session-viewer/how-to-view-claude-code-session-history)
- [Find JSONL files on macOS, Linux and Windows](https://ccviewer.top/claude-code-session-viewer/find-claude-code-session-jsonl-file)
- [Understand storage and retention](https://ccviewer.top/claude-code-session-viewer/where-claude-code-sessions-stored)
- [Fictional JSONL sample](assets/example-session.jsonl) — reading fixture, not a resumable session

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
- 🔍 **Image preview** — enlarge images in the page; close with Escape, the close button or the backdrop
- 🔄 **Live refresh** — refresh manually or every 2 / 5 / 10 / 30 seconds while a session runs; appended messages preserve reading position and expanded content, and follow new output when you are at the bottom
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

Open the local source file or folder in a browser with file access support (such as Chrome / Edge) to enable automatic refresh. Cached sessions and pasted text are snapshots: click **Refresh** to reconnect the source file. Browsers without continuing file access require manually selecting the file again. Automatic refresh pauses when the page is hidden or the session library is open, and resumes when you return to the viewer.

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

The Cloudflare deployment uses extensionless guide URLs. `build.py` also regenerates the root `_redirects`, `sitemap.xml` and the optional `llms.txt` guide index; deploy these together with the HTML pages. To test the production routing locally, run `pnpm dlx wrangler@4.151.1 dev --local --port 8787`, then `python3 tests/check_routing.py --base http://127.0.0.1:8787`. Python's basic HTTP server is sufficient for the viewer but does not implement Cloudflare's extensionless guide routes. See [domain and redirect setup](docs/domain-routing.zh-CN.md) for DNS, HTTPS and GSC verification.

### Contributing

PRs are welcome. If you add or change UI text, update **all 10** language files (the build bakes every key; a missing key falls back to its raw name). Keep session parsing, rendering and storage in the browser, and keep the app dependency-free. Analytics configuration is shared across all generated pages.

## FAQ

**Where are my session files?** Claude Code stores them at `~/.claude/projects/<project>/<sessionId>.jsonl` (one JSON object per line).

**How is data processed?** Parsing, rendering and storage (IndexedDB) happen in your browser. The hosted site also sends page analytics and recordings to Microsoft Clarity.

## Disclaimer

CCViewer is an independent community project and is not affiliated with, endorsed by, or connected to Anthropic. "Claude Code" is a trademark of Anthropic, used here descriptively.

## License

[MIT](LICENSE)
