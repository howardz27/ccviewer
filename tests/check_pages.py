"""Validate generated metadata, crawlable links and sitemap coverage."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'claude-code-session-viewer'
sys.path.insert(0, str(APP))
from seo import attribute, json_ld

assert attribute('A "quote" &amp; <value>') == 'A &quot;quote&quot; &amp; &lt;value&gt;'
assert '</script>' not in json_ld({'text': '</script>'})
assets = json.loads((ROOT / 'wrangler.jsonc').read_text())['assets']
assert assets['html_handling'] == 'auto-trailing-slash'
assert assets['not_found_handling'] == 'none'


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links, self.canonical, self.alternates, self.ld = [], [], [], []
        self.schema = False
        self.h1 = 0
        self.meta, self.ids, self.dates, self.hreflangs = {}, set(), [], {}
        self.title, self.in_title = '', False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if 'id' in a:
            assert a['id'] not in self.ids, ('Duplicate anchor', a['id'])
            self.ids.add(a['id'])
        if tag == 'time':
            self.dates.append(a['datetime'])
        if tag == 'meta':
            key = a.get('name', a.get('property'))
            if key in ('description', 'robots', 'og:title', 'og:description', 'og:url'):
                assert key not in self.meta, ('Duplicate metadata', key)
                self.meta[key] = a['content']
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
            self.hreflangs[a['hreflang']] = a['href']
        if tag == 'script':
            self.schema = a.get('type') == 'application/ld+json'

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'script':
            self.schema = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.schema:
            self.ld.append(json.loads(data))


pages = sorted(p for p in APP.rglob('*.html') if 'src' not in p.parts)
assert len(pages) == 60
canonicals = set()
parsed = {}
titles = set()
for path in pages:
    source = path.read_text(encoding='utf-8')
    assert '{{' not in source and '__CONFIG__' not in source and '__STRINGS__' not in source, path
    p = Page(source)
    assert p.h1 == 1 and len(p.canonical) == 1 and len(p.alternates) == 11, path
    expected = 'https://ccviewer.top/' + str(path.relative_to(ROOT))
    expected = expected[:-10] if expected.endswith('index.html') else expected[:-5]
    assert p.canonical[0] == expected, (path, p.canonical)
    canonicals.add(p.canonical[0])
    parsed[expected] = p
    assert p.title.strip() and p.title not in titles, (path, 'Missing or duplicate title')
    titles.add(p.title)
    assert p.meta['description'] and p.meta['description'] == p.meta['og:description'], path
    assert p.meta['og:url'] == expected, path
    assert 'max-image-preview:large' in p.meta['robots'] and 'noindex' not in p.meta['robots'], path
    nodes = [node for data in p.ld for node in data.get('@graph', [data])]
    webpage = next(node for node in nodes if node.get('@id') == expected + '#webpage')
    assert webpage['url'] == expected and webpage['name'] == p.title, path
    article = next((node for node in nodes if node.get('@type') == 'Article'), None)
    if article:
        assert p.dates == [article['dateModified']], path
        assert article['datePublished'] <= article['dateModified'], path
        for citation in article.get('citation', []):
            assert citation in p.links, (path, 'Schema citation must be visible', citation)
    for href in p.links:
        if href.startswith('#'):
            assert href[1:] in p.ids, (path, 'Broken section anchor', href)
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
for entry in sitemap.findall('.//{*}url'):
    p = parsed[entry.find('{*}loc').text]
    if p.dates:
        assert p.dates == [entry.find('{*}lastmod').text], 'Sitemap and visible dates diverged'
for url, p in parsed.items():
    assert len(p.hreflangs) == 11
    for alternate in p.alternates:
        assert parsed[alternate].hreflangs == p.hreflangs, (url, 'Nonreciprocal hreflang')
discovery = (ROOT / 'llms.txt').read_text()
for url in re.findall(r'\]\((https://ccviewer.top[^)]+)\)', discovery):
    assert url in canonicals or (ROOT / urlsplit(url).path.lstrip('/')).is_file(), url
assert 'Clarity' in discovery and 'not affiliated' in discovery
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
