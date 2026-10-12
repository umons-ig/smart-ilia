#!/usr/bin/env python3
"""Render the curated homepage resources from verified local data."""
from pathlib import Path
from html import escape as esc
import json
import re

root = Path(__file__).resolve().parent.parent
if (root / 'dist/index.html').is_file():
    root /= 'dist'
resources = json.loads((root / 'data/research-resources.json').read_text())

def summary_copy(item):
    full = f'<p class="resource-description resource-description--full">{esc(item["summary"])}</p>'
    if item.get('mobile_summary'):
        full += f'<p class="resource-description resource-description--short">{esc(item["mobile_summary"])}</p>'
    return full

p = resources['feature']
original = p.get('image_original', p['image'])
responsive = ''
if p.get('image_srcset'):
    responsive = f' srcset="{esc(p["image_srcset"])}" sizes="{esc(p["image_sizes"])}"'
parts = [f'''<div class="resource-grid">
  <article class="resource-feature" aria-labelledby="{esc(p['id'])}-title">
    <figure class="resource-figure">
      <a href="{esc(original)}" aria-label="View the complete MPB-UNet published figure"><img src="{esc(p['image'])}"{responsive} alt="{esc(p['image_alt'])}" width="{p['image_width']}" height="{p['image_height']}" loading="lazy" decoding="async"></a>
      <figcaption><a href="{esc(p['url'])}">{esc(p['image_credit'])}</a> · <a href="{esc(p['image_license_url'])}">{esc(p['image_license'])}</a><span>Published test examples · <a href="{esc(original)}">View full figure <span aria-hidden="true">↗</span></a></span></figcaption>
    </figure>
    <div class="resource-body"><p class="eyebrow">{esc(p['category'])}</p><h3 id="{esc(p['id'])}-title">{esc(p['title'])}</h3>{summary_copy(p)}<p class="resource-date"><time datetime="{esc(p['published_at'])}">{esc(p['date_label'])}</time></p><a class="action-text" href="{esc(p['url'])}">{esc(p['link_label'])} <span aria-hidden="true">↗</span></a></div>
  </article>
  <div class="resource-stories">''']
for p in resources['articles']:
    parts.append(f'''<article class="resource-story" aria-labelledby="{esc(p['id'])}-title">
  <div class="resource-meta"><p class="eyebrow">{esc(p['category'])}</p><time datetime="{esc(p['date'])}">{esc(p['date_label'])}</time></div>
  <h3 id="{esc(p['id'])}-title"><a href="{esc(p['url'])}" hreflang="{esc(p['language'])}">{esc(p['title'])}</a></h3>{summary_copy(p)}
  <div class="resource-links"><a class="action-text" href="{esc(p['url'])}" hreflang="{esc(p['language'])}">{esc(p['link_label'])} <small class="resource-language">FR<span class="sr-only"> · in French</span></small><span aria-hidden="true">↗</span></a><a class="resource-project" href="{esc(p['project_url'])}">{esc(p['project_label'])} <span aria-hidden="true">↗</span></a></div>
</article>''')
parts.append('</div></div>')
path = root / 'index.html'
source, count = re.subn(r'<!-- HOME_RESOURCES_START -->.*?<!-- HOME_RESOURCES_END -->', lambda _: '<!-- HOME_RESOURCES_START -->\n' + '\n'.join(parts) + '\n<!-- HOME_RESOURCES_END -->', path.read_text(), flags=re.S)
if count != 1:
    raise ValueError('Expected exactly one HOME_RESOURCES block')
path.write_text(source)
print(f'Rendered one published research visual and {len(resources["articles"])} sourced resources.')
