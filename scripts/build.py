"""Build Court Notes with Python's standard library only."""
import html, json, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'dist'
def esc(x):return html.escape(str(x),quote=True)
def fill(template,fields):
 for k,v in fields.items():template=template.replace('{{'+k+'}}',str(v))
 return template

def thumb(p):
 f=p['frames'][0];end=p['frames'][-1]
 people=''.join(f'<g><circle cx="{x}" cy="{y}" r="16" fill="#26332e"/><text x="{x}" y="{y+5}" font-size="14" text-anchor="middle" fill="#fff" font-family="Arial">{i}</text></g>' for i,(x,y) in enumerate(f['players'],1))
 # Original illustrative geometry, deliberately not a copy of a coaching-manual figure.
 actor=5 if p['slug']=='pick-and-roll' else 1
 a=f['players'][actor-1];b=end['players'][actor-1]
 return f'<svg viewBox="0 0 500 380" aria-hidden="true"><g transform="translate(0,-25)"><path d="M65 65h370v360H65z M180 65h140v180H180z M225 104h50 M250 104v12 M95 65v80C95 370 405 370 405 145V65" fill="none" stroke="#acb7a2" stroke-width="2"/><circle cx="250" cy="128" r="11" fill="none" stroke="#d75b30" stroke-width="3"/><path d="M{a[0]} {a[1]} Q{a[0]+75} {a[1]-65} {b[0]} {b[1]}" fill="none" stroke="#dc5a2e" stroke-width="3" stroke-dasharray="7 5"/>{people}<circle cx="{f["ball"][0]+16}" cy="{f["ball"][1]-16}" r="7" fill="#dc5a2e"/></g></svg>'

