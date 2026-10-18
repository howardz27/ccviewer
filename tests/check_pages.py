"""Validate generated metadata, crawlable links and sitemap coverage."""
import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'claude-code-session-viewer'
assets = json.loads((ROOT / 'wrangler.jsonc').read_text())['assets']
assert assets['html_handling'] == 'auto-trailing-slash'
assert assets['not_found_handling'] == 'none'


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links, self.canonical, self.alternates, self.ld = [], [], [], []
        self.schema = False
        self.h1 = 0
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'h1':
            self.h1 += 1
        if tag == 'a':
            assert a.get('href'), 'Anchor missing crawlable href'
            self.links.append(a['href'])
            if a.get('target') == '_blank':
                assert 'noopener' in a.get('rel', '').split()
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a['href'])
        if tag == 'link' and a.get('rel') == 'alternate':
            self.alternates.append(a['href'])
        if tag == 'script':
            self.schema = a.get('type') == 'application/ld+json'

    def handle_endtag(self, tag):
        if tag == 'script':
            self.schema = False

    def handle_data(self, data):
        if self.schema:
            self.ld.append(json.loads(data))


pages = sorted(p for p in APP.rglob('*.html') if 'src' not in p.parts)
assert len(pages) == 60
canonicals = set()
for path in pages:
    source = path.read_text(encoding='utf-8')
    assert '{{' not in source and '__CONFIG__' not in source and '__STRINGS__' not in source, path
    p = Page(source)
    assert p.h1 == 1 and len(p.canonical) == 1 and len(p.alternates) == 11, path
    expected = 'https://ccviewer.top/' + str(path.relative_to(ROOT))
    expected = expected[:-10] if expected.endswith('index.html') else expected[:-5]
    assert p.canonical[0] == expected, (path, p.canonical)
    canonicals.add(p.canonical[0])
    assert p.ld and 'window.ccviewerAnalytics' in source, path
    for href in p.links + p.alternates + p.canonical:
        u = urlsplit(href)
        if u.scheme and u.netloc != 'ccviewer.top':
            continue
        assert not u.path.endswith('.html'), (path, 'Redirecting HTML link', href)
        target = ROOT / unquote(u.path).lstrip('/') if u.path.startswith('/') else path.parent / unquote(u.path)
        if target.is_dir():
            target /= 'index.html'
        elif not target.exists() and not target.suffix:
            target = target.with_suffix('.html')
        assert target.exists(), (path, href)
    if path.name == 'index.html':
        assert 'location.replace' not in source, 'No automatic language redirect'
    if path.parent.name == 'ja':
        assert 'ja_JA' not in source
sitemap = ET.parse(ROOT / 'sitemap.xml')
locations = {e.text for e in sitemap.findall('.//{*}loc')}
assert canonicals == locations, canonicals ^ locations
assert all(not urlsplit(url).path.endswith('.html') for url in locations)
redirects = {}
for line in (ROOT / '_redirects').read_text(encoding='utf-8').splitlines():
    if not line or line.startswith('#'):
        continue
    source, destination, status = line.split()
    assert status == '301' and source not in redirects
    redirects[source] = destination
    assert 'https://ccviewer.top' + destination in canonicals
for source, destination in redirects.items():
    assert destination not in redirects, (source, 'Redirect chain', destination)
assert redirects['/'] == '/claude-code-session-viewer/'
for url in canonicals:
    path = urlsplit(url).path
    assert path not in redirects, ('Canonical must return 200 directly', path)
    if not path.endswith('/'):
        assert redirects[path + '.html'] == path
assert 'http-equiv="refresh"' not in (ROOT / 'index.html').read_text()
assert 'location.replace' not in (ROOT / 'index.html').read_text()
print('Static pages: 60 pages, structured data, canonical/hreflang, local links and sitemap passed.')
