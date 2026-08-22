#!/usr/bin/env python3
"""把 data/papers/*.json 构建成静态 dashboard（site/）。

- site/index.html：内嵌轻量索引（无摘要），前端搜索/筛选
- site/papers/*.json：原始数据，展开某篇时按需 fetch
由 GitHub Action 在 data/ 变更时自动运行并发布到 Pages。
本地预览: python3 scripts/build_site.py && python3 -m http.server -d site
"""

import json
import shutil
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = REPO_ROOT / "data" / "papers"
SITE_DIR = REPO_ROOT / "site"

TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>paper-radar</title>
<style>
:root {
  --bg:#fafaf9; --surface:#ffffff; --ink:#1c1917; --muted:#78716c;
  --accent:#059669; --chip:#f5f5f4; --border:#e7e5e4;
}
@media (prefers-color-scheme: dark) { :root {
  --bg:#0c0a09; --surface:#1c1917; --ink:#fafaf9; --muted:#a8a29e;
  --accent:#34d399; --chip:#292524; --border:#292524;
}}
:root[data-theme="light"] { --bg:#fafaf9; --surface:#ffffff; --ink:#1c1917; --muted:#78716c; --accent:#059669; --chip:#f5f5f4; --border:#e7e5e4; }
:root[data-theme="dark"]  { --bg:#0c0a09; --surface:#1c1917; --ink:#fafaf9; --muted:#a8a29e; --accent:#34d399; --chip:#292524; --border:#292524; }
* { box-sizing:border-box; margin:0; }
body { background:var(--bg); color:var(--ink); font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif; }
.wrap { max-width:960px; margin:0 auto; padding:24px 16px 80px; }
header { display:flex; align-items:baseline; gap:12px; flex-wrap:wrap; }
h1 { font-size:22px; }
.built { color:var(--muted); font-size:13px; margin-left:auto; }
#theme { background:none; border:1px solid var(--border); border-radius:6px; color:var(--muted); cursor:pointer; padding:2px 8px; }
.tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:10px; margin:18px 0; }
.tile { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:12px 14px; }
.tile b { display:block; font-size:24px; font-weight:650; }
.tile span { color:var(--muted); font-size:13px; }
.filters { display:flex; gap:8px; flex-wrap:wrap; margin:14px 0 18px; }
.filters input, .filters select { background:var(--surface); color:var(--ink); border:1px solid var(--border); border-radius:8px; padding:7px 10px; font-size:14px; }
.filters input { flex:1; min-width:200px; }
#count { color:var(--muted); font-size:13px; margin:0 0 10px; }
.trend { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:14px; margin:0 0 18px; }
.trend h2 { font-size:15px; margin-bottom:8px; }
.tchips { display:flex; gap:6px; flex-wrap:wrap; margin-bottom:10px; }
.tchip { background:var(--chip); border:1px solid transparent; border-radius:999px; padding:2px 10px; font-size:12.5px; color:var(--muted); cursor:pointer; display:inline-flex; align-items:center; gap:6px; }
.tchip .dot { width:9px; height:9px; border-radius:50%; background:var(--border); }
.tchip.on { color:var(--ink); border-color:var(--border); }
#chart { width:100%; height:auto; display:block; }
#tooltip { position:fixed; pointer-events:none; background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:8px 10px; font-size:12.5px; box-shadow:0 4px 14px rgba(0,0,0,.15); display:none; z-index:9; }
#tooltip .row { display:flex; align-items:center; gap:6px; }
#tooltip .dot { width:8px; height:8px; border-radius:50%; }
.paper { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:12px 14px; margin-bottom:8px; }
.paper h2 { font-size:15.5px; font-weight:600; }
.paper h2 a { color:var(--ink); text-decoration:none; }
.paper h2 a:hover { color:var(--accent); }
.meta { color:var(--muted); font-size:13px; margin:2px 0 6px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.chips { display:flex; gap:6px; flex-wrap:wrap; }
.chip { background:var(--chip); border-radius:999px; padding:1px 9px; font-size:12px; color:var(--muted); }
.chip.curated { color:var(--accent); border:1px solid var(--accent); background:none; }
.more { background:none; border:none; color:var(--accent); cursor:pointer; font-size:13px; padding:0; margin-top:6px; }
.detail { border-top:1px solid var(--border); margin-top:10px; padding-top:10px; font-size:14px; }
.detail h3 { font-size:13px; color:var(--muted); margin:8px 0 2px; font-weight:600; }
.detail p { white-space:pre-wrap; overflow-wrap:break-word; }
#loadmore { display:block; margin:16px auto; background:var(--surface); border:1px solid var(--border); border-radius:8px; color:var(--accent); cursor:pointer; padding:8px 20px; font-size:14px; }
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>📡 paper-radar</h1>
  <span class="built">数据更新：__BUILT__</span>
  <button id="theme" title="切换深浅色">◐</button>
</header>
<div class="tiles">
  <div class="tile"><b id="t-total"></b><span>论文总数</span></div>
  <div class="tile"><b id="t-curated"></b><span>精读整理</span></div>
  <div class="tile"><b id="t-week"></b><span>近 7 天新增</span></div>
  <div class="tile"><b id="t-shown"></b><span>当前筛选</span></div>
</div>
<section class="trend" id="trend" hidden>
  <h2>📈 主题趋势（月度论文数）</h2>
  <div class="tchips" id="tchips"></div>
  <svg id="chart" viewBox="0 0 900 260" role="img" aria-label="主题月度论文数折线图"></svg>
</section>
<div id="tooltip"></div>
<div class="filters">
  <input id="q" type="search" placeholder="搜索标题 / 作者…">
  <select id="f-source"><option value="">来源：全部</option><option value="curated">精读整理</option><option value="auto">自动抓取</option></select>
  <select id="f-topic"><option value="">主题：全部</option></select>
  <select id="f-keyword"><option value="">关键词：全部</option></select>
  <select id="f-category"><option value="">分类：全部</option></select>
  <select id="f-year"><option value="">年份：全部</option></select>
</div>
<p id="count"></p>
<div id="list"></div>
<button id="loadmore" hidden>加载更多</button>
</div>
<script>
const PAPERS = __INDEX__;
const TAX = __TAXONOMY__;
const PAGE = 100;
let filtered = PAPERS, shown = 0;

const $ = id => document.getElementById(id);
const esc = s => (s||'').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

function fillSelect(id, values) {
  const sel = $(id);
  for (const v of values) { const o = document.createElement('option'); o.value = o.textContent = v; sel.append(o); }
}
const uniq = key => [...new Set(PAPERS.map(p => p[key]).filter(Boolean))];
fillSelect('f-keyword', uniq('keyword').sort());
fillSelect('f-category', uniq('category').sort());
fillSelect('f-year', uniq('year').sort((a,b)=>b-a));
for (const t of [...new Set(PAPERS.flatMap(p => p.topics || []))].sort()) {
  const o = document.createElement('option');
  o.value = t; o.textContent = TAX[t] || t;
  $('f-topic').append(o);
}

const weekAgo = new Date(Date.now() - 7*864e5).toISOString().slice(0,10);
$('t-total').textContent = PAPERS.length;
$('t-curated').textContent = PAPERS.filter(p=>p.source==='curated').length;
$('t-week').textContent = PAPERS.filter(p=>p.date && p.date >= weekAgo).length;

function applyFilters() {
  const q = $('q').value.trim().toLowerCase();
  const src = $('f-source').value, kw = $('f-keyword').value,
        cat = $('f-category').value, yr = $('f-year').value, tp = $('f-topic').value;
  filtered = PAPERS.filter(p =>
    (!q || (p.title+' '+(p.authors||'')).toLowerCase().includes(q)) &&
    (!src || p.source === src) &&
    (!tp || (p.topics || []).includes(tp)) &&
    (!kw || p.keyword === kw) &&
    (!cat || p.category === cat) &&
    (!yr || String(p.year) === yr));
  $('t-shown').textContent = filtered.length;
  $('count').textContent = `${filtered.length} 篇（按日期倒序）`;
  $('list').innerHTML = ''; shown = 0;
  renderMore();
}

function chipHtml(p) {
  let h = '';
  if (p.source === 'curated') h += '<span class="chip curated">精读整理</span>';
  if (p.hf_upvotes) h += `<span class="chip">🔥 ${p.hf_upvotes}</span>`;
  for (const t of p.topics || []) h += `<span class="chip">${esc(TAX[t] || t)}</span>`;
  if (p.keyword) h += `<span class="chip">${esc(p.keyword)}</span>`;
  if (p.category) h += `<span class="chip">${esc(p.category)}</span>`;
  if (p.status && p.status !== 'unread') h += `<span class="chip">${esc(p.status)}</span>`;
  return h;
}

function renderMore() {
  const frag = document.createDocumentFragment();
  for (const p of filtered.slice(shown, shown + PAGE)) {
    const el = document.createElement('article');
    el.className = 'paper';
    el.innerHTML = `<h2><a href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.title)}</a></h2>
      <div class="meta">${esc(p.date || p.year || '')} · ${esc(p.authors||'')}</div>
      <div class="chips">${chipHtml(p)}</div>
      <button class="more" data-id="${esc(p.id)}">摘要 ▾</button><div class="detail" hidden></div>`;
    frag.append(el);
  }
  shown = Math.min(shown + PAGE, filtered.length);
  $('list').append(frag);
  $('loadmore').hidden = shown >= filtered.length;
}

$('list').addEventListener('click', async e => {
  const btn = e.target.closest('.more');
  if (!btn) return;
  const detail = btn.nextElementSibling;
  if (!detail.hidden) { detail.hidden = true; btn.textContent = '摘要 ▾'; return; }
  detail.hidden = false; btn.textContent = '收起 ▴';
  if (!detail.innerHTML) {
    detail.textContent = '加载中…';
    try {
      const p = await (await fetch(`papers/${btn.dataset.id}.json`)).json();
      detail.innerHTML = (p.summary ? `<h3>总结</h3><p>${esc(p.summary)}</p>` : '') +
                         (p.abstract ? `<h3>Abstract</h3><p>${esc(p.abstract)}</p>` : '') || '（无摘要）';
    } catch { detail.textContent = '加载失败'; }
  }
});

for (const id of ['q','f-source','f-topic','f-keyword','f-category','f-year'])
  $(id).addEventListener('input', applyFilters);
$('loadmore').addEventListener('click', renderMore);

// ---- 主题趋势折线图 ----
const LIGHT = ['#2a78d6','#eb6834','#1baf7a','#eda100','#e87ba4','#008300','#4a3aa7','#e34948'];
const DARK  = ['#3987e5','#d95926','#199e70','#c98500','#d55181','#008300','#9085e9','#e66767'];
const tagged = PAPERS.filter(p => p.topics && p.date);
if (tagged.length) {
  $('trend').hidden = false;
  const maxMo = tagged.map(p => p.date).sort().at(-1).slice(0,7);
  const months = [];
  let [my, mm] = maxMo.split('-').map(Number);
  for (let i = 0; i < 18; i++) { months.unshift(`${my}-${String(mm).padStart(2,'0')}`); mm--; if (!mm) { mm = 12; my--; } }
  const mIdx = new Map(months.map((mo,i) => [mo,i]));
  const counts = {}, totals = {};
  for (const p of tagged) for (const t of p.topics) {
    totals[t] = (totals[t]||0) + 1;
    const i = mIdx.get(p.date.slice(0,7));
    if (i === undefined) continue;
    (counts[t] ??= Array(months.length).fill(0))[i]++;
  }
  const ranked = Object.keys(counts).sort((a,b) => totals[b]-totals[a]);
  const on = new Set(ranked.slice(0,5));
  const slot = new Map();
  const takeSlot = t => { for (let i=0;i<8;i++) if (![...slot.values()].includes(i)) { slot.set(t,i); return; } };
  on.forEach(takeSlot);
  const isDark = () => (document.documentElement.dataset.theme ||
    (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark':'light')) === 'dark';
  const colorOf = t => (isDark() ? DARK : LIGHT)[slot.get(t)];

  function renderChips() {
    $('tchips').innerHTML = '';
    for (const t of ranked) {
      const b = document.createElement('button');
      b.className = 'tchip' + (on.has(t) ? ' on' : '');
      b.innerHTML = `<span class="dot"${on.has(t) ? ` style="background:${colorOf(t)}"` : ''}></span>${esc(TAX[t]||t)} <small>${totals[t]}</small>`;
      b.onclick = () => {
        if (on.has(t)) { on.delete(t); slot.delete(t); }
        else { if (on.size >= 8) return; on.add(t); takeSlot(t); }
        renderChips(); renderChart();
      };
      $('tchips').append(b);
    }
  }

  const W=900, H=260, PL=40, PR=14, PT=12, PB=28;
  const xAt = i => PL + i*(W-PL-PR)/(months.length-1);
  function renderChart() {
    const act = [...on];
    const ymax = Math.max(1, ...act.flatMap(t => counts[t]));
    const top = Math.max(4, Math.ceil(ymax/4)*4);
    const yAt = v => PT + (H-PT-PB)*(1 - v/top);
    let s = '';
    for (let g=0; g<=4; g++) {
      const v = top*g/4;
      s += `<line x1="${PL}" x2="${W-PR}" y1="${yAt(v)}" y2="${yAt(v)}" stroke="var(--border)"/>`;
      s += `<text x="${PL-6}" y="${yAt(v)+4}" text-anchor="end" font-size="11" fill="var(--muted)">${v}</text>`;
    }
    months.forEach((mo,i) => { if (i%3===0 || i===months.length-1)
      s += `<text x="${xAt(i)}" y="${H-8}" text-anchor="middle" font-size="11" fill="var(--muted)">${mo}</text>`; });
    for (const t of act) {
      const d = counts[t].map((v,i) => `${i?'L':'M'}${xAt(i).toFixed(1)},${yAt(v).toFixed(1)}`).join(' ');
      s += `<path d="${d}" fill="none" stroke="${colorOf(t)}" stroke-width="2" stroke-linejoin="round"/>`;
    }
    s += `<line id="cross" y1="${PT}" y2="${H-PB}" stroke="var(--muted)" opacity="0"/>`;
    $('chart').innerHTML = s;
  }

  $('chart').addEventListener('mousemove', e => {
    const r = $('chart').getBoundingClientRect();
    const i = Math.round(((e.clientX-r.left)/r.width*W - PL) / ((W-PL-PR)/(months.length-1)));
    if (i < 0 || i >= months.length) return;
    const cross = $('chart').querySelector('#cross');
    cross.setAttribute('x1', xAt(i)); cross.setAttribute('x2', xAt(i)); cross.setAttribute('opacity', '.5');
    const tt = $('tooltip');
    tt.innerHTML = `<b>${months[i]}</b>` + [...on].map(t =>
      `<div class="row"><span class="dot" style="background:${colorOf(t)}"></span>${esc(TAX[t]||t)}：${counts[t][i]}</div>`).join('');
    tt.style.display = 'block';
    tt.style.left = Math.min(e.clientX+14, innerWidth-190) + 'px';
    tt.style.top = (e.clientY+14) + 'px';
  });
  $('chart').addEventListener('mouseleave', () => {
    $('tooltip').style.display = 'none';
    $('chart').querySelector('#cross')?.setAttribute('opacity','0');
  });

  renderChips(); renderChart();
  window.__renderTrend = () => { renderChips(); renderChart(); };
}

$('theme').addEventListener('click', () => {
  const cur = document.documentElement.dataset.theme ||
    (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  const next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  localStorage.setItem('theme', next);
  window.__renderTrend?.();
});
const saved = localStorage.getItem('theme');
if (saved) document.documentElement.dataset.theme = saved;

applyFilters();
</script>
</body>
</html>
"""

INDEX_FIELDS = ("id", "title", "authors", "date", "year", "url", "keyword",
                "category", "source", "status", "topics", "hf_upvotes")


def sort_key(p):
    return p.get("date") or (f"{p['year']}-00-00" if p.get("year") else "0000")


def main():
    papers = [json.loads(f.read_text(encoding="utf-8"))
              for f in sorted(PAPERS_DIR.glob("*.json"))]
    papers.sort(key=sort_key, reverse=True)
    index = [{k: p.get(k) for k in INDEX_FIELDS if p.get(k)} for p in papers]

    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    (SITE_DIR / "papers").mkdir(parents=True)
    for f in PAPERS_DIR.glob("*.json"):
        shutil.copy2(f, SITE_DIR / "papers" / f.name)

    taxonomy = json.loads((REPO_ROOT / "data" / "taxonomy.json").read_text(encoding="utf-8"))
    tax_names = {slug: v["name"] for slug, v in taxonomy.items()}

    html = TEMPLATE.replace("__BUILT__", time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()))
    html = html.replace("__INDEX__", json.dumps(index, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__TAXONOMY__", json.dumps(tax_names, ensure_ascii=False, separators=(",", ":")))
    (SITE_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"✅ site/ 构建完成：{len(papers)} 篇，index.html "
          f"{(SITE_DIR / 'index.html').stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