def main():
 plays=json.loads((ROOT/'data/plays.json').read_text());raw=json.dumps(plays,ensure_ascii=False).replace('<','\\u003c')
 OUT.mkdir(exist_ok=True)
 # Regenerate all published units, so removed units cannot linger.
 if (OUT/'plays').exists():shutil.rmtree(OUT/'plays')
 shutil.copytree(ROOT/'src/assets',OUT/'assets',dirs_exist_ok=True)
 (OUT/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="13" fill="#202b2a"/><circle cx="32" cy="32" r="20" fill="none" stroke="#f6f3eb" stroke-width="3"/><text x="21" y="42" font-family="Arial" font-size="30" fill="#f6f3eb">C</text><circle cx="46" cy="21" r="5" fill="#dc5a2e"/></svg>')
 cards=[]
 for p in plays:
  cards.append(f'<article class="play-card" data-card="{p["slug"]}"><a class="card-visual" href="plays/{p["slug"]}/index.html" aria-label="閱讀{esc(p["title"])}完整拆解">{thumb(p)}<span class="card-num">PLAY / {p["number"]}</span><span class="card-type">{esc(p["category"])}</span></a><div class="card-body"><a class="card-title-row" href="plays/{p["slug"]}/index.html"><div><h3>{esc(p["title"])}</h3><span class="card-en">{esc(p["english"])}</span></div><span class="card-arrow">↗</span></a><p class="card-summary">{esc(p["summary"])}</p><div class="card-tags">'+''.join(f'<span class="tag">{esc(t)}</span>' for t in p['tags'])+f'</div></div><div class="card-actions"><button class="compare-toggle" data-compare="{p["slug"]}" aria-pressed="false" aria-label="將{esc(p["title"])}加入或移出比較">＋ 加入比較</button><a href="plays/{p["slug"]}/index.html">閱讀拆解 →</a></div></article>')
  fields={'TITLE':esc(p['title']),'SUMMARY':esc(p['summary']),'NUMBER':p['number'],'CATEGORY':esc(p['category']),'DIFFICULTY':esc(p['difficulty']),'ENGLISH':esc(p['english']),'GOAL':esc(p['goal']),'LINEUP':esc(p['lineup']),'SLUG':p['slug'],'JSON':raw,
   'STEPS':''.join(f'<li class="step-item" data-step="{i}"><button class="step-button" aria-pressed="false"><span class="step-n">{i:02}</span><span class="step-copy"><b>{esc(s["title"])}</b><span>{esc(s["text"])}</span></span></button></li>' for i,s in enumerate(p['steps'],1)),
   'POSITIONS':''.join(f'<div class="position-card"><span>0{i}</span>{esc(text)}</div>' for i,text in enumerate(p['positions'],1)),
   'READS':''.join(f'<article class="read-card"><span>IF YOU SEE / {i:02}</span><h3>{esc(r["cue"])}</h3><p>{esc(r["choice"])}</p></article>' for i,r in enumerate(p['reads'],1)),
   'ADVANTAGES':''.join('<li>'+esc(x)+'</li>' for x in p['advantages']),'RISKS':''.join('<li>'+esc(x)+'</li>' for x in p['risks']),
   'MISTAKES':''.join(f'<details><summary>{esc(x)}</summary><p>回到上方步驟，核對站位、持球者與移動時機；先以慢速練習，再依實際防守調整。</p></details>' for x in p['mistakes']),
   'SOURCES':''.join(f'<a class="source-item" href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer"><b>{esc(s["title"])} ↗</b><span>{esc(s["supports"])}</span></a>' for s in p['sources'])}
  target=OUT/'plays'/p['slug'];target.mkdir(parents=True,exist_ok=True)
  (target/'index.html').write_text(fill((ROOT/'templates/play.html').read_text(),fields))
 tabs=''.join(f'<button class="feature-tab {"active" if i==0 else ""}" data-feature="{p["slug"]}" aria-pressed="{str(i==0).lower()}">{esc(p["title"])}</button>' for i,p in enumerate(plays))
 home=fill((ROOT/'templates/index.html').read_text(),{'COUNT':f'{len(plays):02}','CARDS':'\n'.join(cards),'FEATURE_TABS':tabs,'JSON':raw})
 home=home.replace('三個起手式，',f'{"兩" if len(plays)==2 else "三" if len(plays)==3 else str(len(plays))}個起手式，')
 (OUT/'index.html').write_text(home)
 shutil.copyfile(ROOT/'AGENTS.md',OUT/'AGENTS.md');(OUT/'.nojekyll').touch()
 about=OUT/'about';about.mkdir(exist_ok=True)
 (about/'index.html').write_text('''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>關於與來源｜Court Notes</title><link rel="stylesheet" href="../assets/site.css"></head><body><header class="site-header wrap"><a class="brand" href="../index.html"><span class="brand-mark">C<span>·</span></span><span>COURT NOTES<small>籃球戰術拆解室</small></span></a><nav><a href="../index.html#playbook">返回戰術目錄 ←</a></nav></header><main class="wrap about-main"><p class="eyebrow">ABOUT THE NOTEBOOK</p><h1>把配合，變成共同語言。</h1><p>籃球戰術拆解室是給業餘球友的基本配合筆記。透過可操作的五人站位圖、固定章節與比較表，把模糊的「你就跑過去」拆成能一起討論的步驟。</p><h2>這些圖在說什麼？</h2><p>每個單元呈現一個簡化的五對五半場情境，進攻籃框朝上，左右以圖面為準。球員編號是角色標記；圖上的位置、時序與路徑不是等比例測量或真實比賽追蹤，也不模擬防守或保證得分。</p><h2>來源如何使用？</h2><p>基本觀念參考 FIBA／WABC 與 Jr. NBA 的教練教材，來源連結及支持範圍附在每個單元頁尾。本站自行整理五人配置、教學步驟與判讀提示，不把自訂圖解冒充來源原圖，也不捏造成功率。</p><div class="about-source"><h2 style="margin-top:0">一套規則，持續長出新單元。</h2><p>專案以 <a href="../AGENTS.md">AGENTS.md</a> 規定內容章節、命名、共用樣式、圖解資料格式及新增流程。擋拆與傳切構成初版，手遞手則按相同規則新增。所有單元共用模板，首頁與比較表也由同一份戰術資料產生。</p><p>專案組織方式參考 <a href="https://github.com/diveai-lab/diveai-lessons/blob/main/CLAUDE.md" target="_blank" rel="noopener noreferrer">DiveAI 講義專案指引</a>；採用自己的品牌、內容及原創圖解。課程示範亦參考 <a href="https://github.com/22Fatcorgi/AI-Demo" target="_blank" rel="noopener noreferrer">AI-Demo</a>，本網站不需要API金鑰或Gradio。</p></div><h2>想繼續研究？</h2><p>先打開教材來源，再回到球場用慢速配合驗證理解。這裡提供的是開始討論的框架，而不是每個防守情境都有標準答案的戰術生成器。</p><a class="button dark" href="../index.html">回到我的戰術本 ↗</a></main><footer class="site-footer wrap"><span>COURT NOTES · 籃球戰術拆解室</span><a href="../AGENTS.md">閱讀專案規則 ↗</a></footer></body></html>''')
 print(f'Built {len(plays)} plays, homepage and about page into dist/.')
if __name__=='__main__':main()
