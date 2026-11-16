'use strict';
(() => {
 const dataNode=document.getElementById('play-data');
 if(!dataNode)return;
 const plays=JSON.parse(dataNode.textContent);
 const bySlug=Object.fromEntries(plays.map(p=>[p.slug,p]));
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const svgNs='http://www.w3.org/2000/svg';
 function el(name,attrs={}){const n=document.createElementNS(svgNs,name);for(const [k,v] of Object.entries(attrs))n.setAttribute(k,v);return n;}
 let boardSequence=0;
 class Court {
  constructor(host){
   this.host=host;this.step=0;this.timer=null;this.uid='court-'+(++boardSequence);this.build();this.setPlay(bySlug[host.dataset.play]||plays[0]);
  }
  build(){
   this.host.innerHTML=`<svg class="court-svg" viewBox="0 0 500 470" role="img" aria-label="五人半場進攻教學示意"><defs><marker id="${this.uid}-move" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10z" fill="#273c37"/></marker><marker id="${this.uid}-pass" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#dc5a2e"/></marker></defs><text x="250" y="16" text-anchor="middle" class="court-label">進攻籃框 ↑</text><g transform="translate(0,20)"><rect class="court-line" x="25" y="15" width="450" height="425" rx="1"/><path class="court-key" d="M180 15h140v195H180z"/><circle class="court-line" cx="250" cy="210" r="58"/><path class="court-line" d="M52 15v97C52 353 448 353 448 112V15"/><path class="court-line" d="M215 66h70M250 66v17"/><circle cx="250" cy="89" r="12" fill="none" stroke="#dc5a2e" stroke-width="2.5"/><path class="court-line" d="M185 440a65 65 0 0 1 130 0"/></g><g class="arrows"></g><g class="players"></g><circle class="basketball" r="7"/></svg><div class="court-controls"><div class="court-progress" aria-label="選擇戰術階段"></div><div class="control-row"><button class="icon-button previous" aria-label="上一步">←</button><button class="icon-button play-control" aria-label="播放戰術步驟">▶ 播放</button><button class="icon-button next" aria-label="下一步">→</button><button class="replay" aria-label="重設為初始站位">重播</button><span class="step-count"></span></div><p class="court-caption" aria-live="polite"></p></div><div class="court-legend"><span><i class="legend-ball"></i>持球</span><span><i class="legend-move"></i>球員移動</span><span><i class="legend-pass"></i>傳球</span><span>位置非等比例</span></div>`;
   this.svg=this.host.querySelector('svg');this.players=[];
   for(let i=1;i<=5;i++){const g=el('g',{class:'player'});g.append(el('circle',{r:16}));const text=el('text');text.textContent=i;g.append(text);this.svg.querySelector('.players').append(g);this.players.push(g);}
   this.host.querySelector('.previous').addEventListener('click',()=>{this.pause();this.show(this.step-1);});
   this.host.querySelector('.next').addEventListener('click',()=>{this.pause();this.show(this.step+1);});
   this.host.querySelector('.replay').addEventListener('click',()=>{this.pause();this.show(0);});
   this.host.querySelector('.play-control').addEventListener('click',()=>this.timer?this.pause():this.play());
  }
  setPlay(play){this.pause();this.playData=play;this.host.dataset.play=play.slug;const progress=this.host.querySelector('.court-progress');progress.replaceChildren();play.frames.forEach((frame,i)=>{const b=document.createElement('button');b.setAttribute('aria-label',i===0?'初始站位':`第${i}步：${play.steps[i-1].title}`);b.addEventListener('click',()=>{this.pause();this.show(i);});progress.append(b);});this.show(0);}
  show(step){
   const p=this.playData;this.step=Math.max(0,Math.min(p.frames.length-1,step));const frame=p.frames[this.step];
   frame.players.forEach(([x,y],i)=>{this.players[i].style.transform=`translate(${x}px, ${y}px)`;});
   const ball=this.svg.querySelector('.basketball');ball.setAttribute('cx',frame.ball[0]+17);ball.setAttribute('cy',frame.ball[1]-17);
   const arrows=this.svg.querySelector('.arrows');arrows.replaceChildren();
   for(const path of frame.moves){arrows.append(el('path',{d:`M${path[0]} ${path[1]} L${path[2]} ${path[3]}`,class:'run-arrow','marker-end':`url(#${this.uid}-move)`}));}
   if(frame.pass){const f=frame.pass;arrows.append(el('path',{d:`M${f[0]} ${f[1]} L${f[2]} ${f[3]}`,class:'pass-arrow','marker-end':`url(#${this.uid}-pass)`}));}
   this.host.querySelector('.court-caption').textContent=frame.caption;
   this.host.querySelector('.step-count').textContent=`${String(this.step).padStart(2,'0')} / ${String(p.frames.length-1).padStart(2,'0')}`;
   this.host.querySelector('.previous').disabled=this.step===0;this.host.querySelector('.next').disabled=this.step===p.frames.length-1;
   this.host.querySelectorAll('.court-progress button').forEach((b,i)=>{b.classList.toggle('active',i<=this.step);b.setAttribute('aria-current',i===this.step?'step':'false');});
   document.querySelectorAll('.step-item').forEach(n=>{const active=Number(n.dataset.step)===this.step;n.classList.toggle('active',active);n.querySelector('button')?.setAttribute('aria-pressed',String(active));});
   this.svg.setAttribute('aria-label',`${p.title}，${frame.caption}`);
  }
  play(){if(this.step===this.playData.frames.length-1)this.show(0);this.host.querySelector('.play-control').textContent='Ⅱ 暫停';this.host.querySelector('.play-control').setAttribute('aria-label','暫停戰術步驟');this.timer=setInterval(()=>{this.show(this.step+1);if(this.step===this.playData.frames.length-1)this.pause();},1800);}
  pause(){if(this.timer)clearInterval(this.timer);this.timer=null;const button=this.host.querySelector('.play-control');if(button){button.textContent='▶ 播放';button.setAttribute('aria-label','播放戰術步驟');}}
 }
 const courts=[...document.querySelectorAll('[data-court]')].map(n=>new Court(n));
 document.querySelectorAll('[data-feature]').forEach(button=>button.addEventListener('click',()=>{const p=bySlug[button.dataset.feature];if(!p)return;courts[0]?.setPlay(p);document.getElementById('featured-title').innerHTML=`${esc(p.title)} <span>${esc(p.english)}</span>`;document.getElementById('featured-link').href=`plays/${p.slug}/index.html`;document.querySelectorAll('[data-feature]').forEach(b=>{b.classList.toggle('active',b===button);b.setAttribute('aria-pressed',String(b===button));});}));
 document.querySelectorAll('[data-step]').forEach(n=>n.querySelector('button')?.addEventListener('click',()=>{courts[0]?.pause();courts[0]?.show(Number(n.dataset.step));}));
 document.addEventListener('visibilitychange',()=>{if(document.hidden)courts.forEach(c=>c.pause());});
 const search=document.getElementById('play-search');let category='全部';
 function filter(){let count=0;const q=(search?.value||'').trim().toLowerCase();document.querySelectorAll('[data-card]').forEach(card=>{const p=bySlug[card.dataset.card];const show=(category==='全部'||p.category===category)&&[p.title,p.english,p.category,...p.tags].join(' ').toLowerCase().includes(q);card.hidden=!show;if(show)count++;});const empty=document.getElementById('no-results');if(empty)empty.hidden=count!==0;}
 document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{category=b.dataset.filter;document.querySelectorAll('[data-filter]').forEach(n=>{n.classList.toggle('active',n===b);n.setAttribute('aria-pressed',String(n===b));});filter();}));search?.addEventListener('input',filter);
 const selected=new Set();const comparison=document.getElementById('comparison');
 function renderCompare(){if(!comparison)return;document.querySelectorAll('[data-compare]').forEach(b=>{const on=selected.has(b.dataset.compare);b.setAttribute('aria-pressed',String(on));b.textContent=on?'✓ 已加入比較':'＋ 加入比較';});const ps=[...selected].map(s=>bySlug[s]);if(ps.length<2){comparison.innerHTML=`<div class="compare-empty"><span class="compare-glyph">⇄</span><div><h3>${ps.length?'再選一個，放在一起看。':'給兩個方案一個同場比較的機會。'}</h3><p>${ps.length?`已選擇「${esc(ps[0].title)}」。在其他卡片點「加入比較」。`:'先在戰術卡片點「加入比較」，這裡就會出現對照。'}</p></div><span class="count-label">${ps.length} / 3 已選</span></div>`;return;}
  const rows=[['主要目標',p=>p.goal],['適合陣容',p=>p.lineup],['學習門檻',p=>p.difficulty+'（本站教學分類）'],['能創造的機會',p=>p.advantages[0]],['要留意的風險',p=>p.risks[0]]];comparison.innerHTML=`<div class="compare-toolbar"><span>${ps.length} 個配合，同一張對照表。</span><button id="clear-compare">清除比較</button></div><div class="compare-scroll" tabindex="0" aria-label="戰術比較表，可左右捲動"><table class="compare-table"><thead><tr><th scope="col">比較面向</th>${ps.map(p=>`<th scope="col">${esc(p.title)}</th>`).join('')}</tr></thead><tbody>${rows.map(([label,get])=>`<tr><th scope="row">${label}</th>${ps.map(p=>`<td>${esc(get(p))}</td>`).join('')}</tr>`).join('')}<tr><th scope="row">繼續閱讀</th>${ps.map(p=>`<td><a href="plays/${p.slug}/index.html">打開完整拆解 ↗</a></td>`).join('')}</tr></tbody></table></div>`;document.getElementById('clear-compare').addEventListener('click',()=>{selected.clear();renderCompare();});
 }
 document.querySelectorAll('[data-compare]').forEach(b=>b.addEventListener('click',()=>{const s=b.dataset.compare;if(selected.has(s))selected.delete(s);else selected.add(s);renderCompare();}));
})();
