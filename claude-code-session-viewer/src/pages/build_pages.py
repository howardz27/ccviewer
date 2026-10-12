#!/usr/bin/env python3
"""CCViewer SEO 内容页生成器（多语言）。
用法: python3 src/pages/build_pages.py
内容源: src/pages/content/<lang>.py（每语言定义 PAGES 列表）
输出: en -> <root>/<slug>.html，其余 -> <lang>/<slug>.html
"""
import json, os, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
SITE = 'https://ccviewer.top/claude-code-session-viewer'
GH = 'https://github.com/howardz27/ccviewer'
DATE = '2026-10-12'
LANGS = ['en','zh','ja','ko','es','fr','de','pt','ru','hi']

P1 = 'how-to-view-claude-code-session-history.html'
P2 = 'find-claude-code-session-jsonl-file.html'
P3 = 'where-claude-code-sessions-stored.html'
P4 = 'best-claude-code-session-viewer.html'
SLUGS = [P1, P2, P3, P4]

OG_LOCALE = {'en':'en_US','zh':'zh_CN','ja':'ja_JA','ko':'ko_KR','es':'es_ES',
             'fr':'fr_FR','de':'de_DE','pt':'pt_BR','ru':'ru_RU','hi':'hi_IN'}
HTML_LANG = {'en':'en','zh':'zh-CN','ja':'ja','ko':'ko','es':'es','fr':'fr',
             'de':'de','pt':'pt-BR','ru':'ru','hi':'hi'}

