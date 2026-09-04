#!/usr/bin/env python3
"""把 data/papers/*.json 构建成静态论文站（site/）。

- site/index.html：导师地图
- site/faculty.html：导师方向与关联论文详情
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
from datetime import date
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
    {"name": "Calin Belta", "institution": "University of Maryland", "region": "美国", "homepage": "https://robotics.umd.edu/clark/facultydir", "topics": ["formal-methods", "cyber-physical-systems", "runtime-monitoring"]},
    {"name": "Sayan Mitra", "institution": "University of Illinois Urbana-Champaign", "region": "美国", "homepage": "https://mitras.ece.illinois.edu/", "topics": ["formal-methods", "runtime-monitoring", "safe-rl"]},
    {"name": "Somil Bansal", "institution": "USC", "region": "美国", "homepage": "https://sites.google.com/view/somilbansal", "topics": ["safe-rl", "formal-methods", "multimodal-perception"]},
    {"name": "Florian Shkurti", "institution": "University of Toronto", "region": "加拿大", "homepage": "https://www.cs.toronto.edu/~florian/", "topics": ["vla-models", "robot-manipulation", "embodied-benchmarks"]},
    {"name": "Igor Gilitschenski", "institution": "University of Toronto", "region": "加拿大", "homepage": "https://www.gilitschenski.org/", "topics": ["safe-rl", "world-model-control", "robot-manipulation"]},
    {"name": "Sanjit Seshia", "institution": "UC Berkeley", "region": "美国", "homepage": "https://www2.eecs.berkeley.edu/Faculty/Homepages/sseshia.html", "topics": ["formal-methods", "cyber-physical-systems", "runtime-monitoring"]},
    {"name": "Edward A. Lee", "aliases": ["Edward Lee"], "institution": "UC Berkeley", "region": "美国", "homepage": "https://ptolemy.berkeley.edu/~eal/", "topics": ["cyber-physical-systems", "formal-methods", "runtime-monitoring"]},
    {"name": "Murat Arcak", "institution": "UC Berkeley", "region": "美国", "homepage": "https://www2.eecs.berkeley.edu/Faculty/Homepages/arcak.html", "topics": ["cyber-physical-systems", "formal-methods", "safe-rl"]},
    {"name": "Anca Dragan", "institution": "UC Berkeley", "region": "美国", "homepage": "https://people.eecs.berkeley.edu/~anca/", "topics": ["robotics", "hri-human-in-loop", "safe-rl"]},
    {"name": "Ronald Fearing", "institution": "UC Berkeley", "region": "美国", "homepage": "https://www2.eecs.berkeley.edu/Faculty/Homepages/fearing.html", "topics": ["robotics", "robot-manipulation", "sim-to-real"]},
    {"name": "Mark Mueller", "institution": "UC Berkeley", "region": "美国", "homepage": "https://me.berkeley.edu/people/faculty/mark-mueller/", "topics": ["robotics", "world-model-control", "safe-rl"]},
    {"name": "Francesco Borrelli", "institution": "UC Berkeley", "region": "美国", "homepage": "https://me.berkeley.edu/people/faculty/francesco-borrelli/", "topics": ["cyber-physical-systems", "world-model-control", "safe-rl"]},
    {"name": "Oussama Khatib", "institution": "Stanford", "region": "美国", "homepage": "https://robotics.stanford.edu/~ok/", "topics": ["robotics", "robot-manipulation", "hri-human-in-loop"]},
    {"name": "Mac Schwager", "institution": "Stanford", "region": "美国", "homepage": "https://web.stanford.edu/~schwager/", "topics": ["robotics", "cyber-physical-systems", "world-model-control"]},
    {"name": "Karen Liu", "institution": "Stanford", "region": "美国", "homepage": "https://tml.stanford.edu/", "topics": ["robotics", "world-model-learning", "robot-manipulation"]},
    {"name": "Fei-Fei Li", "institution": "Stanford", "region": "美国", "homepage": "https://profiles.stanford.edu/fei-fei-li", "topics": ["vla-models", "multimodal-perception", "embodied-benchmarks"]},
    {"name": "Harry Asada", "institution": "MIT", "region": "美国", "homepage": "https://robotics.mit.edu/people/harry-asada", "topics": ["robotics", "robot-manipulation", "hri-human-in-loop"]},
    {"name": "Navid Azizan", "institution": "MIT", "region": "美国", "homepage": "https://robotics.mit.edu/people/navid-azizan", "topics": ["world-model-learning", "world-model-control", "safe-rl"]},
    {"name": "Andreea Bobu", "institution": "MIT", "region": "美国", "homepage": "https://robotics.mit.edu/people/andreea-bobu", "topics": ["robotics", "hri-human-in-loop", "safe-rl"]},
    {"name": "Domitilla Del Vecchio", "institution": "MIT", "region": "美国", "homepage": "https://robotics.mit.edu/people/domitilla-del-vecchio", "topics": ["cyber-physical-systems", "formal-methods", "runtime-monitoring"]},
    {"name": "Kevin Chen", "institution": "MIT", "region": "美国", "homepage": "https://robotics.mit.edu/people/kevin-chen", "topics": ["robotics", "robot-manipulation", "sim-to-real"]},
    {"name": "Alberto Rodriguez", "institution": "MIT", "region": "美国", "homepage": "https://robotics.mit.edu/people/alberto-rodriguez", "topics": ["robot-manipulation", "robotics", "multimodal-perception"]},
    {"name": "Nicholas Roy", "aliases": ["Nick Roy"], "institution": "MIT", "region": "美国", "homepage": "https://robotics.mit.edu/people/nicholas-roy", "topics": ["robotics", "world-model-control", "safe-rl"]},
    {"name": "Julie Shah", "institution": "MIT", "region": "美国", "homepage": "https://robotics.mit.edu/people/julie-shah", "topics": ["robotics", "hri-human-in-loop", "safe-rl"]},
    {"name": "Brian Williams", "institution": "MIT", "region": "美国", "homepage": "https://robotics.mit.edu/people/brian-williams", "topics": ["formal-methods", "llm-planning", "cyber-physical-systems"]},
    {"name": "Henny Admoni", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.ri.cmu.edu/ri-faculty/henny-admoni/", "topics": ["robotics", "hri-human-in-loop", "robot-manipulation"]},
    {"name": "Chris Atkeson", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.ri.cmu.edu/ri-faculty/christopher-atkeson/", "topics": ["robotics", "robot-manipulation", "safe-rl"]},
    {"name": "Howie Choset", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.ri.cmu.edu/ri-faculty/howie-choset/", "topics": ["robotics", "llm-planning", "robot-manipulation"]},
    {"name": "Zackory Erickson", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.ri.cmu.edu/ri-faculty/zackory-erickson/", "topics": ["robot-manipulation", "hri-human-in-loop", "safe-rl"]},
    {"name": "Martial Hebert", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.ri.cmu.edu/ri-faculty/martial-hebert/", "topics": ["robotics", "multimodal-perception", "embodied-benchmarks"]},
    {"name": "Jeffrey Ichnowski", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.ri.cmu.edu/ri-faculty/jeffrey-ichnowski/", "topics": ["robot-manipulation", "llm-planning", "sim-to-real"]},
    {"name": "Michael Kaess", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.ri.cmu.edu/ri-faculty/michael-kaess/", "topics": ["robotics", "multimodal-perception", "world-model-control"]},
    {"name": "Reid Simmons", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.ri.cmu.edu/ri-faculty/reid-simmons/", "topics": ["formal-methods", "runtime-monitoring", "robotics"]},
    {"name": "Maxim Likhachev", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.ri.cmu.edu/ri-faculty/maxim-likhachev/", "topics": ["robotics", "llm-planning", "robot-manipulation"]},
    {"name": "Sebastian Scherer", "institution": "Carnegie Mellon", "region": "美国", "homepage": "https://www.ri.cmu.edu/ri-faculty/sebastian-scherer/", "topics": ["robotics", "safe-rl", "multimodal-perception"]},
    {"name": "Radhika Nagpal", "institution": "Princeton", "region": "美国", "homepage": "https://engineering.princeton.edu/faculty/radhika-nagpal", "topics": ["robotics", "cyber-physical-systems", "hri-human-in-loop"]},
    {"name": "Karthik Narasimhan", "institution": "Princeton", "region": "美国", "homepage": "https://www.cs.princeton.edu/people/profile/karthikn", "topics": ["llm-agents", "vla-models", "embodied-benchmarks"]},
    {"name": "Henrik Christensen", "institution": "UC San Diego", "region": "美国", "homepage": "https://cri.ucsd.edu/faculty", "topics": ["robotics", "robot-manipulation", "embodied-benchmarks"]},
    {"name": "Sicun Gao", "institution": "UC San Diego", "region": "美国", "homepage": "https://cri.ucsd.edu/faculty", "topics": ["formal-methods", "cyber-physical-systems", "runtime-monitoring"]},
    {"name": "Laurel Riek", "institution": "UC San Diego", "region": "美国", "homepage": "https://cri.ucsd.edu/faculty", "topics": ["robotics", "hri-human-in-loop", "embodied-benchmarks"]},
    {"name": "Hao Su", "institution": "UC San Diego", "region": "美国", "homepage": "https://cri.ucsd.edu/faculty", "topics": ["vla-models", "robot-manipulation", "multimodal-perception"], "auto_match": False},
    {"name": "Nikolay Atanasov", "institution": "UC San Diego", "region": "美国", "homepage": "https://cri.ucsd.edu/faculty", "topics": ["robotics", "world-model-control", "safe-rl"]},
    {"name": "Michael Yip", "institution": "UC San Diego", "region": "美国", "homepage": "https://cri.ucsd.edu/faculty", "topics": ["robotics", "robot-manipulation", "hri-human-in-loop"]},
    {"name": "Yang Zheng", "institution": "UC San Diego", "region": "美国", "homepage": "https://cri.ucsd.edu/faculty", "topics": ["cyber-physical-systems", "world-model-control", "safe-rl"], "auto_match": False},
    {"name": "Maya Cakmak", "institution": "University of Washington", "region": "美国", "homepage": "https://robotics.cs.washington.edu/", "topics": ["robotics", "hri-human-in-loop", "robot-manipulation"]},
    {"name": "Sonia Chernova", "institution": "Georgia Tech", "region": "美国", "homepage": "https://research.gatech.edu/irim/faculty-list", "topics": ["robotics", "hri-human-in-loop", "llm-agents"]},
    {"name": "Samuel Coogan", "institution": "Georgia Tech", "region": "美国", "homepage": "https://research.gatech.edu/irim/faculty-list", "topics": ["cyber-physical-systems", "formal-methods", "safe-rl"]},
    {"name": "Frank Dellaert", "institution": "Georgia Tech", "region": "美国", "homepage": "https://research.gatech.edu/irim/faculty-list", "topics": ["robotics", "world-model-control", "multimodal-perception"]},
    {"name": "Animesh Garg", "institution": "Georgia Tech", "region": "美国", "homepage": "https://research.gatech.edu/irim/faculty-list", "topics": ["vla-models", "robot-manipulation", "world-model-learning"]},
    {"name": "Matthew Gombolay", "institution": "Georgia Tech", "region": "美国", "homepage": "https://research.gatech.edu/irim/faculty-list", "topics": ["robotics", "hri-human-in-loop", "safe-rl"]},
    {"name": "Harish Ravichandar", "institution": "Georgia Tech", "region": "美国", "homepage": "https://people.research.gatech.edu/harish-ravichandar", "topics": ["robotics", "hri-human-in-loop", "safe-rl"]},
    {"name": "Roberto Martin-Martin", "institution": "UT Austin", "region": "美国", "homepage": "https://robotics.utexas.edu/people", "topics": ["vla-models", "robot-manipulation", "multimodal-perception"]},
    {"name": "Chenfeng Xu", "institution": "UT Austin", "region": "美国", "homepage": "https://www.cs.utexas.edu/research/intelligent-robotics", "topics": ["vla-models", "robot-manipulation", "multimodal-perception"]},
    {"name": "David Fridovich-Keil", "institution": "UT Austin", "region": "美国", "homepage": "https://robotics.utexas.edu/people", "topics": ["robotics", "safe-rl", "world-model-control"]},
    {"name": "Luis Sentis", "institution": "UT Austin", "region": "美国", "homepage": "https://robotics.utexas.edu/people", "topics": ["robotics", "robot-manipulation", "hri-human-in-loop"]},
    {"name": "Stephanie Gil", "institution": "Harvard", "region": "美国", "homepage": "https://seas.harvard.edu/robotics/robotics-core-faculty", "topics": ["robotics", "cyber-physical-systems", "safe-rl"]},
    {"name": "Heng Yang", "institution": "Harvard", "region": "美国", "homepage": "https://hankyang.seas.harvard.edu/", "topics": ["formal-methods", "robotics", "safe-rl"], "auto_match": False},
    {"name": "Robert Wood", "institution": "Harvard", "region": "美国", "homepage": "https://seas.harvard.edu/robotics/robotics-core-faculty", "topics": ["robotics", "sim-to-real", "robot-manipulation"]},
    {"name": "Robert Howe", "institution": "Harvard", "region": "美国", "homepage": "https://seas.harvard.edu/robotics/robotics-core-faculty", "topics": ["robotics", "robot-manipulation", "hri-human-in-loop"]},
    {"name": "Rajeev Alur", "institution": "University of Pennsylvania", "region": "美国", "homepage": "https://precise.seas.upenn.edu/people/faculty", "topics": ["formal-methods", "cyber-physical-systems", "runtime-monitoring"]},
    {"name": "Insup Lee", "institution": "University of Pennsylvania", "region": "美国", "homepage": "https://precise.seas.upenn.edu/people/faculty", "topics": ["formal-methods", "cyber-physical-systems", "runtime-monitoring"]},
    {"name": "Oleg Sokolsky", "institution": "University of Pennsylvania", "region": "美国", "homepage": "https://precise.seas.upenn.edu/people/faculty", "topics": ["formal-methods", "cyber-physical-systems", "runtime-monitoring"]},
    {"name": "Linh Thi Xuan Phan", "aliases": ["Linh Phan"], "institution": "University of Pennsylvania", "region": "美国", "homepage": "https://precise.seas.upenn.edu/people/faculty", "topics": ["cyber-physical-systems", "formal-methods", "runtime-monitoring"]},
    {"name": "Ani Hsieh", "institution": "University of Pennsylvania", "region": "美国", "homepage": "https://www.grasp.upenn.edu/people/ani-hsieh/", "topics": ["robotics", "cyber-physical-systems", "world-model-control"]},
    {"name": "Mark Yim", "institution": "University of Pennsylvania", "region": "美国", "homepage": "https://www.grasp.upenn.edu/people/mark-yim/", "topics": ["robotics", "robot-manipulation", "sim-to-real"]},
    {"name": "Dinesh Jayaraman", "institution": "University of Pennsylvania", "region": "美国", "homepage": "https://www.seas.upenn.edu/~dineshj/", "topics": ["vla-models", "world-model-learning", "robot-manipulation"]},
    {"name": "Hadas Kress-Gazit", "institution": "Cornell", "region": "美国", "homepage": "https://robotics.cornell.edu/faculty/", "topics": ["formal-methods", "robotics", "llm-planning"]},
    {"name": "Guy Hoffman", "institution": "Cornell", "region": "美国", "homepage": "https://robotics.cornell.edu/faculty/", "topics": ["robotics", "hri-human-in-loop", "embodied-benchmarks"]},
    {"name": "Tapomayukh Bhattacharjee", "institution": "Cornell", "region": "美国", "homepage": "https://robotics.cornell.edu/faculty/", "topics": ["robot-manipulation", "hri-human-in-loop", "safe-rl"]},
    {"name": "Kirstin Petersen", "institution": "Cornell", "region": "美国", "homepage": "https://robotics.cornell.edu/faculty/", "topics": ["robotics", "cyber-physical-systems", "sim-to-real"]},
    {"name": "Silvia Ferrari", "institution": "Cornell", "region": "美国", "homepage": "https://robotics.cornell.edu/faculty/", "topics": ["robotics", "world-model-control", "safe-rl"]},
    {"name": "Sanjiban Choudhury", "institution": "Cornell", "region": "美国", "homepage": "https://robotics.cornell.edu/faculty/", "topics": ["robotics", "llm-planning", "safe-rl"]},
    {"name": "Matei Ciocarlie", "institution": "Columbia", "region": "美国", "homepage": "https://robotics.columbia.edu/content/faculty", "topics": ["robot-manipulation", "hri-human-in-loop", "safe-rl"]},
    {"name": "Yunzhu Li", "institution": "Columbia", "region": "美国", "homepage": "https://robotics.columbia.edu/content/faculty", "topics": ["world-model-learning", "robot-manipulation", "vla-models"]},
    {"name": "Peter Allen", "institution": "Columbia", "region": "美国", "homepage": "https://robotics.columbia.edu/content/faculty", "topics": ["robotics", "robot-manipulation", "multimodal-perception"]},
    {"name": "Hod Lipson", "institution": "Columbia", "region": "美国", "homepage": "https://robotics.columbia.edu/content/faculty", "topics": ["robotics", "world-model-learning", "sim-to-real"]},
    {"name": "Sunil Agrawal", "institution": "Columbia", "region": "美国", "homepage": "https://robotics.columbia.edu/content/faculty", "topics": ["robotics", "hri-human-in-loop", "robot-manipulation"]},
    {"name": "Tony Dear", "institution": "Columbia", "region": "美国", "homepage": "https://robotics.columbia.edu/content/faculty", "topics": ["robotics", "world-model-control", "safe-rl"]},
    {"name": "Necmiye Ozay", "institution": "University of Michigan", "region": "美国", "homepage": "https://robotics.umich.edu/people/faculty/", "topics": ["formal-methods", "cyber-physical-systems", "safe-rl"]},
    {"name": "Ram Vasudevan", "institution": "University of Michigan", "region": "美国", "homepage": "https://robotics.umich.edu/people/faculty/", "topics": ["robotics", "safe-rl", "world-model-control"]},
    {"name": "Chad Jenkins", "institution": "University of Michigan", "region": "美国", "homepage": "https://robotics.umich.edu/people/faculty/", "topics": ["robotics", "hri-human-in-loop", "embodied-benchmarks"]},
    {"name": "Dmitry Berenson", "institution": "University of Michigan", "region": "美国", "homepage": "https://robotics.umich.edu/people/faculty/", "topics": ["robot-manipulation", "llm-planning", "safe-rl"]},
    {"name": "Nima Fazeli", "institution": "University of Michigan", "region": "美国", "homepage": "https://robotics.umich.edu/people/faculty/", "topics": ["robot-manipulation", "world-model-learning", "multimodal-perception"]},
    {"name": "Dimitra Panagou", "institution": "University of Michigan", "region": "美国", "homepage": "https://robotics.umich.edu/people/faculty/", "topics": ["robotics", "safe-rl", "formal-methods"]},
    {"name": "Yulun Tian", "institution": "University of Michigan", "region": "美国", "homepage": "https://robotics.umich.edu/people/faculty/", "topics": ["robotics", "world-model-control", "formal-methods"]},
    {"name": "Maja Mataric", "aliases": ["Maja Matarić"], "institution": "USC", "region": "美国", "homepage": "https://rasc.usc.edu/faculty/", "topics": ["robotics", "hri-human-in-loop", "embodied-benchmarks"]},
    {"name": "Stefanos Nikolaidis", "institution": "USC", "region": "美国", "homepage": "https://rasc.usc.edu/faculty/", "topics": ["robotics", "hri-human-in-loop", "safe-rl"]},
    {"name": "Jyotirmoy Deshmukh", "aliases": ["Jyo Deshmukh"], "institution": "USC", "region": "美国", "homepage": "https://rasc.usc.edu/faculty/", "topics": ["formal-methods", "cyber-physical-systems", "runtime-monitoring"]},
    {"name": "Erdem Biyik", "aliases": ["Erdem Bıyık"], "institution": "USC", "region": "美国", "homepage": "https://rasc.usc.edu/faculty/", "topics": ["robotics", "hri-human-in-loop", "safe-rl"]},
    {"name": "Daniel Seita", "institution": "USC", "region": "美国", "homepage": "https://rasc.usc.edu/faculty/", "topics": ["robot-manipulation", "vla-models", "sim-to-real"]},
    {"name": "Gaurav Sukhatme", "institution": "USC", "region": "美国", "homepage": "https://rasc.usc.edu/faculty/", "topics": ["robotics", "world-model-control", "embodied-benchmarks"]},
    {"name": "Dinesh Manocha", "institution": "University of Maryland", "region": "美国", "homepage": "https://robotics.umd.edu/clark/facultydir", "topics": ["robotics", "llm-planning", "hri-human-in-loop"]},
    {"name": "Pratap Tokekar", "institution": "University of Maryland", "region": "美国", "homepage": "https://robotics.umd.edu/clark/facultydir", "topics": ["robotics", "world-model-control", "safe-rl"]},
    {"name": "Michael Otte", "institution": "University of Maryland", "region": "美国", "homepage": "https://robotics.umd.edu/clark/facultydir", "topics": ["robotics", "llm-planning", "safe-rl"]},
    {"name": "Derek Paley", "institution": "University of Maryland", "region": "美国", "homepage": "https://robotics.umd.edu/clark/facultydir", "topics": ["robotics", "cyber-physical-systems", "world-model-control"]},
    {"name": "Nikhil Chopra", "institution": "University of Maryland", "region": "美国", "homepage": "https://robotics.umd.edu/clark/facultydir", "topics": ["robotics", "cyber-physical-systems", "hri-human-in-loop"]},
    {"name": "Yiannis Aloimonos", "institution": "University of Maryland", "region": "美国", "homepage": "https://robotics.umd.edu/clark/facultydir", "topics": ["robotics", "multimodal-perception", "embodied-benchmarks"]},
    {"name": "Miroslav Pajic", "institution": "Duke", "region": "美国", "homepage": "https://robotics.duke.edu/faculty", "topics": ["formal-methods", "cyber-physical-systems", "runtime-monitoring"]},
    {"name": "Boyuan Chen", "institution": "Duke", "region": "美国", "homepage": "https://robotics.duke.edu/faculty", "topics": ["world-model-learning", "robot-manipulation", "robotics"]},
    {"name": "Michael Zavlanos", "institution": "Duke", "region": "美国", "homepage": "https://robotics.duke.edu/faculty", "topics": ["robotics", "cyber-physical-systems", "safe-rl"]},
    {"name": "Gregory Hager", "institution": "Johns Hopkins", "region": "美国", "homepage": "https://lcsr.jhu.edu/", "topics": ["robotics", "robot-manipulation", "hri-human-in-loop"]},
    {"name": "Marin Kobilarov", "institution": "Johns Hopkins", "region": "美国", "homepage": "https://asco.lcsr.jhu.edu/", "topics": ["robotics", "world-model-control", "safe-rl"]},
    {"name": "Mathias Unberath", "institution": "Johns Hopkins", "region": "美国", "homepage": "https://lcsr.jhu.edu/", "topics": ["robotics", "multimodal-perception", "hri-human-in-loop"]},
    {"name": "Axel Krieger", "institution": "Johns Hopkins", "region": "美国", "homepage": "https://lcsr.jhu.edu/", "topics": ["robotics", "robot-manipulation", "safe-rl"]},
    {"name": "George Konidaris", "institution": "Brown", "region": "美国", "homepage": "https://cs.brown.edu/people/gdk/", "topics": ["robotics", "world-model-learning", "llm-planning"]},
    {"name": "Brian Scassellati", "institution": "Yale", "region": "美国", "homepage": "https://robotsforgood.yale.edu/about/about-team", "topics": ["robotics", "hri-human-in-loop", "embodied-benchmarks"]},
    {"name": "Marynel Vazquez", "institution": "Yale", "region": "美国", "homepage": "https://robotsforgood.yale.edu/about/about-team", "topics": ["robotics", "hri-human-in-loop", "multimodal-perception"]},
    {"name": "Aaron Dollar", "institution": "Yale", "region": "美国", "homepage": "https://engineering.yale.edu/academic-study/departments/mechanical-engineering/research-areas", "topics": ["robotics", "robot-manipulation", "hri-human-in-loop"]},
    {"name": "Ludovic Righetti", "institution": "New York University", "region": "美国", "homepage": "https://engineering.nyu.edu/faculty/ludovic-righetti", "topics": ["robotics", "world-model-control", "safe-rl"]},
    {"name": "Chen Feng", "institution": "New York University", "region": "美国", "homepage": "https://engineering.nyu.edu/faculty/chen-feng", "topics": ["robotics", "multimodal-perception", "sim-to-real"]},
    {"name": "Nancy Amato", "institution": "University of Illinois Urbana-Champaign", "region": "美国", "homepage": "https://siebelschool.illinois.edu/about/people/faculty/namato", "topics": ["robotics", "llm-planning", "robot-manipulation"]},
    {"name": "Kris Hauser", "institution": "University of Illinois Urbana-Champaign", "region": "美国", "homepage": "https://siebelschool.illinois.edu/about/people/faculty/kkhauser", "topics": ["robotics", "robot-manipulation", "safe-rl"]},
    {"name": "Mattia Gazzola", "institution": "University of Illinois Urbana-Champaign", "region": "美国", "homepage": "https://mechanical.illinois.edu/directory/profile/mgazzola", "topics": ["robotics", "world-model-control", "sim-to-real"]},
    {"name": "Todd Murphey", "institution": "Northwestern", "region": "美国", "homepage": "https://robotics.northwestern.edu/people/faculty/", "topics": ["robotics", "world-model-control", "hri-human-in-loop"]},
    {"name": "Kevin Lynch", "institution": "Northwestern", "region": "美国", "homepage": "https://robotics.northwestern.edu/people/faculty/", "topics": ["robotics", "robot-manipulation", "cyber-physical-systems"]},
    {"name": "Brenna Argall", "institution": "Northwestern", "region": "美国", "homepage": "https://robotics.northwestern.edu/people/faculty/", "topics": ["robotics", "hri-human-in-loop", "safe-rl"]},
    {"name": "Sam Kriegman", "institution": "Northwestern", "region": "美国", "homepage": "https://robotics.northwestern.edu/people/faculty/", "topics": ["robotics", "world-model-learning", "sim-to-real"]},
    {"name": "Zachary Kingston", "institution": "Purdue", "region": "美国", "homepage": "https://www.cs.purdue.edu/research/robotics-computer-vision.html", "topics": ["robotics", "llm-planning", "robot-manipulation"]},
    {"name": "Ahmed Qureshi", "institution": "Purdue", "region": "美国", "homepage": "https://www.cs.purdue.edu/research/robotics-computer-vision.html", "topics": ["robotics", "llm-planning", "world-model-learning"]},
    {"name": "Rohan Paleja", "institution": "Purdue", "region": "美国", "homepage": "https://www.cs.purdue.edu/research/robotics-computer-vision.html", "topics": ["robotics", "hri-human-in-loop", "safe-rl"]},
    {"name": "Shreyas Sundaram", "institution": "Purdue", "region": "美国", "homepage": "https://engineering.purdue.edu/Initiatives/AutoSystems/Faculty", "topics": ["cyber-physical-systems", "formal-methods", "safe-rl"]},
    {"name": "Hai Lin", "institution": "University of Notre Dame", "region": "美国", "homepage": "https://wireless.nd.edu/people/faculty/hai-lin/", "topics": ["formal-methods", "cyber-physical-systems", "robotics"]},
    {"name": "Gabor Karsai", "institution": "Vanderbilt", "region": "美国", "homepage": "https://www.isis.vanderbilt.edu/people", "topics": ["formal-methods", "cyber-physical-systems", "runtime-monitoring"]},
    {"name": "Xenofon Koutsoukos", "institution": "Vanderbilt", "region": "美国", "homepage": "https://www.isis.vanderbilt.edu/people", "topics": ["cyber-physical-systems", "formal-methods", "safe-rl"]},
    {"name": "Taylor Johnson", "institution": "Vanderbilt", "region": "美国", "homepage": "https://www.isis.vanderbilt.edu/people", "topics": ["formal-methods", "cyber-physical-systems", "runtime-monitoring"]},
    {"name": "Aniruddha Gokhale", "institution": "Vanderbilt", "region": "美国", "homepage": "https://www.dre.vanderbilt.edu/~gokhale/", "topics": ["cyber-physical-systems", "runtime-monitoring", "formal-methods"]},
    {"name": "Morteza Lahijanian", "institution": "University of Colorado Boulder", "region": "美国", "homepage": "https://www.colorado.edu/aerospace/morteza-lahijanian", "topics": ["formal-methods", "robotics", "safe-rl"]},
    {"name": "Sriram Sankaranarayanan", "institution": "University of Colorado Boulder", "region": "美国", "homepage": "https://home.cs.colorado.edu/~srirams/", "topics": ["formal-methods", "cyber-physical-systems", "runtime-monitoring"]},
    {"name": "Majid Zamani", "institution": "University of Colorado Boulder", "region": "美国", "homepage": "https://experts.colorado.edu/display/fisid_164967", "topics": ["formal-methods", "cyber-physical-systems", "safe-rl"]},
    {"name": "Zachary Sunberg", "institution": "University of Colorado Boulder", "region": "美国", "homepage": "https://www.colorado.edu/aerospace/zachary-sunberg", "topics": ["robotics", "safe-rl", "world-model-control"]},
    {"name": "Alessandro Roncone", "institution": "University of Colorado Boulder", "region": "美国", "homepage": "https://www.colorado.edu/cs/alessandro-roncone", "topics": ["robotics", "hri-human-in-loop", "llm-planning"]},
    {"name": "Robert Platt", "institution": "Northeastern", "region": "美国", "homepage": "https://robotics.northeastern.edu/people/faculty/", "topics": ["robot-manipulation", "vla-models", "world-model-learning"]},
    {"name": "Christopher Amato", "institution": "Northeastern", "region": "美国", "homepage": "https://robotics.northeastern.edu/people/faculty/", "topics": ["robotics", "safe-rl", "world-model-control"]},
    {"name": "Taskin Padir", "institution": "Northeastern", "region": "美国", "homepage": "https://robotics.northeastern.edu/people/faculty/", "topics": ["robotics", "hri-human-in-loop", "robot-manipulation"]},
    {"name": "Devin Balkcom", "institution": "Dartmouth", "region": "美国", "homepage": "https://web.cs.dartmouth.edu/people/devin-balkcom", "topics": ["robotics", "robot-manipulation", "llm-planning"]},
    {"name": "Alberto Quattrini Li", "institution": "Dartmouth", "region": "美国", "homepage": "https://web.cs.dartmouth.edu/people/alberto-quattrini-li", "topics": ["robotics", "world-model-control", "multimodal-perception"]},
    {"name": "Berk Calli", "institution": "Worcester Polytechnic Institute", "region": "美国", "homepage": "https://www.wpi.edu/people/faculty/bcalli", "topics": ["robot-manipulation", "robotics", "multimodal-perception"]},
    {"name": "Carlo Pinciroli", "institution": "Worcester Polytechnic Institute", "region": "美国", "homepage": "https://www.wpi.edu/people/faculty/cpinciroli", "topics": ["robotics", "cyber-physical-systems", "sim-to-real"]},
    {"name": "Lu Feng", "institution": "University of Virginia", "region": "美国", "homepage": "https://engineering.virginia.edu/faculty/lu-feng", "topics": ["formal-methods", "cyber-physical-systems", "safe-rl"]},
    {"name": "Homa Alemzadeh", "institution": "University of Virginia", "region": "美国", "homepage": "https://engineering.virginia.edu/faculty/homa-alemzadeh", "topics": ["cyber-physical-systems", "runtime-monitoring", "robotics"]},
    {"name": "Madhur Behl", "institution": "University of Virginia", "region": "美国", "homepage": "https://engineering.virginia.edu/faculty/madhur-behl", "topics": ["cyber-physical-systems", "safe-rl", "world-model-control"]},
    {"name": "Dylan Shell", "institution": "Texas A&M", "region": "美国", "homepage": "https://engineering.tamu.edu/cse/profiles/dshell.html", "topics": ["robotics", "llm-planning", "cyber-physical-systems"]},
    {"name": "Dezhen Song", "institution": "Texas A&M", "region": "美国", "homepage": "https://engineering.tamu.edu/cse/profiles/dzsong.html", "topics": ["robotics", "multimodal-perception", "world-model-control"]},
    {"name": "Aaron Becker", "institution": "University of Houston", "region": "美国", "homepage": "https://www.ece.uh.edu/faculty/becker-aaron", "topics": ["robotics", "robot-manipulation", "cyber-physical-systems"]},
    {"name": "Lydia Kavraki", "institution": "Rice University", "region": "美国", "homepage": "https://profiles.rice.edu/faculty/lydia-e-kavraki", "topics": ["robotics", "llm-planning", "robot-manipulation"]},
    {"name": "Marcia O'Malley", "institution": "Rice University", "region": "美国", "homepage": "https://profiles.rice.edu/faculty/marcia-omalley", "topics": ["robotics", "hri-human-in-loop", "robot-manipulation"]},
    {"name": "Kaiyu Hang", "institution": "Rice University", "region": "美国", "homepage": "https://profiles.rice.edu/faculty/kaiyu-hang", "topics": ["robot-manipulation", "vla-models", "hri-human-in-loop"]},
    {"name": "Bolei Zhou", "institution": "UCLA", "region": "美国", "homepage": "https://boleizhou.github.io/", "topics": ["world-model-learning", "video-world-models", "vla-models"]},
    {"name": "Dennis Hong", "institution": "UCLA", "region": "美国", "homepage": "https://www.romela.org/", "topics": ["robotics", "robot-manipulation", "sim-to-real"]},
    {"name": "Mani Srivastava", "institution": "UCLA", "region": "美国", "homepage": "https://nesl.ucla.edu/", "topics": ["cyber-physical-systems", "runtime-monitoring", "formal-methods"]},
    {"name": "Paulo Tabuada", "institution": "UCLA", "region": "美国", "homepage": "https://www.ee.ucla.edu/paulo-tabuada/", "topics": ["formal-methods", "cyber-physical-systems", "safe-rl"]},
    {"name": "Soon-Jo Chung", "institution": "Caltech", "region": "美国", "homepage": "https://aerospacerobotics.caltech.edu/", "topics": ["robotics", "safe-rl", "world-model-control"]},
    {"name": "Joel Burdick", "institution": "Caltech", "region": "美国", "homepage": "https://www.cms.caltech.edu/people/jwb", "topics": ["robotics", "robot-manipulation", "llm-planning"]},
    {"name": "Yisong Yue", "institution": "Caltech", "region": "美国", "homepage": "https://www.cms.caltech.edu/people/yyue", "topics": ["robotics", "safe-rl", "world-model-learning"]},
    {"name": "Geoff Hollinger", "institution": "Oregon State University", "region": "美国", "homepage": "https://robotics.oregonstate.edu/faculty", "topics": ["robotics", "llm-planning", "world-model-control"]},
    {"name": "Naomi Fitter", "institution": "Oregon State University", "region": "美国", "homepage": "https://robotics.oregonstate.edu/faculty", "topics": ["robotics", "hri-human-in-loop", "embodied-benchmarks"]},
    {"name": "Heather Knight", "institution": "Oregon State University", "region": "美国", "homepage": "https://robotics.oregonstate.edu/faculty", "topics": ["robotics", "hri-human-in-loop", "multimodal-perception"]},
    {"name": "Alan Fern", "institution": "Oregon State University", "region": "美国", "homepage": "https://robotics.oregonstate.edu/faculty", "topics": ["robotics", "safe-rl", "llm-planning"]},
    {"name": "Daniel Brown", "institution": "University of Utah", "region": "美国", "homepage": "https://robotics.coe.utah.edu/facultylabs/", "topics": ["safe-rl", "hri-human-in-loop", "robotics"]},
    {"name": "Tucker Hermans", "institution": "University of Utah", "region": "美国", "homepage": "https://robotics.coe.utah.edu/facultylabs/", "topics": ["robot-manipulation", "world-model-learning", "multimodal-perception"]},
    {"name": "Ziad Al-Halah", "institution": "University of Utah", "region": "美国", "homepage": "https://robotics.coe.utah.edu/facultylabs/", "topics": ["vla-models", "multimodal-perception", "embodied-benchmarks"]},
    {"name": "Hani Ben Amor", "institution": "Arizona State University", "region": "美国", "homepage": "https://ras.engineering.asu.edu/faculty/", "topics": ["robotics", "hri-human-in-loop", "robot-manipulation"]},
    {"name": "Spring Berman", "institution": "Arizona State University", "region": "美国", "homepage": "https://ras.engineering.asu.edu/faculty/", "topics": ["robotics", "cyber-physical-systems", "world-model-control"]},
    {"name": "Wanxin Jin", "institution": "Arizona State University", "region": "美国", "homepage": "https://ras.engineering.asu.edu/faculty/", "topics": ["robotics", "safe-rl", "hri-human-in-loop"]},
    {"name": "Siddharth Srivastava", "institution": "Arizona State University", "region": "美国", "homepage": "https://ras.engineering.asu.edu/faculty/", "topics": ["robotics", "llm-planning", "llm-agents"]},
    {"name": "Yu Zhang", "institution": "Arizona State University", "region": "美国", "homepage": "https://ras.engineering.asu.edu/faculty/", "topics": ["robotics", "hri-human-in-loop", "llm-agents"], "auto_match": False},
    {"name": "Bilge Mutlu", "institution": "University of Wisconsin-Madison", "region": "美国", "homepage": "https://integrate.wisc.edu/people/", "topics": ["robotics", "hri-human-in-loop", "embodied-benchmarks"]},
    {"name": "Michael Zinn", "institution": "University of Wisconsin-Madison", "region": "美国", "homepage": "https://integrate.wisc.edu/people/", "topics": ["robotics", "robot-manipulation", "hri-human-in-loop"]},
    {"name": "Kostas Bekris", "institution": "Rutgers", "region": "美国", "homepage": "https://ruccs.rutgers.edu/people/executive-council-faculty", "topics": ["robotics", "llm-planning", "robot-manipulation"]},
    {"name": "Jingang Yi", "institution": "Rutgers", "region": "美国", "homepage": "https://jingangyi.rutgers.edu/", "topics": ["robotics", "cyber-physical-systems", "safe-rl"]},
    {"name": "Dylan Losey", "institution": "Virginia Tech", "region": "美国", "homepage": "https://me.vt.edu/people/faculty/losey-dylan.html", "topics": ["robotics", "hri-human-in-loop", "vla-models"]},
    {"name": "Ron Alterovitz", "institution": "University of North Carolina at Chapel Hill", "region": "美国", "homepage": "https://www.cs.unc.edu/~ron/", "topics": ["robotics", "llm-planning", "robot-manipulation"]},
    {"name": "Hao Zhang", "institution": "Colorado School of Mines", "region": "美国", "homepage": "https://cs.mines.edu/project/robotics/", "topics": ["robotics", "multimodal-perception", "hri-human-in-loop"], "auto_match": False},
    {"name": "Rafael Fierro", "institution": "University of New Mexico", "region": "美国", "homepage": "https://www.unm.edu/~fierro/", "topics": ["robotics", "cyber-physical-systems", "safe-rl"]},
    {"name": "Tim Barfoot", "institution": "University of Toronto", "region": "加拿大", "homepage": "https://robotics.utoronto.ca/", "topics": ["robotics", "world-model-control", "multimodal-perception"]},
    {"name": "Nick Rhinehart", "institution": "University of Toronto", "region": "加拿大", "homepage": "https://robotics.utoronto.ca/", "topics": ["world-model-learning", "robotics", "safe-rl"]},
    {"name": "Jonathan Kelly", "institution": "University of Toronto", "region": "加拿大", "homepage": "https://robotics.utoronto.ca/", "topics": ["robotics", "world-model-control", "safe-rl"]},
    {"name": "Steven Waslander", "aliases": ["Steve Waslander"], "institution": "University of Toronto", "region": "加拿大", "homepage": "https://robotics.utoronto.ca/", "topics": ["robotics", "multimodal-perception", "safe-rl"]},
    {"name": "Jessica Burgner-Kahrs", "institution": "University of Toronto", "region": "加拿大", "homepage": "https://robotics.utoronto.ca/", "topics": ["robotics", "robot-manipulation", "hri-human-in-loop"]},
    {"name": "Kelsey Allen", "institution": "University of British Columbia", "region": "加拿大", "homepage": "https://www.cs.ubc.ca/cs-research/research-area/robotics", "topics": ["world-model-learning", "robotics", "robot-manipulation"]},
    {"name": "Peter Yichen Chen", "institution": "University of British Columbia", "region": "加拿大", "homepage": "https://www.cs.ubc.ca/cs-research/research-area/robotics", "topics": ["robotics", "world-model-control", "safe-rl"]},
    {"name": "Karon MacLean", "institution": "University of British Columbia", "region": "加拿大", "homepage": "https://www.cs.ubc.ca/cs-research/research-area/robotics", "topics": ["robotics", "hri-human-in-loop", "multimodal-perception"]},
    {"name": "Ian Mitchell", "institution": "University of British Columbia", "region": "加拿大", "homepage": "https://www.cs.ubc.ca/cs-research/research-area/robotics", "topics": ["formal-methods", "cyber-physical-systems", "safe-rl"]},
    {"name": "Kerstin Dautenhahn", "institution": "University of Waterloo", "region": "加拿大", "homepage": "https://uwaterloo.ca/robohub/about/team/core", "topics": ["robotics", "hri-human-in-loop", "embodied-benchmarks"]},
    {"name": "William Melek", "institution": "University of Waterloo", "region": "加拿大", "homepage": "https://uwaterloo.ca/robohub/about/team/core", "topics": ["robotics", "world-model-control", "multimodal-perception"]},
    {"name": "Chris Nielsen", "institution": "University of Waterloo", "region": "加拿大", "homepage": "https://uwaterloo.ca/robohub/about/team/core", "topics": ["robotics", "cyber-physical-systems", "world-model-control"]},
    {"name": "Stephen Smith", "institution": "University of Waterloo", "region": "加拿大", "homepage": "https://uwaterloo.ca/robohub/about/team/core", "topics": ["robotics", "llm-planning", "cyber-physical-systems"]},
    {"name": "Gennaro Notomista", "institution": "University of Waterloo", "region": "加拿大", "homepage": "https://uwaterloo.ca/robohub/robotics-waterloo/robotics-researchers", "topics": ["robotics", "safe-rl", "hri-human-in-loop"]},
    {"name": "Yash Pant", "institution": "University of Waterloo", "region": "加拿大", "homepage": "https://uwaterloo.ca/robohub/robotics-waterloo/robotics-researchers", "topics": ["formal-methods", "cyber-physical-systems", "safe-rl"]},
    {"name": "Glen Berseth", "institution": "Université de Montréal", "region": "加拿大", "homepage": "https://diro.umontreal.ca/english/research/research-interests/experts/ex/Robotics/", "topics": ["robotics", "safe-rl", "world-model-learning"]},
    {"name": "Liam Paull", "institution": "Université de Montréal", "region": "加拿大", "homepage": "https://diro.umontreal.ca/english/research/research-interests/experts/ex/Robotics/", "topics": ["robotics", "multimodal-perception", "safe-rl"]},
    {"name": "David Meger", "institution": "McGill University", "region": "加拿大", "homepage": "https://www.cs.mcgill.ca/~dmeger/", "topics": ["robotics", "multimodal-perception", "vla-models"]},
    {"name": "Gregory Dudek", "institution": "McGill University", "region": "加拿大", "homepage": "https://www.cim.mcgill.ca/~dudek/", "topics": ["robotics", "world-model-control", "multimodal-perception"]},
    {"name": "Jerome Le Ny", "aliases": ["Jérôme Le Ny"], "institution": "Polytechnique Montréal", "region": "加拿大", "homepage": "https://www.professeurs.polymtl.ca/jerome.le-ny/", "topics": ["cyber-physical-systems", "formal-methods", "robotics"]},
    {"name": "Pierre-Yves Lajoie", "institution": "Polytechnique Montréal", "region": "加拿大", "homepage": "https://www.polymtl.ca/expertises/en/lajoie-pierre-yves", "topics": ["robotics", "multimodal-perception", "cyber-physical-systems"]},
    {"name": "Lionel Birglen", "institution": "Polytechnique Montréal", "region": "加拿大", "homepage": "https://www.polymtl.ca/labrobot/membres/membres", "topics": ["robotics", "robot-manipulation", "hri-human-in-loop"]},
    {"name": "Angelica Lim", "institution": "Simon Fraser University", "region": "加拿大", "homepage": "https://www.sfu.ca/cognitive-science/about/people/current-faculty-and-instructors.html", "topics": ["robotics", "hri-human-in-loop", "multimodal-perception"]},
    {"name": "Jesus Savage", "aliases": ["Jesús Savage"], "institution": "UNAM", "region": "墨西哥", "homepage": "https://www.siass.unam.mx/consulta/2101119", "topics": ["robotics", "llm-planning", "hri-human-in-loop"]},
    {"name": "Jose Martinez-Carranza", "aliases": ["José Martínez-Carranza"], "institution": "INAOE", "region": "墨西哥", "homepage": "https://ccc.inaoep.mx/~carranza/", "topics": ["robotics", "multimodal-perception", "world-model-control"]},
    {"name": "Luis Enrique Sucar", "institution": "INAOE", "region": "墨西哥", "homepage": "https://ccc.inaoep.mx/lineas-de-investigacion/robotica", "topics": ["robotics", "world-model-learning", "hri-human-in-loop"]},
    {"name": "Joel Carlos Huegel-West", "institution": "Tecnológico de Monterrey", "region": "墨西哥", "homepage": "https://tec.mx/es/profesores/eic/joel-carlos-huegel-west", "topics": ["robotics", "hri-human-in-loop", "robot-manipulation"]},
    {"name": "Jesus Arturo Escobedo", "aliases": ["Jesús Arturo Escobedo"], "institution": "Tecnológico de Monterrey", "region": "墨西哥", "homepage": "https://tec.mx/es/profesores/eic/jesus-arturo-escobedo", "topics": ["robotics", "hri-human-in-loop", "llm-planning"]},
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
.identity h3 a { color:var(--ink); text-decoration:none; }
.identity h3 a:hover { color:var(--accent); }
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
  <nav class="site-nav" aria-label="主导航"><a class="on" href="index.html">导师地图</a><a href="papers.html?sort=quality">精选推荐</a><a href="papers.html">论文库</a><a href="/tools">抓取与订阅</a></nav>
  <span class="built">数据更新：__BUILT__</span>
  <button id="theme" title="切换深浅色">◐</button>
</header>
<section class="intro">
  <div><div class="kicker">RESEARCH GROUP FIELD GUIDE</div><h1>先找对老师，再顺着研究脉络读论文。</h1></div>
  <p class="scope">当前范围覆盖北美 formal methods、CPS、robotics、VLA / 具身智能与世界模型。只收录可由高校或个人主页核验的 faculty / PI；论文数量仅代表本站已有记录，不等于完整发表量。</p>
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
  const ids = new Set(faculty.paper_ids || []);
  return PAPERS.filter(p => ids.has(p.id));
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
      <div class="identity"><h3><a href="faculty.html?id=${encodeURIComponent(f.id)}">${esc(f.name)}</a></h3><p>${esc(f.institution)} · ${esc(f.region)}</p>
      <a href="${esc(f.homepage)}" target="_blank" rel="noopener">官方资料 ↗</a></div>
      <div class="faculty-main"><div class="chips">${f.topics.map(t=>`<span class="chip">${esc(TAX[t]||t)}</span>`).join('')}</div>
      <p class="evidence">本站收录 ${papers.length} 篇相关论文</p>
      <div class="paper-links"><a href="faculty.html?id=${encodeURIComponent(f.id)}">查看方向总结与全部论文 →</a>${papers.slice(0,2).map(p=>`<a href="paper.html?id=${encodeURIComponent(p.id)}">${esc(p.title)} →</a>`).join('')}</div></div>`;
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

FACULTY_TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>导师 · paper-radar</title>
<meta name="description" content="导师研究方向与本站关联论文">
<style>
:root { --bg:#f5f7fb; --surface:#fff; --ink:#17223b; --muted:#65708a; --accent:#2546d8; --accent-soft:#e9edff; --signal:#e14a2b; --border:#dce2ee; }
@media (prefers-color-scheme:dark) { :root { --bg:#0c1220; --surface:#151d2f; --ink:#f3f6ff; --muted:#a9b2c7; --accent:#8ea2ff; --accent-soft:#202b52; --signal:#ff8065; --border:#293550; } }
:root[data-theme="light"] { --bg:#f5f7fb; --surface:#fff; --ink:#17223b; --muted:#65708a; --accent:#2546d8; --accent-soft:#e9edff; --signal:#e14a2b; --border:#dce2ee; }
:root[data-theme="dark"] { --bg:#0c1220; --surface:#151d2f; --ink:#f3f6ff; --muted:#a9b2c7; --accent:#8ea2ff; --accent-soft:#202b52; --signal:#ff8065; --border:#293550; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink); font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif; }
a { color:var(--accent); }
.wrap { max-width:1080px; margin:auto; padding:0 24px 80px; }
.topbar { min-height:72px; display:flex; align-items:center; gap:18px; border-bottom:1px solid var(--border); }
.brand { font-weight:800; letter-spacing:-.02em; white-space:nowrap; }.brand span { color:var(--signal); }
.site-nav { display:flex; gap:4px; }.site-nav a { color:var(--muted); text-decoration:none; padding:6px 10px; border-radius:8px; font-size:14px; }
.site-nav a:hover,.site-nav a.on { color:var(--accent); background:var(--accent-soft); }
#theme { margin-left:auto; background:var(--surface); border:1px solid var(--border); border-radius:999px; color:var(--muted); cursor:pointer; padding:4px 11px; }
.profile { padding:42px 0 28px; border-bottom:1px solid var(--ink); }
.back { display:inline-block; color:var(--muted); text-decoration:none; font-size:14px; margin-bottom:18px; }.back:hover { color:var(--accent); }
.eyebrow { color:var(--signal); font-size:13px; font-weight:800; letter-spacing:.1em; text-transform:uppercase; }
h1 { margin:8px 0 6px; font-size:clamp(38px,6vw,64px); line-height:1.05; letter-spacing:-.045em; }
.affiliation { color:var(--muted); font-size:18px; }
.chips { display:flex; flex-wrap:wrap; gap:7px; margin:20px 0 16px; }.chip { color:var(--accent); background:var(--accent-soft); border-radius:999px; padding:4px 10px; font-size:13px; }
.homepage { text-decoration:none; font-weight:650; }
.summary { display:grid; grid-template-columns:180px minmax(0,1fr); gap:28px; padding:28px 0; border-bottom:1px solid var(--border); }
.summary h2,.papers-head h2 { margin:0; font-size:13px; color:var(--muted); letter-spacing:.1em; text-transform:uppercase; }
.summary p { margin:0; font-size:18px; line-height:1.7; }
.boundary { color:var(--muted); font-size:14px; border-left:3px solid var(--accent); padding-left:14px; margin-top:14px; }
.papers-head { display:flex; justify-content:space-between; align-items:baseline; gap:20px; padding:30px 0 10px; border-bottom:1px solid var(--ink); }.papers-head span { color:var(--muted); font-size:14px; }
.paper { display:grid; grid-template-columns:100px minmax(0,1fr); gap:22px; padding:20px 4px; border-bottom:1px solid var(--border); }
.date { color:var(--muted); font-size:13px; padding-top:4px; }
.paper h3 { margin:0; font-size:18px; line-height:1.4; }.paper h3 a { color:var(--ink); text-decoration:none; }.paper h3 a:hover { color:var(--accent); }
.meta { color:var(--muted); font-size:14px; margin:5px 0 9px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.paper .chips { margin:0; }.paper .chip { padding:2px 8px; font-size:12px; }
.links { display:flex; gap:16px; margin-top:9px; }.links a { font-size:13px; text-decoration:none; }
.empty,.error { color:var(--muted); padding:48px 0; }.error { max-width:680px; margin:auto; text-align:center; }
@media (max-width:720px) { .wrap{padding:0 16px 60px}.topbar{gap:8px;flex-wrap:wrap;padding:12px 0}.brand{font-size:14px}.site-nav{order:3;width:100%}.summary{grid-template-columns:1fr;gap:10px}.paper{grid-template-columns:1fr;gap:5px}.date{padding:0} }
</style>
</head>
<body>
<main class="wrap" id="page" hidden>
  <header class="topbar"><div class="brand">paper<span>radar</span> / 导师</div><nav class="site-nav" aria-label="主导航"><a class="on" href="index.html">导师地图</a><a href="papers.html?sort=quality">精选推荐</a><a href="papers.html">论文库</a><a href="/tools">抓取与订阅</a></nav><button id="theme" aria-label="切换深浅色">◐</button></header>
  <section class="profile"><a class="back" href="index.html">← 返回导师地图</a><div class="eyebrow">Research direction profile</div><h1 id="name"></h1><div class="affiliation" id="affiliation"></div><div class="chips" id="topics"></div><a class="homepage" id="homepage" target="_blank" rel="noopener">官方资料 ↗</a></section>
  <section class="summary"><h2>方向总结</h2><div><p id="summary"></p><div class="boundary">方向标签来自人工整理；论文通过作者姓名及别名与本站记录匹配，不代表完整发表列表，同名作者仍需通过原文核验。</div></div></section>
  <section><div class="papers-head"><h2>本站关联论文</h2><span id="count"></span></div><div id="papers"></div></section>
</main>
<div class="error" id="error" hidden><h1>找不到这位导师</h1><p>请回到导师地图重新打开。</p><a href="index.html">返回导师地图</a></div>
<script>
const FACULTY = __FACULTY__;
const PAPERS = __INDEX__;
const TAX = __TAXONOMY__;
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

function paperChips(p) {
  return (p.topics||[]).slice(0,3).map(t=>`<span class="chip">${esc(TAX[t]||t)}</span>`).join('');
}
function directionSummary(faculty,papers) {
  const labels=faculty.topics.map(t=>TAX[t]||t);
  const counts={};
  for(const paper of papers) for(const topic of paper.topics||[]) counts[topic]=(counts[topic]||0)+1;
  const ranked=Object.entries(counts).sort((a,b)=>b[1]-a[1]).slice(0,3);
  const observed=ranked.length ? `在本站匹配到的论文中，出现最多的是${ranked.map(([t,n])=>`${TAX[t]||t}（${n}篇）`).join('、')}。` : '本站目前尚未匹配到其论文记录，方向描述仅依据人工整理标签。';
  return `本站将其主要方向归纳为${labels.join('、')}。${observed}`;
}
function load() {
  const id=new URLSearchParams(location.search).get('id');
  const faculty=FACULTY.find(f=>f.id===id);
  if(!faculty){ $('error').hidden=false; return; }
  const ids=new Set(faculty.paper_ids||[]);
  const papers=PAPERS.filter(p=>ids.has(p.id));
  document.title=`${faculty.name} · paper-radar`;
  $('name').textContent=faculty.name;
  $('affiliation').textContent=`${faculty.institution} · ${faculty.region}`;
  $('homepage').href=faculty.homepage;
  $('topics').innerHTML=faculty.topics.map(t=>`<span class="chip">${esc(TAX[t]||t)}</span>`).join('');
  $('summary').textContent=directionSummary(faculty,papers);
  $('count').textContent=`${papers.length} 篇`;
  $('papers').innerHTML=papers.length ? papers.map(p=>`<article class="paper"><div class="date">${esc(p.date||p.year||'日期未记录')}</div><div><h3><a href="paper.html?id=${encodeURIComponent(p.id)}">${esc(p.title)}</a></h3><div class="meta">${esc(p.authors||'作者未记录')}</div><div class="chips">${paperChips(p)}</div><div class="links"><a href="paper.html?id=${encodeURIComponent(p.id)}">结构化详情 →</a>${p.url?`<a href="${esc(p.url)}" target="_blank" rel="noopener">原文 ↗</a>`:''}</div></div></article>`).join('') : '<p class="empty">本站暂未收录可匹配的论文。</p>';
  $('page').hidden=false;
}
$('theme').addEventListener('click',()=>{ const cur=document.documentElement.dataset.theme||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'); const next=cur==='dark'?'light':'dark'; document.documentElement.dataset.theme=next; localStorage.setItem('theme',next); });
const saved=localStorage.getItem('theme'); if(saved) document.documentElement.dataset.theme=saved;
load();
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
.chip.score { color:var(--signal); font-weight:750; }
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
  <nav class="site-nav" aria-label="主导航"><a href="index.html">导师地图</a><a id="nav-quality" href="papers.html?sort=quality">精选推荐</a><a id="nav-library" class="on" href="papers.html">论文库</a><a href="/tools">抓取与订阅</a></nav>
  <span class="built">数据更新：__BUILT__</span><button id="theme" aria-label="切换深浅色">◐</button>
</header>
<section class="intro">
  <div><div class="kicker" id="kicker">RESEARCH PAPER LIBRARY</div><h1 id="page-title">从论文回到研究脉络。</h1></div>
  <p class="scope" id="scope">汇总每日自动抓取与人工精读记录。可按主题、来源和年份筛选，并进入每篇论文的结构化详情页。</p>
</section>
<div class="filters">
  <input id="q" type="search" placeholder="搜索标题或作者…" aria-label="搜索论文">
  <select id="f-topic"><option value="">主题：全部</option></select>
  <select id="f-source"><option value="">来源：全部</option><option value="curated">精读整理</option><option value="auto">自动抓取</option></select>
  <select id="f-year"><option value="">年份：全部</option></select>
  <select id="f-sort"><option value="recent">排序：最新优先</option><option value="quality">排序：精选推荐</option></select>
</div>
<div class="result-head"><h2 id="result-title">论文目录</h2><span id="count"></span></div>
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
  const quality = $('f-sort').value==='quality' && p.quality_score ? `<span class="chip score">推荐 ${p.quality_score}</span>${(p.quality_reasons||[]).map(v=>`<span class="chip">${esc(v)}</span>`).join('')}` : '';
  return quality + (p.source==='curated' ? '<span class="chip">精读整理</span>' : '') + values.map(v=>`<span class="chip">${esc(v)}</span>`).join('');
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
  const q=$('q').value.trim().toLowerCase(), topic=$('f-topic').value, source=$('f-source').value, year=$('f-year').value, quality=$('f-sort').value==='quality';
  filtered=PAPERS.filter(p=>(!q||`${p.title} ${p.authors||''}`.toLowerCase().includes(q))&&(!topic||(p.topics||[]).includes(topic))&&(!source||(source==='auto'?p.source!=='curated':p.source===source))&&(!year||String(p.year)===year));
  if (quality) filtered=filtered.filter(p=>(p.quality_score||0)>=20).sort((a,b)=>b.quality_score-a.quality_score||String(b.date||b.year||'').localeCompare(String(a.date||a.year||'')));
  $('nav-quality').classList.toggle('on',quality); $('nav-library').classList.toggle('on',!quality);
  $('kicker').textContent=quality?'EVIDENCE-AWARE RECOMMENDATIONS':'RESEARCH PAPER LIBRARY';
  $('page-title').textContent=quality?'先读更值得关注的论文。':'从论文回到研究脉络。';
  $('scope').textContent=quality?'推荐分只用于排阅读优先级，不是论文质量定论。依据人工精读、核心标记、发表 venue、HF 社区关注度和新近度；缺少证据时保守降分。':'汇总每日自动抓取与人工精读记录。可按主题、来源和年份筛选，并进入每篇论文的结构化详情页。';
  $('result-title').textContent=quality?'精选推荐':'论文目录';
  $('count').textContent=`${filtered.length} / ${PAPERS.length} 篇`; $('list').innerHTML=''; shown=0;
  if (filtered.length) renderMore(); else $('list').innerHTML='<p class="empty">没有匹配的论文。</p>';
}
for (const id of ['q','f-topic','f-source','f-year','f-sort']) $(id).addEventListener('input',applyFilters);
$('loadmore').addEventListener('click',renderMore);
$('theme').addEventListener('click',()=>{ const cur=document.documentElement.dataset.theme||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'); const next=cur==='dark'?'light':'dark'; document.documentElement.dataset.theme=next; localStorage.setItem('theme',next); });
const saved=localStorage.getItem('theme'); if(saved) document.documentElement.dataset.theme=saved;
$('f-sort').value=new URLSearchParams(location.search).get('sort')==='quality'?'quality':'recent';
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
  <nav class="topbar"><a class="back" href="papers.html">← 论文库</a><a href="papers.html?sort=quality">精选推荐</a><a href="index.html">导师地图</a><a href="/tools">抓取与订阅</a><button id="theme" aria-label="切换深浅色">◐</button></nav>
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
                "category", "source", "status", "topics", "hf_upvotes", "venue", "is_core")


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
    index = []
    today = date.today()
    for paper in papers:
        score, reasons = 0, []
        if paper.get("source") == "curated":
            score += 35
            reasons.append("人工精读")
        if paper.get("is_core"):
            score += 25
            reasons.append("核心论文")
        venue = str(paper.get("venue") or "").strip()
        if venue and not re.search(r"arxiv|preprint|report", venue, re.I):
            score += 15
            reasons.append(venue)
        votes = int(paper.get("hf_upvotes") or 0)
        vote_score = 25 if votes >= 200 else 22 if votes >= 100 else 18 if votes >= 50 else 14 if votes >= 20 else 10 if votes >= 10 else 0
        if vote_score:
            score += vote_score
            reasons.append(f"HF {votes} 赞")
        if score and paper.get("date"):
            age_days = (today - date.fromisoformat(paper["date"])).days
            if age_days <= 30:
                score += 10
                reasons.append("近 30 天")
            elif age_days <= 180:
                score += 5
                reasons.append("近半年")
        record = {k: paper.get(k) for k in INDEX_FIELDS if paper.get(k)}
        if score:
            record["quality_score"] = min(score, 100)
            record["quality_reasons"] = reasons
        index.append(record)

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
    faculty = []
    for item in FACULTY:
        names = [item["name"], *item.get("aliases", [])]
        paper_ids = [p["id"] for p in papers if item.get("auto_match", True) and any(
            re.search(rf"(?<![\w]){re.escape(name)}(?![\w])",
                      str(p.get("authors") or ""), re.I)
            for name in names)]
        faculty.append({**item,
                        "id": re.sub(r"[^a-z0-9]+", "-", item["name"].lower()).strip("-"),
                        "paper_ids": paper_ids})
    if len({item["id"] for item in faculty}) != len(faculty):
        raise ValueError("faculty ids must be unique")

    html = TEMPLATE.replace("__BUILT__", time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()))
    html = html.replace("__INDEX__", json.dumps(index, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__FACULTY__", json.dumps(faculty, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__TAXONOMY__", json.dumps(tax_names, ensure_ascii=False, separators=(",", ":")))
    (SITE_DIR / "index.html").write_text(html, encoding="utf-8")
    faculty_html = FACULTY_TEMPLATE.replace(
        "__FACULTY__", json.dumps(faculty, ensure_ascii=False, separators=(",", ":")))
    faculty_html = faculty_html.replace(
        "__INDEX__", json.dumps(index, ensure_ascii=False, separators=(",", ":")))
    faculty_html = faculty_html.replace(
        "__TAXONOMY__", json.dumps(tax_names, ensure_ascii=False, separators=(",", ":")))
    (SITE_DIR / "faculty.html").write_text(faculty_html, encoding="utf-8")
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
    print(f"✅ site/ 构建完成：{len(faculty)} 位导师、{len(papers)} 篇论文、"
          f"{len(reviews)} 篇含精读主页内容")


if __name__ == "__main__":
    main()
