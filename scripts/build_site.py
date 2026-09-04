#!/usr/bin/env python3
"""把 data/papers/*.json 构建成静态论文站（site/）。

- site/index.html：导师地图
- site/papers.html：内嵌轻量索引（无摘要），前端搜索/筛选
- site/paper.html：每篇论文共用的结构化详情页
- site/papers/*.json：原始数据，详情页按需 fetch
由 workpc cron 在数据更新后自动运行。
本地预览: python3 scripts/build_site.py && python3 -m http.server -d site
"""

import json
import re
import shutil
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = REPO_ROOT / "data" / "papers"
SITE_DIR = REPO_ROOT / "site"
SOCIAL_IMAGE = REPO_ROOT / "assets" / "paper-radar-og.png"

FACULTY = [
    {"name": "Sergey Levine", "institution": "UC Berkeley", "region": "美国", "homepage": "https://www2.eecs.berkeley.edu/Faculty/Homepages/svlevine.html", "topics": ["vla-models", "vla-post-training", "robot-manipulation"]},
    {"name": "Pieter Abbeel", "institution": "UC Berkeley", "region": "美国", "homepage": "https://www2.eecs.berkeley.edu/Faculty/Homepages/pabbeel.html", "topics": ["robot-manipulation", "safe-rl"]},
    {"name": "Claire Tomlin", "institution": "UC Berkeley", "region": "美国", "homepage": "https://www2.eecs.berkeley.edu/Faculty/Homepages/tomlin.html", "topics": ["formal-methods", "safe-rl", "runtime-monitoring"]},
    {"name": "Chelsea Finn", "institution": "Stanford", "region": "美国", "homepage": "https://ai.stanford.edu/~cbfinn/", "topics": ["vla-models", "vla-post-training", "robot-manipulation"]},
    {"name": "Dorsa Sadigh", "institution": "Stanford", "region": "美国", "homepage": "https://dorsa.fyi/", "topics": ["hri-human-in-loop", "safe-rl", "robot-manipulation"]},
    {"name": "Jiajun Wu", "institution": "Stanford", "region": "美国", "homepage": "https://jiajunwu.com/", "topics": ["world-model-learning", "world-model-control", "robot-manipulation"]},
    {"name": "Shuran Song", "institution": "Stanford", "region": "美国", "homepage": "https://shurans.github.io/", "topics": ["robot-manipulation", "world-model-learning", "multimodal-perception"]},
    {"name": "Marco Pavone", "institution": "Stanford", "region": "美国", "homepage": "https://web.stanford.edu/~pavone/", "topics": ["runtime-monitoring", "safe-rl", "world-model-control"]},
    {"name": "Russ Tedrake", "aliases": ["Russell Tedrake"], "institution": "MIT", "region": "美国", "homepage": "https://locomotion.csail.mit.edu/russt.html", "topics": ["formal-methods", "safe-rl", "robot-manipulation"]},
    {"name": "Pulkit Agrawal", "institution": "MIT", "region": "美国", "homepage": "https://people.csail.mit.edu/pulkitag/", "topics": ["robot-manipulation", "sim-to-real", "safe-rl"]},
    {"name": "Luca Carlone", "institution": "MIT", "region": "美国", "homepage": "https://lucacarlone.mit.edu/", "topics": ["runtime-monitoring", "formal-methods", "robot-manipulation"]},
    {"name": "Chuchu Fan", "institution": "MIT", "region": "美国", "homepage": "https://chuchu.mit.edu/", "topics": ["formal-methods", "runtime-monitoring", "safe-rl"]},
    {"name": "Deepak Pathak", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://pathak22.github.io/", "topics": ["world-model-learning", "robot-manipulation", "safe-rl"]},
    {"name": "Andrea Bajcsy", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.cs.cmu.edu/~abajcsy/", "topics": ["vla-safety", "safe-rl", "hri-human-in-loop"]},
    {"name": "Anirudha Majumdar", "institution": "Princeton", "region": "美国", "homepage": "https://irom-lab.princeton.edu/", "topics": ["formal-methods", "runtime-monitoring", "safe-rl"]},
    {"name": "Sylvia Herbert", "institution": "UC San Diego", "region": "美国", "homepage": "https://sylviaherbert.com/", "topics": ["formal-methods", "runtime-monitoring", "safe-rl"]},
    {"name": "Ken Goldberg", "institution": "UC Berkeley", "region": "美国", "homepage": "https://goldberg.berkeley.edu/", "topics": ["robot-manipulation", "embodied-benchmarks", "hri-human-in-loop"]},
    {"name": "Koushil Sreenath", "institution": "UC Berkeley", "region": "美国", "homepage": "https://hybrid-robotics.berkeley.edu/", "topics": ["formal-methods", "safe-rl", "robot-manipulation"]},
    {"name": "Jeannette Bohg", "institution": "Stanford", "region": "美国", "homepage": "https://web.stanford.edu/~bohg/", "topics": ["robot-manipulation", "multimodal-perception", "runtime-monitoring"]},
    {"name": "Mykel Kochenderfer", "institution": "Stanford", "region": "美国", "homepage": "https://mykel.kochenderfer.com/", "topics": ["safe-rl", "runtime-monitoring", "embodied-benchmarks"]},
    {"name": "Daniela Rus", "institution": "MIT", "region": "美国", "homepage": "https://danielarus.csail.mit.edu/", "topics": ["robot-manipulation", "embodied-benchmarks", "hri-human-in-loop"]},
    {"name": "Phillip Isola", "institution": "MIT", "region": "美国", "homepage": "https://web.mit.edu/phillipi/", "topics": ["world-model-learning", "robot-manipulation", "multimodal-perception"]},
    {"name": "Leslie Pack Kaelbling", "aliases": ["Leslie Kaelbling"], "institution": "MIT", "region": "美国", "homepage": "https://people.csail.mit.edu/lpk/", "topics": ["llm-planning", "robot-manipulation", "safe-rl"]},
    {"name": "Vincent Sitzmann", "institution": "MIT", "region": "美国", "homepage": "https://www.vincentsitzmann.com/", "topics": ["world-model-learning", "video-world-models", "multimodal-perception"]},
    {"name": "Abhinav Gupta", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.cs.cmu.edu/~abhinavg/", "topics": ["robot-manipulation", "world-model-learning", "multimodal-perception"]},
    {"name": "David Held", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://davheld.github.io/", "topics": ["robot-manipulation", "world-model-learning", "sim-to-real"]},
    {"name": "Oliver Kroemer", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.ri.cmu.edu/ri-faculty/oliver-kroemer/", "topics": ["robot-manipulation", "hri-human-in-loop", "safe-rl"]},
    {"name": "Guanya Shi", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.gshi.me/", "topics": ["safe-rl", "sim-to-real", "robot-manipulation"]},
    {"name": "Ding Zhao", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://safeai-lab.github.io/", "topics": ["vla-safety", "safe-rl", "embodied-benchmarks"]},
    {"name": "Changliu Liu", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.cs.cmu.edu/~cliu6/", "topics": ["safe-rl", "formal-methods", "hri-human-in-loop"]},
    {"name": "Dieter Fox", "institution": "University of Washington", "region": "美国", "homepage": "https://homes.cs.washington.edu/~fox/", "topics": ["robot-manipulation", "multimodal-perception", "vla-models"]},
    {"name": "Byron Boots", "institution": "University of Washington", "region": "美国", "homepage": "https://homes.cs.washington.edu/~bboots/", "topics": ["safe-rl", "world-model-control", "sim-to-real"]},
    {"name": "Abhishek Gupta", "institution": "University of Washington", "region": "美国", "homepage": "https://homes.cs.washington.edu/~abhgupta/", "topics": ["world-model-learning", "robot-manipulation", "sim-to-real"]},
    {"name": "Siddhartha Srinivasa", "aliases": ["Sidd Srinivasa"], "institution": "University of Washington", "region": "美国", "homepage": "https://www.cs.washington.edu/people/faculty/siddhartha-sidd-srinivasa/", "topics": ["robot-manipulation", "hri-human-in-loop", "llm-planning"]},
    {"name": "Dhruv Batra", "institution": "Georgia Tech", "region": "美国", "homepage": "https://faculty.cc.gatech.edu/~dbatra/", "topics": ["embodied-benchmarks", "multimodal-perception", "llm-agents"]},
    {"name": "Danfei Xu", "institution": "Georgia Tech", "region": "美国", "homepage": "https://faculty.cc.gatech.edu/~danfei/", "topics": ["vla-models", "world-model-learning", "robot-manipulation"]},
    {"name": "Sehoon Ha", "institution": "Georgia Tech", "region": "美国", "homepage": "https://faculty.cc.gatech.edu/~sha9/", "topics": ["robot-manipulation", "safe-rl", "sim-to-real"]},
    {"name": "Ufuk Topcu", "institution": "UT Austin", "region": "美国", "homepage": "https://ece.utexas.edu/people/faculty/ufuk-topcu", "topics": ["formal-methods", "safe-rl", "runtime-monitoring"]},
    {"name": "Yuke Zhu", "institution": "UT Austin", "region": "美国", "homepage": "https://yukezhu.me/", "topics": ["vla-models", "robot-manipulation", "llm-planning"]},
    {"name": "Peter Stone", "institution": "UT Austin", "region": "美国", "homepage": "https://www.cs.utexas.edu/~pstone/", "topics": ["safe-rl", "robot-manipulation", "hri-human-in-loop"]},
    {"name": "Joydeep Biswas", "institution": "UT Austin", "region": "美国", "homepage": "https://www.cs.utexas.edu/~joydeepb/", "topics": ["robot-manipulation", "llm-planning", "embodied-benchmarks"]},
    {"name": "Jaime Fernandez Fisac", "aliases": ["Jaime Fisac", "Fisac"], "institution": "Princeton", "region": "美国", "homepage": "https://ece.princeton.edu/people/jaime-fernandez-fisac", "topics": ["formal-methods", "safe-rl", "hri-human-in-loop"]},
    {"name": "Xiaolong Wang", "institution": "UC San Diego", "region": "美国", "homepage": "https://xiaolonw.github.io/", "topics": ["robot-manipulation", "world-model-learning", "multimodal-perception"]},
    {"name": "Lerrel Pinto", "institution": "New York University", "region": "美国", "homepage": "https://lerrelpinto.com/", "topics": ["vla-models", "robot-manipulation", "safe-rl"]},
    {"name": "Yilun Du", "institution": "Harvard", "region": "美国", "homepage": "https://yilundu.github.io/", "topics": ["world-model-learning", "world-model-control", "robot-manipulation"]},
    {"name": "Angela Schoellig", "institution": "Technical University of Munich", "region": "德国", "homepage": "https://www.ce.cit.tum.de/lsy/prof-angela-schoellig/", "topics": ["safe-rl", "sim-to-real", "runtime-monitoring"]},
    {"name": "Matthias Althoff", "institution": "Technical University of Munich", "region": "德国", "homepage": "https://www.ce.cit.tum.de/air/people/prof-dr-ing-matthias-althoff/", "topics": ["formal-methods", "runtime-monitoring", "safe-rl"]},
    {"name": "Melanie Zeilinger", "institution": "ETH Zurich", "region": "瑞士", "homepage": "https://idsc.ethz.ch/research-zeilinger.html", "topics": ["safe-rl", "formal-methods", "runtime-monitoring"]},
    {"name": "Lars Lindemann", "institution": "ETH Zurich", "region": "瑞士", "homepage": "https://ee.ethz.ch/the-department/people-a-z/person-detail.MzY4OTYz.TGlzdC8zMjc5LC0xNjUwNTg5ODIw.html", "topics": ["formal-methods", "runtime-monitoring", "safe-rl"]},
    {"name": "Andreas Krause", "institution": "ETH Zurich", "region": "瑞士", "homepage": "https://las.inf.ethz.ch/krausea", "topics": ["safe-rl", "runtime-monitoring", "world-model-control"]},
    {"name": "Stelian Coros", "institution": "ETH Zurich", "region": "瑞士", "homepage": "https://crl.ethz.ch/people/coros/index.html", "topics": ["robot-manipulation", "world-model-control", "sim-to-real"]},
    {"name": "Aaron Ames", "institution": "Caltech", "region": "美国", "homepage": "https://directory.caltech.edu/personnel/adames", "topics": ["formal-methods", "safe-rl", "robot-manipulation"]},
    {"name": "Nikolai Matni", "institution": "University of Pennsylvania", "region": "美国", "homepage": "https://nikolaimatni.github.io/", "topics": ["safe-rl", "formal-methods", "runtime-monitoring"]},
    {"name": "George Pappas", "institution": "University of Pennsylvania", "region": "美国", "homepage": "https://www.georgejpappas.org/", "topics": ["formal-methods", "runtime-monitoring", "safe-rl"]},
    {"name": "Vijay Kumar", "institution": "University of Pennsylvania", "region": "美国", "homepage": "https://www.kumarrobotics.org/", "topics": ["robot-manipulation", "safe-rl", "embodied-benchmarks"]},
    {"name": "Rahul Mangharam", "institution": "University of Pennsylvania", "region": "美国", "homepage": "https://precise.seas.upenn.edu/people/faculty", "topics": ["runtime-monitoring", "formal-methods", "safe-rl"]},
    {"name": "Dimos Dimarogonas", "institution": "KTH Royal Institute of Technology", "region": "瑞典", "homepage": "https://www.kth.se/profile/dimos", "topics": ["formal-methods", "safe-rl", "hri-human-in-loop"]},
    {"name": "Jana Tumova", "institution": "KTH Royal Institute of Technology", "region": "瑞典", "homepage": "https://people.kth.se/~tumova/", "topics": ["formal-methods", "llm-planning", "hri-human-in-loop"]},
    {"name": "Calin Belta", "institution": "Boston University", "region": "美国", "homepage": "https://sites.bu.edu/hyness/calin-belta/", "topics": ["formal-methods", "safe-rl", "runtime-monitoring"]},
    {"name": "Sayan Mitra", "institution": "University of Illinois Urbana-Champaign", "region": "美国", "homepage": "https://mitras.ece.illinois.edu/", "topics": ["formal-methods", "runtime-monitoring", "safe-rl"]},
    {"name": "Somil Bansal", "institution": "USC", "region": "美国", "homepage": "https://sites.google.com/view/somilbansal", "topics": ["safe-rl", "formal-methods", "multimodal-perception"]},
    {"name": "Florian Shkurti", "institution": "University of Toronto", "region": "加拿大", "homepage": "https://www.cs.toronto.edu/~florian/", "topics": ["vla-models", "robot-manipulation", "embodied-benchmarks"]},
    {"name": "Igor Gilitschenski", "institution": "University of Toronto", "region": "加拿大", "homepage": "https://www.gilitschenski.org/", "topics": ["safe-rl", "world-model-control", "robot-manipulation"]},
    {"name": "Edward Johns", "institution": "Imperial College London", "region": "英国", "homepage": "https://www.robot-learning.uk/", "topics": ["vla-models", "robot-manipulation", "sim-to-real"]},
    {"name": "Ingmar Posner", "institution": "University of Oxford", "region": "英国", "homepage": "https://ori.ox.ac.uk/people/ingmar-posner/", "topics": ["robot-manipulation", "world-model-learning", "multimodal-perception"]},
    {"name": "Nick Hawes", "institution": "University of Oxford", "region": "英国", "homepage": "https://nickhawes.com/", "topics": ["llm-planning", "robot-manipulation", "runtime-monitoring"]},
    {"name": "Jan Peters", "institution": "TU Darmstadt", "region": "德国", "homepage": "https://www.ias.informatik.tu-darmstadt.de/Team/JanPeters", "topics": ["safe-rl", "robot-manipulation", "sim-to-real"]},
    {"name": "Marc Deisenroth", "institution": "University College London", "region": "英国", "homepage": "https://www.ucl.ac.uk/engineering/research/centres-institutes-and-labs/ucl-centre-artificial-intelligence/people", "topics": ["safe-rl", "world-model-control", "robot-manipulation"]},
    {"name": "Davide Scaramuzza", "institution": "University of Zurich", "region": "瑞士", "homepage": "https://rpg.ifi.uzh.ch/people_scaramuzza.html", "topics": ["robot-manipulation", "safe-rl", "multimodal-perception"]},
    {"name": "Cewu Lu", "institution": "Shanghai Jiao Tong University", "region": "中国大陆", "homepage": "https://www.qingyuan.sjtu.edu.cn/a/Cewu-Lu.html", "topics": ["vla-models", "robot-manipulation", "multimodal-perception"]},
    {"name": "He Wang", "institution": "Peking University", "region": "中国大陆", "homepage": "https://hughw19.github.io/", "topics": ["vla-models", "world-model-learning", "robot-manipulation"]},
    {"name": "Hongsheng Li", "institution": "Chinese University of Hong Kong", "region": "中国香港", "homepage": "https://research.cuhk.edu.hk/en/persons/hongsheng-li/", "topics": ["vla-models", "robot-manipulation", "multimodal-perception"]},
    {"name": "Ping Luo", "institution": "University of Hong Kong", "region": "中国香港", "homepage": "https://datascience.hku.hk/people/ping-luo/", "topics": ["vla-models", "embodied-benchmarks", "multimodal-perception"]},
    {"name": "Ziwei Liu", "institution": "Nanyang Technological University", "region": "新加坡", "homepage": "https://liuziwei7.github.io/", "topics": ["vla-models", "world-model-learning", "multimodal-perception"]},
    {"name": "David Hsu", "institution": "National University of Singapore", "region": "新加坡", "homepage": "https://www.comp.nus.edu.sg/~dyhsu/", "topics": ["llm-planning", "safe-rl", "hri-human-in-loop"]},
    {"name": "Harold Soh", "institution": "National University of Singapore", "region": "新加坡", "homepage": "https://haroldsoh.com/", "topics": ["hri-human-in-loop", "safe-rl", "robot-manipulation"]},
    {"name": "Qifeng Chen", "institution": "HKUST", "region": "中国香港", "homepage": "https://cqf.io/", "topics": ["robot-manipulation", "world-model-learning", "multimodal-perception"]},
    {"name": "Ping Tan", "institution": "HKUST", "region": "中国香港", "homepage": "https://ece.hkust.edu.hk/pingtan", "topics": ["world-model-learning", "robot-manipulation", "multimodal-perception"]},
    {"name": "Jia Pan", "institution": "University of Hong Kong", "region": "中国香港", "homepage": "https://www.cs.hku.hk/people/academic-staff/jpan", "topics": ["robot-manipulation", "safe-rl", "sim-to-real"]},
]

TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>导师地图 · paper-radar</title>
<meta name="description" content="按导师研究方向浏览具身智能、机器人学习与安全论文">
<meta property="og:title" content="paper-radar">
<meta property="og:description" content="Classify. Review. Connect.">
<meta property="og:image" content="https://zhatgpt.com/paper-radar-og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="paper-radar">
<meta name="twitter:description" content="Classify. Review. Connect.">
<meta name="twitter:image" content="https://zhatgpt.com/paper-radar-og.png">
<style>
:root {
  --bg:#f5f7fb; --surface:#ffffff; --ink:#17223b; --muted:#65708a;
  --accent:#2546d8; --accent-soft:#e9edff; --signal:#e14a2b; --border:#dce2ee;
}
@media (prefers-color-scheme: dark) { :root {
  --bg:#0c1220; --surface:#151d2f; --ink:#f3f6ff; --muted:#a9b2c7;
  --accent:#8ea2ff; --accent-soft:#202b52; --signal:#ff8065; --border:#293550;
}}
:root[data-theme="light"] { --bg:#f5f7fb; --surface:#fff; --ink:#17223b; --muted:#65708a; --accent:#2546d8; --accent-soft:#e9edff; --signal:#e14a2b; --border:#dce2ee; }
:root[data-theme="dark"]  { --bg:#0c1220; --surface:#151d2f; --ink:#f3f6ff; --muted:#a9b2c7; --accent:#8ea2ff; --accent-soft:#202b52; --signal:#ff8065; --border:#293550; }
* { box-sizing:border-box; margin:0; }
body { background:var(--bg); color:var(--ink); font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif; }
button,input { font:inherit; }
.wrap { max-width:1180px; margin:auto; padding:0 24px 80px; }
.topbar { height:72px; display:flex; align-items:center; gap:18px; border-bottom:1px solid var(--border); }
.brand { font-weight:800; letter-spacing:-.02em; }
.brand span { color:var(--signal); }
.site-nav { display:flex; gap:4px; }
.site-nav a { color:var(--muted); text-decoration:none; padding:6px 10px; border-radius:8px; font-size:14px; }
.site-nav a:hover,.site-nav a.on { color:var(--accent); background:var(--accent-soft); }
.built { color:var(--muted); font-size:13px; margin-left:auto; }
#theme { background:var(--surface); border:1px solid var(--border); border-radius:999px; color:var(--muted); cursor:pointer; padding:4px 11px; }
.intro { padding:44px 0 28px; display:grid; grid-template-columns:minmax(0,1.2fr) minmax(260px,.8fr); gap:48px; align-items:end; }
.kicker { color:var(--signal); font-size:13px; font-weight:800; letter-spacing:.12em; }
h1 { font-size:clamp(38px,6vw,72px); line-height:1.02; letter-spacing:-.055em; margin-top:10px; max-width:760px; }
.scope { color:var(--muted); border-left:3px solid var(--accent); padding-left:16px; }
.controls { position:sticky; top:0; z-index:3; background:color-mix(in srgb,var(--bg) 92%,transparent); backdrop-filter:blur(12px); padding:16px 0; display:flex; flex-wrap:wrap; gap:10px; border-bottom:1px solid var(--border); }
#q,.controls select { background:var(--surface); color:var(--ink); border:1px solid var(--border); border-radius:10px; padding:10px 13px; }
#q { flex:1; min-width:180px; }
.directory { display:grid; grid-template-columns:240px minmax(0,1fr); gap:36px; padding-top:28px; }
.topics h2 { font-size:13px; letter-spacing:.1em; color:var(--muted); margin-bottom:12px; }
.topic-list { display:grid; gap:6px; }
.topic { border:0; background:transparent; color:var(--muted); text-align:left; cursor:pointer; padding:8px 10px; border-radius:8px; }
.topic:hover,.topic.on { background:var(--accent-soft); color:var(--accent); }
.result-head { display:flex; justify-content:space-between; gap:20px; align-items:baseline; margin-bottom:10px; }
.result-head h2 { font-size:24px; }
#count { color:var(--muted); font-size:14px; }
#list { border-top:1px solid var(--ink); }
.faculty { display:grid; grid-template-columns:60px minmax(190px,.7fr) minmax(250px,1.3fr); gap:18px; padding:22px 4px; border-bottom:1px solid var(--border); }
.avatar { width:48px; height:48px; display:grid; place-items:center; border-radius:50%; background:var(--accent-soft); color:var(--accent); font-weight:800; }
.identity h3 { font-size:19px; line-height:1.25; }
.identity p { color:var(--muted); font-size:14px; margin-top:3px; }
.identity a { display:inline-block; color:var(--accent); text-decoration:none; margin-top:8px; font-size:14px; }
.chips { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px; }
.chip { color:var(--accent); background:var(--accent-soft); border-radius:999px; padding:3px 9px; font-size:13px; }
.evidence { color:var(--muted); font-size:14px; }
.paper-links { display:grid; gap:5px; margin-top:8px; }
.paper-links a { color:var(--ink); text-decoration:none; font-size:14px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.paper-links a:hover { color:var(--accent); }
.empty { color:var(--muted); padding:48px 0; }
@media (max-width:760px) {
  .wrap{padding:0 16px 60px}.built{display:none}.intro{grid-template-columns:1fr;gap:20px;padding:32px 0 22px}
  .directory{grid-template-columns:1fr;gap:20px}.topic-list{display:flex;overflow:auto}.topic{white-space:nowrap}
  .faculty{grid-template-columns:48px 1fr}.faculty-main{grid-column:2}.controls{top:0}.controls select{flex:1;min-width:145px}
}
</style>
</head>
<body>
<div class="wrap">
<header class="topbar">
  <div class="brand">paper<span>radar</span> / 导师地图</div>
  <nav class="site-nav" aria-label="主导航"><a class="on" href="index.html">导师地图</a><a href="papers.html">论文库</a><a href="/tools">抓取与订阅</a></nav>
  <span class="built">数据更新：__BUILT__</span>
  <button id="theme" title="切换深浅色">◐</button>
</header>
<section class="intro">
  <div><div class="kicker">RESEARCH GROUP FIELD GUIDE</div><h1>先找对老师，再顺着研究脉络读论文。</h1></div>
  <p class="scope">当前范围聚焦 VLA、机器人学习、世界模型与安全保障。只收录可由高校或个人主页核验的 PI；论文数量仅代表本站已有记录，不等于完整发表量。</p>
</section>
<div class="controls">
  <input id="q" type="search" placeholder="搜索导师或学校…" aria-label="搜索导师或学校">
  <select id="f-region" aria-label="按地区筛选"><option value="">地区：全部</option></select>
  <select id="f-school" aria-label="按学校筛选"><option value="">学校：全部</option></select>
</div>
<section class="directory">
  <aside class="topics"><h2>研究方向</h2><div class="topic-list" id="topic-list"></div></aside>
  <main>
    <div class="result-head"><h2>导师目录</h2><span id="count"></span></div>
    <div id="list"></div>
  </main>
</section>
</div>
<script>
const PAPERS = __INDEX__;
const FACULTY = __FACULTY__;
const TAX = __TAXONOMY__;
let activeTopic = '';

const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

const relevantTopics = [...new Set(FACULTY.flatMap(f => f.topics))];
function fillSelect(id, values) {
  for (const value of values) {
    const option = document.createElement('option'); option.value = value; option.textContent = value; $(id).append(option);
  }
}
fillSelect('f-region', [...new Set(FACULTY.map(f=>f.region))].sort());
fillSelect('f-school', [...new Set(FACULTY.map(f=>f.institution))].sort());
for (const topic of ['', ...relevantTopics]) {
  const button = document.createElement('button');
  button.className = 'topic';
  button.dataset.topic = topic;
  button.textContent = topic ? TAX[topic] || topic : '全部方向';
  button.onclick = () => { activeTopic = topic; render(); };
  $('topic-list').append(button);
}

function papersFor(faculty) {
  const names = [faculty.name, ...(faculty.aliases || [])].map(n => n.toLowerCase());
  return PAPERS.filter(p => names.some(name => String(p.authors || '').toLowerCase().includes(name)));
}

function render() {
  const q = $('q').value.trim().toLowerCase();
  const region = $('f-region').value, school = $('f-school').value;
  const faculty = FACULTY.filter(f =>
    (!activeTopic || f.topics.includes(activeTopic)) &&
    (!region || f.region === region) && (!school || f.institution === school) &&
    (!q || `${f.name} ${f.institution}`.toLowerCase().includes(q)))
    .sort((a,b) => a.institution.localeCompare(b.institution) || a.name.localeCompare(b.name));
  $('count').textContent = `${faculty.length} 位 · ${new Set(faculty.map(f=>f.institution)).size} 所学校`;
  document.querySelectorAll('.topic').forEach(b => b.classList.toggle('on', b.dataset.topic === activeTopic));
  $('list').innerHTML = '';
  for (const f of faculty) {
    const papers = papersFor(f);
    const row = document.createElement('article');
    row.className = 'faculty';
    row.innerHTML = `<div class="avatar">${esc(f.name.split(/\\s+/).map(v=>v[0]).slice(0,2).join(''))}</div>
      <div class="identity"><h3>${esc(f.name)}</h3><p>${esc(f.institution)} · ${esc(f.region)}</p>
      <a href="${esc(f.homepage)}" target="_blank" rel="noopener">导师主页 ↗</a></div>
      <div class="faculty-main"><div class="chips">${f.topics.map(t=>`<span class="chip">${esc(TAX[t]||t)}</span>`).join('')}</div>
      <p class="evidence">本站收录 ${papers.length} 篇相关论文</p>
      <div class="paper-links">${papers.slice(0,2).map(p=>`<a href="paper.html?id=${encodeURIComponent(p.id)}">${esc(p.title)} →</a>`).join('')}</div></div>`;
    $('list').append(row);
  }
  if (!faculty.length) $('list').innerHTML = '<p class="empty">没有匹配的导师。</p>';
}

$('q').addEventListener('input', render);
for (const id of ['f-region','f-school']) $(id).addEventListener('input', render);

$('theme').addEventListener('click', () => {
  const cur = document.documentElement.dataset.theme ||
    (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  const next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  localStorage.setItem('theme', next);
});
const saved = localStorage.getItem('theme');
if (saved) document.documentElement.dataset.theme = saved;

render();
</script>
</body>
</html>
"""

PAPERS_TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>论文库 · paper-radar</title>
<meta name="description" content="按主题、来源和年份浏览 paper-radar 收录的论文">
<style>
:root { --bg:#f5f7fb; --surface:#fff; --ink:#17223b; --muted:#65708a; --accent:#2546d8; --accent-soft:#e9edff; --signal:#e14a2b; --border:#dce2ee; }
@media (prefers-color-scheme:dark) { :root { --bg:#0c1220; --surface:#151d2f; --ink:#f3f6ff; --muted:#a9b2c7; --accent:#8ea2ff; --accent-soft:#202b52; --signal:#ff8065; --border:#293550; } }
:root[data-theme="light"] { --bg:#f5f7fb; --surface:#fff; --ink:#17223b; --muted:#65708a; --accent:#2546d8; --accent-soft:#e9edff; --signal:#e14a2b; --border:#dce2ee; }
:root[data-theme="dark"] { --bg:#0c1220; --surface:#151d2f; --ink:#f3f6ff; --muted:#a9b2c7; --accent:#8ea2ff; --accent-soft:#202b52; --signal:#ff8065; --border:#293550; }
* { box-sizing:border-box; margin:0; }
body { background:var(--bg); color:var(--ink); font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif; }
button,input,select { font:inherit; }
.wrap { max-width:1080px; margin:auto; padding:0 24px 80px; }
.topbar { height:72px; display:flex; align-items:center; gap:18px; border-bottom:1px solid var(--border); }
.brand { font-weight:800; letter-spacing:-.02em; white-space:nowrap; }.brand span { color:var(--signal); }
.site-nav { display:flex; gap:4px; }.site-nav a { color:var(--muted); text-decoration:none; padding:6px 10px; border-radius:8px; font-size:14px; }
.site-nav a:hover,.site-nav a.on { color:var(--accent); background:var(--accent-soft); }
.built { color:var(--muted); font-size:13px; margin-left:auto; white-space:nowrap; }
#theme { background:var(--surface); border:1px solid var(--border); border-radius:999px; color:var(--muted); cursor:pointer; padding:4px 11px; }
.intro { padding:44px 0 30px; display:grid; grid-template-columns:minmax(0,1.2fr) minmax(240px,.8fr); gap:44px; align-items:end; }
.kicker { color:var(--signal); font-size:13px; font-weight:800; letter-spacing:.12em; }
h1 { font-size:clamp(38px,6vw,68px); line-height:1.02; letter-spacing:-.055em; margin-top:10px; }
.scope { color:var(--muted); border-left:3px solid var(--accent); padding-left:16px; }
.filters { position:sticky; top:0; z-index:3; background:color-mix(in srgb,var(--bg) 92%,transparent); backdrop-filter:blur(12px); padding:16px 0; display:flex; flex-wrap:wrap; gap:10px; border-bottom:1px solid var(--border); }
.filters input,.filters select { background:var(--surface); color:var(--ink); border:1px solid var(--border); border-radius:10px; padding:10px 13px; }
.filters input { flex:1; min-width:220px; }
.result-head { display:flex; justify-content:space-between; align-items:baseline; gap:20px; padding:28px 0 10px; border-bottom:1px solid var(--ink); }
.result-head h2 { font-size:24px; }.result-head span { color:var(--muted); font-size:14px; }
.paper { display:grid; grid-template-columns:100px minmax(0,1fr); gap:22px; padding:22px 4px; border-bottom:1px solid var(--border); }
.date { color:var(--muted); font-size:13px; padding-top:4px; }
.paper h3 { font-size:19px; line-height:1.35; }.paper h3 a { color:var(--ink); text-decoration:none; }.paper h3 a:hover { color:var(--accent); }
.meta { color:var(--muted); font-size:14px; margin:5px 0 10px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.chips { display:flex; flex-wrap:wrap; gap:6px; }.chip { color:var(--accent); background:var(--accent-soft); border-radius:999px; padding:3px 9px; font-size:12px; }
.links { margin-top:10px; display:flex; gap:16px; }.links a { color:var(--accent); text-decoration:none; font-size:13px; }
#loadmore { display:block; margin:24px auto; padding:9px 22px; color:var(--accent); background:var(--surface); border:1px solid var(--border); border-radius:9px; cursor:pointer; }
.empty { color:var(--muted); padding:48px 0; }
@media (max-width:720px) { .wrap{padding:0 16px 60px}.built{display:none}.intro{grid-template-columns:1fr;gap:20px;padding:32px 0 22px}.paper{grid-template-columns:1fr;gap:6px}.topbar{gap:8px}.brand{font-size:14px}.site-nav a{padding:5px 7px}.filters select{flex:1}.date{padding:0} }
</style>
</head>
<body>
<div class="wrap">
<header class="topbar">
  <div class="brand">paper<span>radar</span> / 论文库</div>
  <nav class="site-nav" aria-label="主导航"><a href="index.html">导师地图</a><a class="on" href="papers.html">论文库</a><a href="/tools">抓取与订阅</a></nav>
  <span class="built">数据更新：__BUILT__</span><button id="theme" aria-label="切换深浅色">◐</button>
</header>
<section class="intro">
  <div><div class="kicker">RESEARCH PAPER LIBRARY</div><h1>从论文回到研究脉络。</h1></div>
  <p class="scope">汇总每日自动抓取与人工精读记录。可按主题、来源和年份筛选，并进入每篇论文的结构化详情页。</p>
</section>
<div class="filters">
  <input id="q" type="search" placeholder="搜索标题或作者…" aria-label="搜索论文">
  <select id="f-topic"><option value="">主题：全部</option></select>
  <select id="f-source"><option value="">来源：全部</option><option value="curated">精读整理</option><option value="auto">自动抓取</option></select>
  <select id="f-year"><option value="">年份：全部</option></select>
</div>
<div class="result-head"><h2>论文目录</h2><span id="count"></span></div>
<main id="list"></main><button id="loadmore" hidden>加载更多</button>
</div>
<script>
const PAPERS = __INDEX__;
const TAX = __TAXONOMY__;
const PAGE = 100;
let filtered = PAPERS, shown = 0;
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

function addOptions(id, values, label) {
  for (const value of values) { const o=document.createElement('option'); o.value=value; o.textContent=label ? label(value) : value; $(id).append(o); }
}
addOptions('f-topic', [...new Set(PAPERS.flatMap(p=>p.topics||[]))].sort(), v=>TAX[v]||v);
addOptions('f-year', [...new Set(PAPERS.map(p=>p.year).filter(Boolean))].sort((a,b)=>b-a));

function chips(p) {
  const values = [...(p.topics||[]).map(t=>TAX[t]||t), p.keyword, p.category].filter(Boolean);
  return (p.source==='curated' ? '<span class="chip">精读整理</span>' : '') + values.map(v=>`<span class="chip">${esc(v)}</span>`).join('');
}
function renderMore() {
  const frag=document.createDocumentFragment();
  for (const p of filtered.slice(shown,shown+PAGE)) {
    const el=document.createElement('article'); el.className='paper';
    el.innerHTML=`<div class="date">${esc(p.date||p.year||'日期未记录')}</div><div><h3><a href="paper.html?id=${encodeURIComponent(p.id)}">${esc(p.title)}</a></h3><div class="meta">${esc(p.authors||'作者未记录')}</div><div class="chips">${chips(p)}</div><div class="links"><a href="paper.html?id=${encodeURIComponent(p.id)}">结构化详情 →</a>${p.url?`<a href="${esc(p.url)}" target="_blank" rel="noopener">原文 ↗</a>`:''}</div></div>`;
    frag.append(el);
  }
  shown=Math.min(shown+PAGE,filtered.length); $('list').append(frag); $('loadmore').hidden=shown>=filtered.length;
}
function applyFilters() {
  const q=$('q').value.trim().toLowerCase(), topic=$('f-topic').value, source=$('f-source').value, year=$('f-year').value;
  filtered=PAPERS.filter(p=>(!q||`${p.title} ${p.authors||''}`.toLowerCase().includes(q))&&(!topic||(p.topics||[]).includes(topic))&&(!source||(source==='auto'?p.source!=='curated':p.source===source))&&(!year||String(p.year)===year));
  $('count').textContent=`${filtered.length} / ${PAPERS.length} 篇`; $('list').innerHTML=''; shown=0;
  if (filtered.length) renderMore(); else $('list').innerHTML='<p class="empty">没有匹配的论文。</p>';
}
for (const id of ['q','f-topic','f-source','f-year']) $(id).addEventListener('input',applyFilters);
$('loadmore').addEventListener('click',renderMore);
$('theme').addEventListener('click',()=>{ const cur=document.documentElement.dataset.theme||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'); const next=cur==='dark'?'light':'dark'; document.documentElement.dataset.theme=next; localStorage.setItem('theme',next); });
const saved=localStorage.getItem('theme'); if(saved) document.documentElement.dataset.theme=saved;
applyFilters();
</script>
</body>
</html>
"""

DETAIL_TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paper · paper-radar</title>
<meta id="description" name="description" content="Structured literature-review page for one research paper">
<meta id="og-title" property="og:title" content="Paper · paper-radar">
<meta id="og-description" property="og:description" content="Structured literature-review page for one research paper">
<meta name="twitter:card" content="summary">
<meta id="twitter-title" name="twitter:title" content="Paper · paper-radar">
<meta id="twitter-description" name="twitter:description" content="Structured literature-review page for one research paper">
<style>
:root { --bg:#f4f2ed; --surface:#fff; --ink:#17211c; --muted:#68736d; --accent:#087a5b; --soft:#e4f1ea; --border:#d9ded9; --warn:#8a5a16; }
@media (prefers-color-scheme:dark) { :root { --bg:#101512; --surface:#18201c; --ink:#f2f4f2; --muted:#a9b2ad; --accent:#5dd3aa; --soft:#20382f; --border:#334039; --warn:#efbd70; } }
:root[data-theme="light"] { --bg:#f4f2ed; --surface:#fff; --ink:#17211c; --muted:#68736d; --accent:#087a5b; --soft:#e4f1ea; --border:#d9ded9; --warn:#8a5a16; }
:root[data-theme="dark"] { --bg:#101512; --surface:#18201c; --ink:#f2f4f2; --muted:#a9b2ad; --accent:#5dd3aa; --soft:#20382f; --border:#334039; --warn:#efbd70; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink); font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif; }
a { color:var(--accent); }
.wrap { max-width:1120px; margin:auto; padding:24px 20px 80px; }
.topbar { display:flex; justify-content:space-between; gap:16px; align-items:center; margin-bottom:42px; }
.back { color:var(--ink); text-decoration:none; font-weight:650; }
#theme { border:1px solid var(--border); border-radius:999px; color:var(--muted); background:var(--surface); padding:5px 11px; cursor:pointer; }
.eyebrow { color:var(--accent); font-size:13px; font-weight:750; letter-spacing:.08em; text-transform:uppercase; }
h1 { max-width:920px; margin:10px 0 14px; font-size:clamp(30px,5vw,58px); line-height:1.08; letter-spacing:-.035em; }
.byline { color:var(--muted); max-width:900px; }
.meta { display:flex; flex-wrap:wrap; gap:8px; margin:20px 0 30px; }
.chip { border:1px solid var(--border); border-radius:999px; background:var(--surface); color:var(--muted); padding:4px 10px; font-size:13px; }
.boundary { border-left:3px solid var(--accent); background:var(--soft); padding:12px 15px; margin:0 0 22px; color:var(--muted); }
.grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; }
.card { min-width:0; background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:22px; }
.card.wide { grid-column:1/-1; }
.card h2 { color:var(--muted); font-size:13px; letter-spacing:.06em; text-transform:uppercase; margin:0 0 10px; }
.card p { margin:0; white-space:pre-wrap; overflow-wrap:anywhere; }
.card ol { margin:0; padding-left:22px; }
.card li + li { margin-top:8px; }
.method-grid { display:grid; grid-template-columns:1.1fr .9fr; gap:18px; align-items:stretch; }
.figure-gap { display:flex; min-height:180px; flex-direction:column; justify-content:center; border:1px dashed var(--border); border-radius:10px; padding:22px; color:var(--muted); background:var(--bg); }
.figure-gap strong { color:var(--warn); margin-bottom:5px; }
.sources { display:grid; gap:8px; }
.sources a { overflow-wrap:anywhere; }
.missing { color:var(--muted); font-style:italic; }
.error { margin:15vh auto; max-width:640px; text-align:center; }
@media (max-width:760px) { .wrap{padding:18px 14px 60px}.topbar{margin-bottom:28px}.grid,.method-grid{grid-template-columns:1fr}.card.wide{grid-column:auto}.card{padding:18px} }
</style>
</head>
<body>
<main class="wrap" id="page" hidden>
  <nav class="topbar"><a class="back" href="papers.html">← 论文库</a><a href="index.html">导师地图</a><a href="/tools">抓取与订阅</a><button id="theme" aria-label="切换深浅色">◐</button></nav>
  <header>
    <div class="eyebrow" id="role"></div>
    <h1 id="title"></h1>
    <div class="byline" id="authors"></div>
    <div class="meta" id="meta"></div>
  </header>
  <div class="boundary" id="boundary"></div>
  <div class="grid">
    <section class="card"><h2>What it does</h2><p id="what"></p></section>
    <section class="card"><h2>Problem / motivation</h2><p id="problem"></p></section>
    <section class="card wide"><h2>Difference</h2><p id="difference"></p></section>
    <section class="card wide method-grid">
      <div><h2>Method in one glance</h2><ol id="method"></ol></div>
      <div class="figure-gap"><strong>Original paper diagram</strong><span id="figure-note"></span><a id="pdf-link" target="_blank" rel="noopener" hidden>Open source PDF ↗</a></div>
    </section>
    <section class="card"><h2>Evidence</h2><ol id="evidence"></ol></section>
    <section class="card"><h2>Take-away</h2><p id="takeaway"></p></section>
    <section class="card wide"><h2>Sources</h2><div class="sources" id="sources"></div></section>
  </div>
</main>
<div class="error" id="error" hidden><h1>找不到这篇论文</h1><p>请回到论文列表重新打开。</p><a href="papers.html">返回论文库</a></div>
<script>
const REVIEWS = __REVIEWS__;
const TAX = __TAXONOMY__;
const $ = id => document.getElementById(id);
const missing = '当前记录中没有可核验的内容。';

function text(id, value) {
  const el = $(id); el.textContent = value || missing;
  el.classList.toggle('missing', !value);
}
function list(id, values) {
  const el = $(id); el.innerHTML = '';
  for (const value of values?.length ? values : [missing]) {
    const li = document.createElement('li'); li.textContent = value;
    if (value === missing) li.className = 'missing';
    el.append(li);
  }
}
function cleanSummary(value) {
  return String(value || '').replace(/^#+\\s.*$/gm,'').replace(/[*_`>#-]/g,' ').replace(/\\s+/g,' ').trim();
}
function clip(value, length=520) {
  const s = cleanSummary(value); return s.length > length ? s.slice(0,length).trimEnd() + '…' : s;
}
function pdfUrl(url) {
  const match = String(url || '').match(new RegExp('https?://(?:www[.])?arxiv[.]org/abs/([^?#]+)', 'i'));
  return match ? `https://arxiv.org/pdf/${match[1]}` : '';
}
function chip(value) {
  if (!value) return;
  const el = document.createElement('span'); el.className = 'chip'; el.textContent = value; $('meta').append(el);
}
function source(label, url) {
  if (!url) return;
  const a = document.createElement('a'); a.href = url; a.target = '_blank'; a.rel = 'noopener'; a.textContent = `${label}: ${url}`; $('sources').append(a);
}

async function load() {
  const id = new URLSearchParams(location.search).get('id');
  if (!id) throw new Error('missing id');
  const response = await fetch(`papers/${encodeURIComponent(id)}.json`);
  if (!response.ok) throw new Error('paper not found');
  const paper = await response.json();
  const review = REVIEWS[id] || {};
  const fallback = clip(paper.summary || paper.abstract);
  const topics = (paper.topics || []).map(t => TAX[t] || t);

  document.title = `${paper.title} · paper-radar`;
  const description = review.what || fallback || 'Structured literature-review page for one research paper';
  for (const id of ['description','og-description','twitter-description']) $(id).content = description;
  for (const id of ['og-title','twitter-title']) $(id).content = paper.title || id;
  $('title').textContent = paper.title || id;
  $('authors').textContent = paper.authors || 'Authors not recorded';
  $('role').textContent = paper.category || topics[0] || 'Research paper';
  chip(paper.venue || (String(paper.url || '').includes('arxiv.org') ? 'arXiv' : 'Venue not recorded'));
  chip(paper.date || paper.year || 'Date not recorded');
  chip(paper.affiliations || 'Affiliations not recorded');
  for (const topic of topics) chip(topic);

  $('boundary').textContent = review.source_note
    ? 'Evidence level: curated local paper note. Claims below are drawn from that note and the linked primary record.'
    : 'Evidence level: abstract / automatic-summary record only. Method differences, exact results, affiliations, and guarantee boundaries still require paper-level verification.';
  text('what', review.what || fallback);
  text('problem', review.problem || clip(paper.abstract));
  text('difference', review.difference);
  list('method', review.method);
  list('evidence', review.evidence);
  text('takeaway', review.takeaway || (fallback ? `${fallback}\n\nLimitation: not independently verified from the full paper.` : ''));

  const pdf = pdfUrl(paper.url);
  $('figure-note').textContent = 'No verified figure crop is stored for this record. The site does not fabricate a substitute.';
  if (pdf) { $('pdf-link').href = pdf; $('pdf-link').hidden = false; }
  source('Paper record', paper.url);
  source('Paper PDF / figure source', pdf);
  if (review.source_note) {
    const span = document.createElement('span'); span.textContent = `Local review note: ${review.source_note}`; $('sources').append(span);
  }
  $('page').hidden = false;
}

$('theme').addEventListener('click', () => {
  const cur = document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme:dark)').matches ? 'dark':'light');
  const next = cur === 'dark' ? 'light':'dark'; document.documentElement.dataset.theme = next; localStorage.setItem('theme', next);
});
const saved = localStorage.getItem('theme'); if (saved) document.documentElement.dataset.theme = saved;
load().catch(() => { $('error').hidden = false; });
</script>
</body>
</html>
"""

INDEX_FIELDS = ("id", "title", "authors", "date", "year", "url", "keyword",
                "category", "source", "status", "topics", "hf_upvotes")


def sections(markdown):
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", markdown, re.MULTILINE))
    return {m.group(1).strip().lower(): markdown[m.end():matches[i + 1].start()
                                                     if i + 1 < len(matches) else len(markdown)].strip()
            for i, m in enumerate(matches)}


def block_points(block, limit=3):
    """Turn one Markdown section into a few readable, plain-text points."""
    if not block:
        return []
    points, paragraph, in_fence = [], [], False
    for raw in block.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or line.startswith(("#", "![", "$$")):
            continue
        line = re.sub(r"\[\[([^]|]+\|)?([^]]+)\]\]", r"\2", line)
        line = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", line)
        line = re.sub(r"[*_`>]", "", line).strip()
        if line.lower().startswith(("implementation-level interpretation", "safety enforcement layer:",
                                    "safety scope:", "main interface to safe vla:")):
            continue
        is_bullet = re.match(r"^[-+]\s+", line)
        if not line or is_bullet:
            if paragraph:
                points.append(" ".join(paragraph))
                paragraph = []
            if is_bullet:
                points.append(re.sub(r"^[-+]\s+", "", line))
        else:
            paragraph.append(line)
    if paragraph:
        points.append(" ".join(paragraph))
    return [p[:700].rstrip() + ("…" if len(p) > 700 else "") for p in points if p][:limit]


def first_section(note_sections, *names, limit=3):
    for name in names:
        points = block_points(note_sections.get(name.lower()), limit)
        if points:
            return points
    return []


def review_from_note(paper):
    note_path = paper.get("note_path")
    if not note_path:
        return None
    path = REPO_ROOT / note_path
    if not path.is_file():
        return None
    note_sections = sections(path.read_text(encoding="utf-8"))
    summary = first_section(note_sections, "One-sentence Summary", "一句话总结", limit=1)
    problem = first_section(note_sections, "Motivation", "Problem Setting", "动机", "研究问题", limit=1)
    difference = first_section(note_sections, "Main Contributions", "主要贡献", limit=1)
    method = first_section(note_sections, "Methodology", "Method", "方法", limit=3)
    evidence = first_section(note_sections, "Experiments", "实验", limit=2)
    limitation = first_section(note_sections, "Limitations", "局限", limit=1)
    takeaway = "\n\n".join(summary + ([f"Limitation: {limitation[0]}"] if limitation else []))
    return {
        "what": summary[0] if summary else "",
        "problem": problem[0] if problem else "",
        "difference": difference[0] if difference else "",
        "method": method,
        "evidence": evidence,
        "takeaway": takeaway,
        "source_note": note_path,
    }


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
    if SOCIAL_IMAGE.is_file():
        shutil.copy2(SOCIAL_IMAGE, SITE_DIR / SOCIAL_IMAGE.name)

    taxonomy = json.loads((REPO_ROOT / "data" / "taxonomy.json").read_text(encoding="utf-8"))
    tax_names = {slug: v["name"] for slug, v in taxonomy.items()}
    reviews = {p["id"]: review for p in papers if (review := review_from_note(p))}

    html = TEMPLATE.replace("__BUILT__", time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()))
    html = html.replace("__INDEX__", json.dumps(index, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__FACULTY__", json.dumps(FACULTY, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__TAXONOMY__", json.dumps(tax_names, ensure_ascii=False, separators=(",", ":")))
    (SITE_DIR / "index.html").write_text(html, encoding="utf-8")
    papers_html = PAPERS_TEMPLATE.replace("__BUILT__", time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()))
    papers_html = papers_html.replace(
        "__INDEX__", json.dumps(index, ensure_ascii=False, separators=(",", ":")))
    papers_html = papers_html.replace(
        "__TAXONOMY__", json.dumps(tax_names, ensure_ascii=False, separators=(",", ":")))
    (SITE_DIR / "papers.html").write_text(papers_html, encoding="utf-8")
    detail_html = DETAIL_TEMPLATE.replace(
        "__REVIEWS__", json.dumps(reviews, ensure_ascii=False, separators=(",", ":")))
    detail_html = detail_html.replace(
        "__TAXONOMY__", json.dumps(tax_names, ensure_ascii=False, separators=(",", ":")))
    (SITE_DIR / "paper.html").write_text(detail_html, encoding="utf-8")
    print(f"✅ site/ 构建完成：导师地图、{len(papers)} 篇论文、{len(reviews)} 篇含精读主页内容")


if __name__ == "__main__":
    main()
