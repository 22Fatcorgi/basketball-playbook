"""Meaningful content/diagram/link contract checks; no third-party packages."""
import json,re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
ROOT=Path(__file__).resolve().parent.parent
plays=json.loads((ROOT/'data/plays.json').read_text());slugs=[]
required={'slug','title','english','category','difficulty','summary','goal','lineup','positions','steps','advantages','risks','reads','mistakes','sources','frames'}
for p in plays:
 assert required<=p.keys(),p.get('slug')
 assert re.fullmatch('[a-z]+(?:-[a-z]+)*',p['slug']),p['slug']
 assert p['slug'] not in slugs;slugs.append(p['slug'])
 assert (ROOT/'content'/f"{p['slug']}.md").exists(),p['slug']
 assert len(p['positions'])==5
 assert len(p['frames'])==len(p['steps'])+1
 assert p['sources'] and all(s['url'].startswith('https://') and s['supports'] for s in p['sources'])
 for f in p['frames']:
  assert len(f['players'])==5
  for x,y in f['players']:assert 0<=x<=500 and 0<=y<=470
  assert f['ball'] in f['players'],'Ball must be assigned to one of the displayed players.'
  if f['pass']:assert len(f['pass'])==4
 assert (ROOT/'dist/plays'/p['slug']/'index.html').exists()
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.add(a['id'])
  for key in ('href','src'):
   if key in a:self.links.append(a[key])
files=list((ROOT/'dist').rglob('*.html'));count=0
for file in files:
 text=file.read_text();assert '{{'not in text,f'Unresolved template in {file}'
 links=Links();links.feed(text)
 for href in links.links:
  u=urlparse(href)
  if u.scheme or u.netloc:continue
  assert not href.startswith('/'),f'Root-relative path breaks project hosting: {href}'
  target=(file.parent/unquote(u.path)) if u.path else file
  if target.is_dir():target=target/'index.html'
  assert target.exists(),f'Broken link {file}: {href}'
  if u.fragment and target.suffix=='.html':
   other=Links();other.feed(target.read_text());assert unquote(u.fragment)in other.ids,(file,href)
  count+=1
print(f'PASS: {len(plays)} complete units; diagram/frame/ball contracts; {len(files)} HTML pages; {count} relative links.')
