#!/usr/bin/env python3
"""Recover images referenced by public content, preserving upload URLs locally."""
import concurrent.futures
import html
import json
from pathlib import Path
import re
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

def main():
    files = list((ROOT / 'site').rglob('*.md'))
    urls = {'https://josephlemaitre.com/wp-content/uploads/2022/02/head-scaled.jpg'}
    prior = ROOT / 'media-manifest.json'
    if prior.exists():
        urls.update(e['url'] for e in json.loads(prior.read_text()))
    for p in files:
        urls.update(html.unescape(u) for u in re.findall(r'https?://josephlemaitre\.com/wp-content/uploads/[^\s"<>\)]+', p.read_text()))
    def recover(url):
        path = urlparse(url).path
        target = ROOT / 'site' / path.lstrip('/')
        try:
            if not target.exists():
                with urlopen(Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=25) as response:
                    if not response.headers.get('Content-Type','').startswith('image/'):
                        raise ValueError('Expected an image response')
                    data = response.read()
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            return {'url': url, 'local': path, 'recovered': True}
        except Exception as e:
            return {'url': url, 'recovered': False, 'error': str(e)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        report = list(pool.map(recover, sorted(urls)))
    for p in files:
        source = p.read_text()
        for entry in report:
            if entry['recovered']:
                source = source.replace(entry['url'], entry['local'])
        p.write_text(source)
    (ROOT / 'media-manifest.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
