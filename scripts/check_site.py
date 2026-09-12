#!/usr/bin/env python3
"""Check migrated public routes, internal links, assets and private exclusions."""
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src') and value:
                self.urls.append(value)

errors = []
pages = list(OUT.rglob('*.html'))
assert pages, 'Build the site first.'
for page in pages:
    parser = Links()
    source = page.read_text()
    parser.feed(source)
    base = 'https://jcblemai.github.io/' + page.relative_to(OUT).as_posix()
    for raw in parser.urls:
        url = urlparse(urljoin(base, raw))
        if url.scheme not in ('http', 'https') or url.netloc != 'jcblemai.github.io':
            continue
        path = OUT / unquote(url.path).lstrip('/')
        if path.is_dir():
            path /= 'index.html'
        if not path.is_file():
            errors.append(f'{page.relative_to(OUT)}: broken reference {raw}')
    if '<!-- wp:' in source:
        errors.append(f'{page}: unconverted WordPress blocks')
for path in OUT.rglob('*'):
    if any(part in ('draft', 'private', 'wordpress archive', 'vendor', 'scripts') for part in path.relative_to(OUT).parts):
        errors.append(f'Non-public source in output: {path}')
    if path.name in ('migration-manifest.json', 'Gemfile', 'README.md') or path.suffix == '.md':
        errors.append(f'Source document in output: {path}')
manifest = ROOT / 'migration-manifest.json'
if manifest.exists():
    entries = json.loads(manifest.read_text())
    assert len(entries) == 17
    for entry in entries:
        assert (ROOT / entry['file']).is_file(), entry
        route = urlparse(entry['original_url'])
        if entry['status'] == 'publish' and entry['type'] == 'page' and entry['id'] not in (9, 137):
            assert (OUT / route.path.lstrip('/') / 'index.html').is_file(), entry
        elif not route.query:
            assert not (OUT / route.path.lstrip('/') / 'index.html').exists(), entry
    all_output = '\n'.join(p.read_text() for p in OUT.rglob('*') if p.suffix in ('.html','.xml','.json'))
    for entry in entries:
        if entry['status'] == 'publish':
            continue
        body = (ROOT / entry['file']).read_text().split('---',2)[2].strip()
        # Long verbatim paragraphs identify unpublished text without false title matches.
        for para in body.split('\n\n'):
            if len(para) > 100 and '<' not in para and '[' not in para:
                assert para not in all_output, f'Unpublished content exposed: {entry["file"]}'
for name in ('sitemap.xml',):
    ET.parse(OUT / name)
assert len(list((ROOT/'site/_posts').glob('*.md'))) == 7
if errors:
    raise SystemExit('\n'.join(errors))
assert not (OUT/'posts').exists()
assert not (OUT/'atomic-posts').exists()
for post in (ROOT/'site/_posts').glob('*.md'):
    meta = post.read_text().split('---', 2)[1]
    permalink = json.loads(next(line.split(': ',1)[1] for line in meta.splitlines() if line.startswith('permalink:')))
    assert not (OUT/permalink.lstrip('/')/'index.html').exists()
print(f'PASS: {len(pages)} HTML pages; links/assets; sitemap; posts and private content excluded.')
