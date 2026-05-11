#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查4.x系列题目的结构"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\76272\Documents\GitHub\aitrainer"

for qid in ['4.1.1','4.1.2','4.1.3','4.1.4','4.1.5','4.2.1','4.2.2','4.2.3','4.2.4','4.2.5']:
    html_path = os.path.join(BASE, qid, "index.html")
    content = open(html_path, "r", encoding="utf-8").read()
    
    # 找 data-correct 属性
    corrects = re.findall(r'data-correct="([^"]+)"', content)
    # 找 data-score 属性  
    scores = re.findall(r'data-score="([^"]+)"', content)
    # 找按钮
    has_calc = 'calculateScore' in content
    has_script = '</script>' in content
    
    print(f"\n{qid}: has_calculateScore={has_calc}, has_script={has_script}")
    print(f"  data-score: {scores}")
    print(f"  data-correct ({len(corrects)} items): {corrects[:3]}{'...' if len(corrects)>3 else ''}")
