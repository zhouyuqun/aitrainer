#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查哪些题目的btnCheck按钮没有绑定打分逻辑"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\76272\Documents\GitHub\aitrainer"
DIR_PATTERN = re.compile(r'^\d+\.\d+\.\d+$')

for name in sorted(os.listdir(BASE)):
    if not DIR_PATTERN.match(name):
        continue
    html_path = os.path.join(BASE, name, "index.html")
    if not os.path.exists(html_path):
        continue
    content = open(html_path, "r", encoding="utf-8").read()
    
    has_btncheck = 'btnCheck' in content
    has_onclick_check = "btnCheck').onclick" in content or 'btnCheck").onclick' in content or "checkScore" in content or "checkAnswer" in content
    has_scoring_array = 'scoring' in content or 'SCORING' in content or 'answers' in content.lower()
    
    # 检测是否有实质性打分逻辑
    has_real_scoring = bool(re.search(r'(scoring|score\s*\+=|total\s*\+=)\s*', content))
    
    qmax_match = re.search(r"QMAX\s*=\s*(\d+)", content)
    qmax = qmax_match.group(1) if qmax_match else "?"
    
    status = "OK" if has_real_scoring else "NO-SCORING"
    print(f"{name}: QMAX={qmax:>3} btnCheck={has_btncheck} hasScoring={has_real_scoring} => {status}")
