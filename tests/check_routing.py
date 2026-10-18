"""Check actual Cloudflare routing, locally with wrangler or after deployment.

Usage: python3 tests/check_routing.py --base http://127.0.0.1:8787
       python3 tests/check_routing.py --base https://ccviewer.top
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def check(base, path, expected_status, expected_path=None, expected_query=None):
    request = Request(base + path, method='HEAD', headers={'User-Agent': 'CCViewerRoutingCheck/1.0'})
    try:
        response = build_opener(NoRedirect).open(request, timeout=20)
    except HTTPError as error:
        response = error
    with response:
        status, location = response.code, response.headers.get('Location', '')
    assert status == expected_status, (path, status, location, 'expected', expected_status)
    if expected_path is not None:
        actual = urlsplit(location)
        assert actual.path == expected_path, (path, location, expected_path)
        assert not actual.netloc or actual.netloc == urlsplit(base).netloc, (path, location)
        if expected_query is not None:
            assert actual.query == expected_query, (path, location, expected_query)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True)
    args = parser.parse_args()
    base = args.base.rstrip('/')
    cases = []
    for entry in ET.parse(ROOT / 'sitemap.xml').findall('.//{*}loc'):
        cases.append((urlsplit(entry.text).path, 200, None, None))
    for line in (ROOT / '_redirects').read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'):
            continue
        source, destination, code = line.split()
        cases.append((source, int(code), destination, None))
    cases.extend([
        ('/?utm_source=routing-check', 301, '/claude-code-session-viewer/', 'utm_source=routing-check'),
        ('/claude-code-session-viewer/help.html?utm_source=routing-check', 301, '/claude-code-session-viewer/help', 'utm_source=routing-check'),
        ('/claude-code-session-viewer/not-an-existing-page', 404, None, None),
    ])
    for path in ['/docs/analytics.md', '/tests/check_pages.py',
                 '/claude-code-session-viewer/src/template.html',
                 '/claude-code-session-viewer/analytics.json', '/.git/config']:
        cases.append((path, 404, None, None))
    failures = []
    def run(case):
        try:
            check(base, *case)
        except Exception as error:
            return str(error)
        return None
    with ThreadPoolExecutor(max_workers=6) as pool:
        failures = [error for error in pool.map(run, cases) if error]
    if failures:
        raise SystemExit('\n'.join(failures))
    print(f'Routing passed: {len(cases)} HTTP checks at {base}; canonical 200s, permanent aliases, query preservation and real 404.')


if __name__ == '__main__':
    main()