UI = {
 'zh': dict(help='帮助中心', updated='更新于', applies='适用于 Claude Code 2.x',
   cta_t='用 CCViewer 图形化回放你的 Claude Code 会话',
   cta_b='打开网页，把 <code>.jsonl</code> 文件或整个 <code>~/.claude/projects/</code> 文件夹拖进去即可 —— Markdown 渲染、思考块、工具调用、Token 与费用统计，全程在你的浏览器本地完成，不上传任何数据。',
   open='打开 CCViewer（免费、无需安装）', src='查看源码', faq='常见问题', rel='相关阅读',
   foot='© 2026 CCViewer · MIT 开源 · 与 Anthropic 无隶属关系，"Claude Code" 是 Anthropic 的商标，此处为描述性使用'),
 'en': dict(help='Help Center', updated='Updated', applies='Applies to Claude Code 2.x',
   cta_t='Replay your Claude Code sessions visually with CCViewer',
   cta_b='Open the page and drop in a <code>.jsonl</code> file — or the whole <code>~/.claude/projects/</code> folder. Markdown rendering, thinking blocks, tool calls, token &amp; cost stats, all processed locally in your browser. Nothing is ever uploaded.',
   open='Open CCViewer (free, no install)', src='View source', faq='FAQ', rel='Related guides',
   foot='© 2026 CCViewer · MIT open source · Not affiliated with Anthropic. "Claude Code" is an Anthropic trademark, used descriptively.'),
 'ja': dict(help='ヘルプセンター', updated='更新日', applies='Claude Code 2.x 対応',
   cta_t='CCViewer で Claude Code セッションをビジュアルに再生',
   cta_b='ページを開いて <code>.jsonl</code> ファイル（または <code>~/.claude/projects/</code> フォルダ全体）をドロップするだけ。Markdown レンダリング、思考ブロック、ツール呼び出し、トークン・コスト統計まで、すべてブラウザ内のローカル処理で、データは送信されません。',
   open='CCViewer を開く（無料・インストール不要）', src='ソースを見る', faq='よくある質問', rel='関連記事',
   foot='© 2026 CCViewer · MIT オープンソース · Anthropic とは提携関係にありません。「Claude Code」は Anthropic の商標です。'),
 'ko': dict(help='도움말 센터', updated='업데이트', applies='Claude Code 2.x 대응',
   cta_t='CCViewer로 Claude Code 세션을 시각적으로 재생하기',
   cta_b='페이지를 열고 <code>.jsonl</code> 파일 또는 <code>~/.claude/projects/</code> 폴더 전체를 끌어다 놓기만 하면 됩니다. Markdown 렌더링, 사고 블록, 도구 호출, 토큰·비용 통계가 모두 브라우저에서 로컬로 처리되며 어떤 데이터도 업로드되지 않습니다.',
   open='CCViewer 열기(무료, 설치 불필요)', src='소스 보기', faq='자주 묻는 질문', rel='관련 글',
   foot='© 2026 CCViewer · MIT 오픈소스 · Anthropic와는 무관합니다. "Claude Code"는 Anthropic의 상표입니다.'),
 'es': dict(help='Centro de ayuda', updated='Actualizado', applies='Aplica a Claude Code 2.x',
   cta_t='Reproduce tus sesiones de Claude Code visualmente con CCViewer',
   cta_b='Abre la página y suelta un archivo <code>.jsonl</code> — o la carpeta <code>~/.claude/projects/</code> completa. Markdown, bloques de pensamiento, llamadas a herramientas y estadísticas de tokens y coste, todo se procesa localmente en tu navegador. Nada se sube.',
   open='Abrir CCViewer (gratis, sin instalación)', src='Ver código', faq='Preguntas frecuentes', rel='Guías relacionadas',
   foot='© 2026 CCViewer · código abierto MIT · Sin afiliación con Anthropic. "Claude Code" es una marca de Anthropic, usada de forma descriptiva.'),
 'fr': dict(help="Centre d'aide", updated='Mis à jour', applies='Concerne Claude Code 2.x',
   cta_t='Rejouez vos sessions Claude Code visuellement avec CCViewer',
   cta_b='Ouvrez la page et déposez un fichier <code>.jsonl</code> — ou tout le dossier <code>~/.claude/projects/</code>. Rendu Markdown, blocs de réflexion, appels d\u2019outils, statistiques de tokens et de coûts : tout se passe localement dans votre navigateur, rien n\u2019est envoyé.',
   open='Ouvrir CCViewer (gratuit, sans installation)', src='Voir le code', faq='FAQ', rel='Guides liés',
   foot='© 2026 CCViewer · open source MIT · Sans affiliation avec Anthropic. « Claude Code » est une marque d\u2019Anthropic, utilisée à titre descriptif.'),
 'de': dict(help='Hilfe-Center', updated='Aktualisiert', applies='Gilt für Claude Code 2.x',
   cta_t='Claude-Code-Sessions visuell mit CCViewer wiedergeben',
   cta_b='Seite öffnen und eine <code>.jsonl</code>-Datei — oder den ganzen Ordner <code>~/.claude/projects/</code> — hineinziehen. Markdown-Rendering, Thinking-Blöcke, Tool-Aufrufe, Token- und Kostenstatistiken: alles läuft lokal im Browser, nichts wird hochgeladen.',
   open='CCViewer öffnen (kostenlos, ohne Installation)', src='Quellcode ansehen', faq='Häufige Fragen', rel='Verwandte Artikel',
   foot='© 2026 CCViewer · MIT Open Source · Keine Verbindung zu Anthropic. „Claude Code“ ist eine Marke von Anthropic, rein beschreibend verwendet.'),
 'pt': dict(help='Central de Ajuda', updated='Atualizado', applies='Aplica-se ao Claude Code 2.x',
   cta_t='Releia visualmente suas sessões do Claude Code com o CCViewer',
   cta_b='Abra a página e arraste um arquivo <code>.jsonl</code> — ou a pasta <code>~/.claude/projects/</code> inteira. Markdown, blocos de raciocínio, chamadas de ferramentas e estatísticas de tokens e custo, tudo processado localmente no navegador. Nada é enviado.',
   open='Abrir o CCViewer (grátis, sem instalação)', src='Ver código-fonte', faq='Perguntas frequentes', rel='Guias relacionados',
   foot='© 2026 CCViewer · código aberto MIT · Sem afiliação com a Anthropic. "Claude Code" é marca da Anthropic, usada de forma descritiva.'),
 'ru': dict(help='Центр справки', updated='Обновлено', applies='Подходит для Claude Code 2.x',
   cta_t='Визуально воспроизводите сессии Claude Code с CCViewer',
   cta_b='Откройте страницу и перетащите файл <code>.jsonl</code> — или всю папку <code>~/.claude/projects/</code>. Markdown, блоки размышлений, вызовы инструментов, статистика токенов и расходов — всё обрабатывается локально в браузере, ничего не отправляется.',
   open='Открыть CCViewer (бесплатно, без установки)', src='Исходный код', faq='Частые вопросы', rel='Похожие статьи',
   foot='© 2026 CCViewer · open source MIT · Не аффилировано с Anthropic. «Claude Code» — товарный знак Anthropic, используется описательно.'),
 'hi': dict(help='सहायता केंद्र', updated='अपडेट', applies='Claude Code 2.x के लिए',
   cta_t='CCViewer से अपने Claude Code सत्र विज़ुअली रीप्ले करें',
   cta_b='पेज खोलें और कोई <code>.jsonl</code> फ़ाइल — या पूरा <code>~/.claude/projects/</code> फ़ोल्डर — ड्रैप कर दें। Markdown रेंडरिंग, थिंकिंग ब्लॉक, टूल कॉल, टोकन व लागत आँकड़े सब आपके ब्राउज़र में लोकल चलते हैं, कुछ भी अपलोड नहीं होता।',
   open='CCViewer खोलें (नि:शुल्क, इंस्टॉल ज़रूरी नहीं)', src='सोर्स देखें', faq='सामान्य प्रश्न', rel='संबंधित लेख',
   foot='© 2026 CCViewer · MIT ओपन सोर्स · Anthropic से कोई संबंध नहीं। "Claude Code" Anthropic का ट्रेडमार्क है, वर्णनात्मक उपयोग।'),
}

