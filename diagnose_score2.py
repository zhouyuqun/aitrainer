#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\76272\Documents\GitHub\aitrainer"
DIR_PATTERN = re.compile(r'^\d+\.\d+\.\d+$')

UNKNOWN_DIRS = [
    '1.2.2','1.2.3','1.2.4','1.2.5',
    '2.1.4','2.1.5',
    '2.2.1','2.2.2','2.2.3','2.2.4','2.2.5',
    '3.1.1','3.1.2','3.1.3','3.1.5',
    '3.2.1','3.2.2','3.2.3','3.2.4','3.2.5',
    '4.1.1','4.1.2','4.1.3','4.1.4','4.1.5',
    '4.2.1','4.2.2','4.2.3','4.2.4','4.2.5',
]

# 检测点：JS中写入答案对比的目标元素
WRITE_PATTERNS = [
    r'getElementById\([\'"](\w+)[\'"]\)\.innerHTML',
    r'getElementById\([\'"](\w+)[\'"]\)\.textContent',
    r'getElementById\([\'"](\w+)[\'"]\)\.innerText',
    r'getElementById\([\'"](\w+)[\'"]\)\.style\.display',
]

for name in UNKNOWN_DIRS:
    html_path = os.path.join(BASE, name, "index.html")
    if not os.path.exists(html_path):
        continue
    content = open(html_path, "r", encoding="utf-8").read()
    
    # 找所有JS写入目标id
    written_ids = set()
    for pat in WRITE_PATTERNS:
        for m in re.finditer(pat, content):
            written_ids.add(m.group(1))
    
    # 找HTML中有id的div
    html_ids = set(re.findall(r'<div[^>]+id="(\w+)"', content))
    
    # 找JS中被写入内容但HTML div里没有id的情况
    # 具体看wrong/correct相关id
    score_ids_in_js = {i for i in written_ids if 'wrong' in i.lower() or 'correct' in i.lower() or 'compare' in i.lower() or 'result' in i.lower() or 'score' in i.lower()}
    
    print(f"\n[{name}]")
    print(f"  JS writes to: {sorted(written_ids)}")
    print(f"  HTML div ids: {sorted(html_ids)}")
    missing = written_ids - html_ids
    if missing:
        print(f"  *** MISSING IDs (JS writes, HTML lacks): {missing}")
    else:
        print(f"  OK - all JS-target ids exist in HTML")
