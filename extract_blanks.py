#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统计每道NO-SCORING题的blank id列表和评分标准"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\76272\Documents\GitHub\aitrainer"

NO_SCORE_DIRS = [
    '1.2.4','1.2.5',
    '2.1.4','2.1.5',
    '2.2.1','2.2.2','2.2.3','2.2.4','2.2.5',
    '3.1.1','3.1.2','3.1.3','3.1.5',
    '3.2.1','3.2.2','3.2.3','3.2.4','3.2.5',
    '4.1.1','4.1.2','4.1.3','4.1.4','4.1.5',
    '4.2.1','4.2.2','4.2.3','4.2.4','4.2.5',
]

for name in NO_SCORE_DIRS:
    html_path = os.path.join(BASE, name, "index.html")
    content = open(html_path, "r", encoding="utf-8").read()
    
    # 找所有input blank的id
    blank_ids = re.findall(r'<input[^>]+class="blank"[^>]+id="([^"]+)"', content)
    # 找textarea的id
    ta_ids = re.findall(r'<textarea[^>]+id="([^"]+)"', content)
    
    # 找评分标准行（含分值）
    score_lines = re.findall(r'(M\d+[^<\n]{0,80}?\d+分[^<\n]{0,30})', content)
    
    print(f"\n===== {name} =====")
    print(f"blank ids ({len(blank_ids)}): {blank_ids}")
    print(f"textarea ids: {ta_ids}")
    print(f"score lines: {score_lines[:15]}")
