#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\76272\Documents\GitHub\aitrainer"
DIR_PATTERN = re.compile(r'^\d+\.\d+\.\d+$')

problem_dirs = []
ok_dirs = []
other_structure = []

for name in sorted(os.listdir(BASE)):
    if not DIR_PATTERN.match(name):
        continue
    html_path = os.path.join(BASE, name, "index.html")
    if not os.path.exists(html_path):
        continue

    content = open(html_path, "r", encoding="utf-8").read()
    
    js_uses_wrong = "getElementById('wrongAnswer')" in content or 'getElementById("wrongAnswer")' in content
    html_has_wrong_id = 'id="wrongAnswer"' in content
    js_uses_correct = "getElementById('correctAnswer')" in content or 'getElementById("correctAnswer")' in content
    html_has_correct_id = 'id="correctAnswer"' in content
    
    uses_code_compare = 'codeCompareResult' in content
    uses_comparison_result = 'comparisonResult' in content
    
    bug = (js_uses_wrong and not html_has_wrong_id) or (js_uses_correct and not html_has_correct_id)
    
    if bug:
        problem_dirs.append(name)
        print(f"[BUG] {name}: JS uses wrongAnswer={js_uses_wrong}, html_has_id={html_has_wrong_id}")
    elif js_uses_wrong and html_has_wrong_id:
        ok_dirs.append(name)
        print(f"[OK-wrongAnswer] {name}")
    elif uses_code_compare or uses_comparison_result:
        other_structure.append(name)
        print(f"[OK-otherStruct] {name}: codeCompare={uses_code_compare}, compResult={uses_comparison_result}")
    else:
        print(f"[UNKNOWN] {name}")

print()
print(f"BUG count: {len(problem_dirs)}: {problem_dirs}")
print(f"OK(wrongAnswer) count: {len(ok_dirs)}: {ok_dirs}")
print(f"OK(other) count: {len(other_structure)}: {other_structure}")