CSS = """
:root{--bg:#0d1117;--panel:#161b22;--panel2:#1c2128;--border:#30363d;--text:#e6edf3;
--dim:#8b949e;--faint:#6e7681;--accent:#d97757;--accent2:#cc9b7a;--user:#58a6ff;--code-bg:#0b0f14}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-size:15px;line-height:1.8;
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}
code,kbd{font-family:"SFMono-Regular",Consolas,Menlo,monospace}
header.nav{display:flex;align-items:center;gap:10px;padding:12px 20px;background:var(--panel);
border-bottom:1px solid var(--border);position:sticky;top:0;z-index:5}
header.nav .brand{display:flex;align-items:center;gap:9px;font-weight:700;color:var(--accent);
text-decoration:none;font-size:15px}
header.nav .sp{flex:1}
header.nav a.gh{color:var(--text);text-decoration:none;font-size:13px;border:1px solid var(--border);
background:var(--panel2);padding:5px 11px;border-radius:6px}
header.nav a.gh:hover{border-color:var(--accent);color:var(--accent)}
main{max-width:820px;margin:0 auto;padding:36px 20px 64px}
.crumbs{font-size:12.5px;color:var(--faint);margin-bottom:14px}
.crumbs a{color:var(--dim);text-decoration:none}
.crumbs a:hover{color:var(--accent)}
h1{font-size:27px;line-height:1.4;margin:0 0 10px}
.meta{color:var(--faint);font-size:12.5px;margin-bottom:26px;padding-bottom:18px;border-bottom:1px solid var(--border)}
h2{font-size:19px;margin:34px 0 10px;color:var(--accent2)}
h3{font-size:16px;margin:24px 0 8px}
p{margin:10px 0}
a{color:var(--user)}
ul,ol{padding-left:24px}
li{margin:5px 0}
code{background:var(--code-bg);border:1px solid var(--border);border-radius:4px;padding:1px 6px;font-size:13px;color:var(--accent2)}
pre{background:var(--code-bg);border:1px solid var(--border);border-radius:8px;padding:14px 16px;overflow:auto}
pre code{background:none;border:none;padding:0;color:var(--text);font-size:13px}
table{border-collapse:collapse;margin:14px 0;width:100%;font-size:13.5px}
th,td{border:1px solid var(--border);padding:7px 11px;text-align:left}
th{background:var(--panel2);color:var(--accent2)}
img.shot{max-width:100%;border:1px solid var(--border);border-radius:10px;margin:12px 0;
box-shadow:0 14px 44px rgba(0,0,0,.4)}
.cta{background:linear-gradient(120deg,rgba(217,119,87,.13),rgba(191,227,239,.05));
border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:12px;
padding:18px 22px;margin:30px 0}
.cta b{color:var(--accent)}
.cta .btns{margin-top:12px;display:flex;gap:10px;flex-wrap:wrap}
.btn{display:inline-block;background:var(--panel2);color:var(--text);border:1px solid var(--border);
padding:8px 16px;border-radius:6px;text-decoration:none;font-size:14px}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn.primary{background:var(--accent);color:#1a1109;border-color:var(--accent);font-weight:600}
.btn.primary:hover{opacity:.9;color:#1a1109}
details{border:1px solid var(--border);border-radius:10px;background:var(--panel);margin:9px 0}
summary{cursor:pointer;padding:11px 16px;font-weight:500;list-style:none}
summary::-webkit-details-marker{display:none}
summary::before{content:'\\25B8 ';color:var(--accent)}
details[open] summary::before{content:'\\25BE '}
details .a{padding:0 16px 13px;color:var(--dim);font-size:14px}
.related{margin-top:44px;padding-top:22px;border-top:1px solid var(--border)}
.related h3{margin:0 0 10px;font-size:14px;color:var(--faint);text-transform:uppercase;letter-spacing:.5px}
.related a{display:block;padding:7px 0;color:var(--dim);text-decoration:none;font-size:14.5px}
.related a:hover{color:var(--accent)}
footer{border-top:1px solid var(--border);padding:20px;color:var(--faint);font-size:12.5px;text-align:center}
footer a{color:var(--dim)}
.kbd{background:var(--panel2);border:1px solid var(--border);border-radius:4px;padding:0 5px;font-size:12px}
"""

