#!/usr/bin/env python3
"""Render sourced team and project content into the static site. No network calls."""
from pathlib import Path
import html
import json
import re
from datetime import date

root=Path(__file__).resolve().parent.parent
if (root/'dist/team.html').is_file():
    root=root/'dist'
esc=html.escape
team=json.loads((root/'data/team-members.json').read_text())
research=json.loads((root/'data/project-research.json').read_text())
visuals=json.loads((root/'data/project-visuals.json').read_text())
visual_by_id={p['id']:p for p in visuals['assets']}
if set(visual_by_id)!=set(p['id'] for p in research['projects']):
    raise ValueError('Project visuals do not match the project catalogue')
statuses=json.loads((root/'data/project-statuses.json').read_text())
status_by_name={p['name']:p for p in statuses['projects']}
checked=date.fromisoformat(statuses['checked_at'])
months=['January','February','March','April','May','June','July','August','September','October','November','December']
checked_label=f'{checked.day} {months[checked.month-1]} {checked.year}'

def replace_block(path,marker,content,start):
    source=path.read_text()
    replacement=f'<!-- {marker}_START -->\n{content}\n<!-- {marker}_END -->'
    if f'<!-- {marker}_START -->' in source:
        source,count=re.subn(rf'<!-- {marker}_START -->.*?<!-- {marker}_END -->',lambda m:replacement,source,flags=re.S)
        if count!=1: raise ValueError(f'Expected one {marker} block')
    else:
        first=source.index(start)
        last=source.index('\n    </div>\n</div>\n</main>',first)
        source=source[:first]+replacement+source[last:]
    path.write_text(source)

groups=list(dict.fromkeys(p['group'] for p in team['members']))
group_ids={'Faculty':'faculty','Researchers & collaborators':'researchers','PhD students':'doctoral-researchers'}
group_labels={'Faculty':'Faculty','Researchers & collaborators':'Researchers','PhD students':'PhD students'}
shortcuts=''.join(f'<a href="#{group_ids[group]}-title">{group_labels[group]} <span>{sum(m["group"]==group for m in team["members"])}</span></a>' for group in groups)
parts=[f'<nav class="team-jump-links" aria-label="Team groups">{shortcuts}</nav>','<div class="team-groups">']
project_contacts={}
for project in research['projects']:
    for link in project['links']:
        if link['url'].startswith('team.html#'):
            project_contacts.setdefault(link['url'].split('#',1)[1],[]).append(project)
for group in groups:
    group_id=group_ids[group]
    grid_class=' team-grid--researchers' if group=='Researchers & collaborators' else ''
    parts.append(f'<section aria-labelledby="{group_id}-title"><h2 class="team-group-label" id="{group_id}-title">{esc(group)}</h2><div class="team-grid{grid_class}">')
    for p in (m for m in team['members'] if m['group']==group):
        if p['image']:
            portrait=f'<div class="team-photo-wrap"><img src="{esc(p["image"])}" alt="{esc(p["name"])}" class="team-photo" width="120" height="120" loading="lazy"></div>'
        else:
            initials=''.join(word[0] for word in p['name'].split()[:2])
            portrait=f'<div class="team-placeholder team-initials" aria-hidden="true">{esc(initials)}</div>'
        focus=esc(p['focus']) if p['focus'] else 'Contact the lab for details of current research.'
        links=''.join(f'<a href="{esc(link["url"])}" class="team-profile-link" aria-label="{esc(link["label"])} — {esc(p["name"])}">{esc(link["label"])} <span aria-hidden="true">↗</span></a>' for link in p['links'])
        related=''.join(f'<a href="projects.html#{esc(project["id"])}" aria-label="{esc(project["name"])} project — {esc(p["name"])}">{esc(project["name"])} <span aria-hidden="true">↗</span></a>' for project in project_contacts.get(p['id'],[]))
        related_html=f'<div class="team-projects"><span class="team-projects-label">Project</span>{related}</div>' if related else ''
        parts.append(f'<article class="team-card" data-anim id="{p["id"]}"><div class="team-identity">{portrait}<div class="team-heading"><h3 class="team-name">{esc(p["name"])}</h3><p class="team-role">{esc(p["role"])}</p></div></div><p class="team-focus">{focus}</p>{related_html}<div class="team-links">{links}</div></article>')
    parts.append('</div></section>')
parts.append('</div><p class="source-note">Research summaries are based on linked profiles and publications. Visit the <a href="https://web.umons.ac.be/ilia/equipe/">UMONS department directory</a> for institutional contact information.</p>')
parts.append('<aside class="research-contact"><div><h2>Find the right research contact.</h2><p>Planning a collaboration or a student project? Contact the lab to discuss your research interests.</p></div><a class="action-primary" href="mailto:said.mahmoudi@umons.ac.be">Contact the lab <span aria-hidden="true">↗</span></a></aside>')
replace_block(root/'team.html','TEAM_PROFILES','\n'.join(parts),'<div class="team-groups">')

