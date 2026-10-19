"""Shared public identity and editorial dates; never use the build clock."""
import html
import json

ORIGIN = 'https://ccviewer.top'
APP_URL = ORIGIN + '/claude-code-session-viewer/'
REPOSITORY = 'https://github.com/howardz27/ccviewer'
PUBLISHED = '2026-10-12'
MODIFIED = '2026-10-19'
SOURCES = [
    ('Claude Code: application data, paths and retention', 'https://code.claude.com/docs/en/claude-directory'),
    ('Claude Code: resume and manage sessions', 'https://code.claude.com/docs/en/sessions'),
    ('JSON Lines format', 'https://jsonlines.org/'),
    ('CCViewer source and license', REPOSITORY),
]


def plain(value):
    # Content metadata is plain text; decode existing editorial HTML entities.
    return html.unescape(value)


def attribute(value):
    return html.escape(plain(value), quote=True)


def json_ld(value):
    # Prevent content containing </script> from ending a JSON-LD script.
    return json.dumps(value, ensure_ascii=False).replace('<', '\\u003c')


def identity(url, lang, name, description, kind='WebPage'):
    return json_ld({'@context': 'https://schema.org', '@graph': [
        {'@type': 'Organization', '@id': ORIGIN + '/#organization',
         'name': 'CCViewer', 'url': APP_URL, 'sameAs': [REPOSITORY],
         'logo': ORIGIN + '/assets/logo.svg'},
        {'@type': 'WebSite', '@id': ORIGIN + '/#website', 'name': 'CCViewer',
         'url': APP_URL, 'publisher': {'@id': ORIGIN + '/#organization'}},
        {'@type': kind, '@id': url + '#webpage', 'url': url,
         'name': plain(name), 'description': plain(description), 'inLanguage': lang,
         'isPartOf': {'@id': ORIGIN + '/#website'},
         'publisher': {'@id': ORIGIN + '/#organization'}},
    ]})