SHELL = """<!DOCTYPE html>
<html lang="{{html_lang}}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{title}}</title>
<meta name="description" content="{{desc}}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{{url}}">
{{hreflang}}
<meta property="og:type" content="article">
<meta property="og:site_name" content="CCViewer">
<meta property="og:title" content="{{title}}">
<meta property="og:description" content="{{desc}}">
<meta property="og:url" content="{{url}}">
<meta property="og:locale" content="{{og_locale}}">
<meta property="og:image" content="https://ccviewer.top/assets/screenshot-viewer.png">
<link rel="icon" type="image/svg+xml" href="/assets/logo.svg">
<script type="application/ld+json">{{ld_article}}</script>
<script type="application/ld+json">{{ld_breadcrumb}}</script>
<script type="application/ld+json">{{ld_faq}}</script>
<style>__CSS__</style>
</head>
<body>
<header class="nav">
  <a class="brand" href="{{app}}"><img src="/assets/logo.svg" width="26" alt="CCViewer logo">CCViewer</a>
  <span class="sp"></span>
  <a class="gh" href="{{gh}}" target="_blank" rel="noopener">GitHub</a>
</header>
<main>
<div class="crumbs"><a href="{{app}}">CCViewer</a> / <a href="{{app}}">{{help}}</a> / {{crumb}}</div>
<article>
<h1>{{h1}}</h1>
<div class="meta">{{updated}} {{date}} · CCViewer {{help}} · {{applies}}</div>
{{body}}
<div class="cta">
  <b>{{cta_t}}</b><br>
  {{cta_b}}
  <div class="btns">
    <a class="btn primary" href="{{app}}">{{open}}</a>
    <a class="btn" href="{{gh}}" target="_blank" rel="noopener">{{src}}</a>
  </div>
</div>
{{faq}}
<div class="related">
<h3>{{rel}}</h3>
{{related}}
</div>
</article>
</main>
<footer>{{foot}}</footer>
</body>
</html>
"""


