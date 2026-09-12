#!/usr/bin/env python3
"""Convert the original WXR export to Markdown. Never overwrites edited files."""
import html
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'wordpress archive/josephlemaitre.WordPress.2026-09-12.xml'
NS = {'wp': 'http://wordpress.org/export/1.2/', 'content': 'http://purl.org/rss/1.0/modules/content/', 'dc': 'http://purl.org/dc/elements/1.1/'}

def text(item, field):
    return item.findtext(field, default='', namespaces=NS) or ''

def convert(source):
    # Social links exist only as Gutenberg block attributes in WXR.
    def social(match):
        attrs = json.loads(match.group(1))
        url = attrs.get('url', '')
        if not url:
            return ''
        if attrs.get('service') == 'mail' and not url.startswith('mailto:'):
            url = 'mailto:' + url
        return '<p><a href="' + html.escape(url, quote=True) + '">' + html.escape(attrs.get('service', 'Link')) + '</a></p>'
    source = re.sub(r'<!-- wp:social-link (\{.*?\}) /-->', social, source)
    source = re.sub(r'<!--.*?-->', '', source, flags=re.S)
    source = re.sub(r'<pre\b[^>]*>', '<pre>', source)
    # Remove WordPress layout wrappers, retaining all text and semantic content.
    source = re.sub(r'</?(?:div|span|figure)\b[^>]*>', '', source)
    source = re.sub(r'<figcaption\b[^>]*>', '<p>', source).replace('</figcaption>', '</p>')
    result = subprocess.run(['pandoc', '--from=html', '--to=gfm', '--wrap=none'], input=source, text=True, capture_output=True, check=True)
    return result.stdout.strip() + '\n'

def main():
    entries = []
    for item in ET.parse(SOURCE).findall('./channel/item'):
        kind, status = text(item, 'wp:post_type'), text(item, 'wp:status')
        if kind not in ('post', 'page'):
            continue
        ident = text(item, 'wp:post_id')
        raw_title = text(item, 'title')
        title = html.unescape(re.sub('<[^>]+>', '', raw_title)).strip() or f'Untitled {kind} {ident}'
        slug = text(item, 'wp:post_name') or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        folder = 'draft' if status == 'draft' else 'private' if status == 'private' else 'site/pages'
        target = ROOT / folder / f'{slug}.md'
        if status == 'publish':
            if kind == 'post':
                target = ROOT / 'site/_posts' / f'{text(item, "wp:post_date")[:10]}-{slug}.md'
            elif ident == '7':
                target = ROOT / 'site/index.md'
        meta = {
            'title': title, 'date': text(item, 'wp:post_date').replace(' ', 'T'),
            'lastmod': text(item, 'wp:post_modified').replace(' ', 'T'),
            'draft': status != 'publish', 'published': status == 'publish', 'slug': slug,
            'render_with_liquid': False,
            'wordpress_id': int(ident), 'wordpress_type': kind, 'wordpress_status': status,
            'wordpress_title': raw_title, 'wordpress_url': text(item, 'link'),
            'author': text(item, 'dc:creator'),
            'categories': [c.text for c in item.findall('category') if c.get('domain') == 'category'],
            'tags': [c.text for c in item.findall('category') if c.get('domain') == 'post_tag'],
        }
        if status == 'publish':
            meta['permalink'] = urlparse(text(item, 'link')).path
            meta['layout'] = 'post' if kind == 'post' else {'7': 'home', '9': 'posts', '137': 'atomic'}.get(ident, 'page')
        front = '\n'.join(k + ': ' + json.dumps(v, ensure_ascii=False) for k,v in meta.items())
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text('---\n' + front + '\n---\n\n' + convert(text(item, 'content:encoded')))
        entries.append({'id': int(ident), 'status': status, 'type': kind, 'title': title, 'file': str(target.relative_to(ROOT)), 'original_url': text(item, 'link')})
    (ROOT / 'migration-manifest.json').write_text(json.dumps(entries, indent=2, ensure_ascii=False) + '\n')
    print(f'Extracted/preserved {len(entries)} Markdown documents.')

if __name__ == '__main__':
    main()
