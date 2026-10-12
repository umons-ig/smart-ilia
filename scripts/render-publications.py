#!/usr/bin/env python3
"""Render the curated ORBI metadata into static, accessible HTML. No network calls."""
from pathlib import Path
import html
import json
import re
from datetime import date

root = Path(__file__).resolve().parent.parent
data = json.loads((root / 'data/recent-publications.json').read_text())
esc = html.escape

def replace_block(path, marker, content):
    source = path.read_text()
    pattern = rf'<!-- {marker}_START -->.*?<!-- {marker}_END -->'
    replacement = f'<!-- {marker}_START -->\n{content}\n<!-- {marker}_END -->'
    updated, count = re.subn(pattern, lambda match: replacement, source, flags=re.S)
    if count != 1:
        raise ValueError(f'{path.name}: expected one {marker} block, found {count}')
    path.write_text(updated)

home, catalogue = [], []
for p in data['publications']:
    authors = []
    for name in p['authors']:
        uid = p['members'].get(name)
        authors.append(f'<a href="https://orbi.umons.ac.be/profile?uid={uid}" class="pub-member">{esc(name)}</a>' if uid else esc(name))
    doi = f'<a href="https://doi.org/{p["doi"]}">Publisher / DOI ↗</a>' if p['doi'] else ''
    kind = 'journal' if p['type'] == 'Journal' else 'conf'
    catalogue.append(f'''<div class="pub-item" id="pub-{p['id']}" data-anim><div class="pub-type pub-type--{kind}">{esc(p['type'])}</div><div class="pub-body"><h3 class="pub-title"><a href="{esc(p['url'])}">{esc(p['title'])}</a></h3><div class="pub-authors">{', '.join(authors)}</div><div class="pub-venue">{esc(p['venue'])} · {esc(p['date_label'])}</div><div class="pub-record-links"><a href="{esc(p['url'])}">ORBI record ↗</a>{doi}</div></div></div>''')
    if p['home']:
        home.append(f'''<article class="latest-paper"><div class="paper-meta"><span class="paper-topic">{esc(p['topic'])}</span><span>{esc(p['type'])}</span><time class="paper-date" datetime="{esc(p['date'])}">{esc(p['date_label'])}</time></div><h3><a href="{esc(p['url'])}">{esc(p['title'])}</a></h3><p class="paper-summary">{esc(p['summary'])}</p><p class="paper-authors">{esc(' · '.join(p['authors']))}</p><div class="paper-bottom"><span class="paper-venue">{esc(p['venue'])}</span><a class="action-text" href="{esc(p['url'])}" aria-label="Read {esc(p['title'])} on ORBI">Read on ORBI <span aria-hidden="true">↗</span></a></div></article>''')

replace_block(root / 'index.html', 'RECENT_PUBLICATIONS', '\n'.join(home))
replace_block(root / 'publications.html', 'RECENT_ORBI', '\n'.join(catalogue))
checked = date.fromisoformat(data['checked_at'])
month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][checked.month - 1]
checked_label = f'{checked.day} {month} {checked.year}'
path = root / 'index.html'
source = path.read_text()
source = re.sub(r'(Selection verified against .*? on )<time datetime="[^"]+">[^<]+</time>', lambda m: m[1] + f'<time datetime="{data["checked_at"]}">{checked_label}</time>', source)
path.write_text(source)
path = root / 'publications.html'
source = re.sub(r'Recent additions verified on [^<]+\.', f'Recent additions verified on {checked_label}.', path.read_text())
path.write_text(source)
print(f'Rendered {len(home)} homepage publications and {len(catalogue)} ORBI additions.')