def project_card(p):
    status=status_by_name[p['name']]
    visual=visual_by_id[p['id']]
    icon=f'<div class="project-icon project-icon--illustrated" aria-hidden="true"><img src="{esc(visual["image"])}" alt="" width="{visual["width"]}" height="{visual["height"]}" loading="lazy" decoding="async"></div>'
    title=esc(p['name'])
    if p.get('featured'):
        title=f'<a href="https://www.wallesmart.be/">{title} <svg class="external-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M7 17L17 7"/><path d="M7 7h10v10"/></svg></a>'
    status_link=f'<a href="{esc(status["source_url"])}" aria-label="Source for {esc(p["name"])} project information">Project information <span aria-hidden="true">↗</span></a>' if status['source_url'] else ''
    art=''
    if p['image']:
        art=f'<a class="project-art" href="{esc(p["image"])}" aria-label="View the {esc(p["name"])} research diagram"><img class="project-illustration" src="{esc(p["image"])}" alt="{esc(p["image_alt"])}" width="520" height="290" loading="lazy"></a>'
    focus=f'<div class="project-research"><p class="project-focus-label">{esc(p["focus_label"])}</p><p>{esc(p["focus"])}</p></div>' if p['focus'] else ''
    tags=p['tags']+([status['period_label']] if status['period_label'] else [])
    tag_html=''.join(f'<span class="project-tag">{esc(tag)}</span>' for tag in tags)
    links=''.join(f'<a href="{esc(link["url"])}">{esc(link["label"])} <span aria-hidden="true">↗</span></a>' for link in p['links'])
    link_html=f'<div class="project-links">{links}</div>' if links else ''
    outputs=''
    if p.get('outputs'):
        records=[]
        for result in p['outputs']:
            evidence=''.join(f'<a href="{esc(link["url"])}">{esc(link["label"])} <span aria-hidden="true">↗</span></a>' for link in result['links'])
            records.append(f'<article class="project-result"><p class="result-meta">{esc(result["category"])} · {esc(result["date_label"])}</p><h4>{esc(result["title"])}</h4><p>{esc(result["description"])}</p><div class="result-evidence">{evidence}</div></article>')
        outputs=f'<details class="project-results"><summary>{esc(p["outputs_summary"])} <span class="result-count">{len(records)}<span class="sr-only"> documented {"resource" if len(records)==1 else "resources"}</span></span></summary><div class="project-results-body">'+''.join(records)+'</div></details>'
    classes='project-card'+(' project-card--featured' if p.get('featured') else '')
    overview='project-overview'+(' project-overview--text' if not art else '')
    summary=f'<p class="project-desc">{esc(p["summary"])}</p>'
    tags_html=f'<div class="project-tags">{tag_html}</div>'
    if p.get('featured'):
        details=f'<div class="{overview}">{art}<div class="project-copy">{summary}{focus}{tags_html}</div></div>'
    else:
        details=f'<div class="{overview}">{art}{summary}</div>{focus}{tags_html}'
    return f'''<article class="{classes}" data-anim id="{p['id']}">
  <div class="project-header">{icon}<h3 class="project-title">{title}</h3></div>
  <div class="project-status"><strong>{esc(status['status'])}</strong>{status_link}</div>
  {details}
{outputs}
{link_html}
</article>'''

parts=[]
for label,items in [('Research projects & platforms',research['projects'][:6]),('Past projects',research['projects'][6:])]:
    identifier='current-projects' if label.startswith('Research') else 'past-projects'
    parts.append(f'<section class="projects-group" aria-labelledby="{identifier}-title"><h2 class="team-group-label" id="{identifier}-title">{esc(label)}</h2>')
    if identifier=='current-projects':
        parts.append(f'<p class="source-note project-status-note">Status reviewed on <time datetime="{statuses["checked_at"]}">{checked_label}</time>. Unconfirmed timelines are identified; diagrams illustrate research approaches.</p>')
    parts.append('<div class="projects-grid">'+'\n'.join(project_card(p) for p in items)+'</div></section>')
parts.append('<aside class="research-contact"><div><h2>Discuss a research collaboration.</h2><p>Connect with our team about medical AI, smart farming or secure distributed systems.</p></div><a class="action-primary" href="mailto:said.mahmoudi@umons.ac.be">Contact the lab <span aria-hidden="true">↗</span></a></aside>')
replace_block(root/'projects.html','RESEARCH_PROJECTS','\n'.join(parts),'<!-- ══ Research Projects and Platforms ══ -->')
print(f'Rendered {len(team["members"])} team profiles and {len(research["projects"])} project cards.')