def load_content(lang):
    path = os.path.join(HERE, 'content', f'{lang}.py')
    spec = importlib.util.spec_from_file_location(f'content_{lang}', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PAGES


def page_url(lang, slug):
    return f'{SITE}/{slug}' if lang == 'en' else f'{SITE}/{lang}/{slug}'


def app_url(lang):
    return f'{SITE}/' if lang == 'en' else f'{SITE}/{lang}/'


def render(lang):
    ui = UI[lang]
    pages = load_content(lang)
    by_slug = {p['slug']: p for p in pages}
    out_dir = ROOT if lang == 'en' else os.path.join(ROOT, lang)
    os.makedirs(out_dir, exist_ok=True)
    for pg in pages:
        slug = pg['slug']
        url = page_url(lang, slug)
        hreflang = '\n'.join(
            f'<link rel="alternate" hreflang="{l}" href="{page_url(l, slug)}">' for l in LANGS
        ) + f'\n<link rel="alternate" hreflang="x-default" href="{page_url("en", slug)}">'
        article_ld = json.dumps({
            '@context': 'https://schema.org', '@type': 'Article',
            'headline': pg['h1'], 'description': pg['desc'],
            'datePublished': DATE, 'dateModified': DATE,
            'inLanguage': HTML_LANG[lang],
            'image': 'https://ccviewer.top/assets/screenshot-viewer.png',
            'author': {'@type': 'Organization', 'name': 'CCViewer', 'url': SITE},
            'publisher': {'@type': 'Organization', 'name': 'CCViewer', 'url': SITE},
            'mainEntityOfPage': url,
        }, ensure_ascii=False)
        crumb_ld = json.dumps({
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'CCViewer', 'item': app_url(lang)},
                {'@type': 'ListItem', 'position': 2, 'name': pg['h1'], 'item': url},
            ],
        }, ensure_ascii=False)
        faq_ld = json.dumps({
            '@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [
                {'@type': 'Question', 'name': q,
                 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                for q, a in pg['faqs']
            ],
        }, ensure_ascii=False)
        faq_html = f'<h2 id="faq">{ui["faq"]}</h2>' + ''.join(
            f'<details><summary>{q}</summary><div class="a">{a}</div></details>'
            for q, a in pg['faqs']
        )
        related = ''.join(
            f'<a href="{s}">{by_slug[s]["short"]}</a>' for s in SLUGS if s in by_slug
        )
        body = pg['body'].replace('{{app}}', app_url(lang))
        page = (SHELL.replace('__CSS__', CSS)
                .replace('{{html_lang}}', HTML_LANG[lang])
                .replace('{{title}}', pg['title'])
                .replace('{{desc}}', pg['desc'])
                .replace('{{url}}', url)
                .replace('{{hreflang}}', hreflang)
                .replace('{{og_locale}}', OG_LOCALE[lang])
                .replace('{{h1}}', pg['h1'])
                .replace('{{crumb}}', pg['crumb'])
                .replace('{{help}}', ui['help'])
                .replace('{{updated}}', ui['updated'])
                .replace('{{applies}}', ui['applies'])
                .replace('{{date}}', DATE)
                .replace('{{body}}', body)
                .replace('{{cta_t}}', ui['cta_t'])
                .replace('{{cta_b}}', ui['cta_b'])
                .replace('{{open}}', ui['open'])
                .replace('{{src}}', ui['src'])
                .replace('{{faq}}', faq_html)
                .replace('{{rel}}', ui['rel'])
                .replace('{{related}}', related)
                .replace('{{app}}', app_url(lang))
                .replace('{{gh}}', GH)
                .replace('{{ld_article}}', article_ld)
                .replace('{{ld_breadcrumb}}', crumb_ld)
                .replace('{{ld_faq}}', faq_ld)
                .replace('{{foot}}', ui['foot']))
        out = os.path.join(out_dir, slug)
        open(out, 'w', encoding='utf-8').write(page)
        print('built', os.path.normpath(out))


def build():
    for lang in LANGS:
        render(lang)
    print('done.')


if __name__ == '__main__':
    build()
