#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复 aitrainer 所有题目 HTML 中答案对比 div 缺少 id 属性的问题。
修复规则：
  <div class="wrong-answer">  -> <div class="wrong-answer" id="wrongAnswer">
  <div class="correct-answer">-> <div class="correct-answer" id="correctAnswer">
只处理没有 id 的情况，已有 id 的跳过。
"""
import os
import re

BASE = r"C:\Users\76272\Documents\GitHub\aitrainer"

# 需要处理的目录模式
DIR_PATTERN = re.compile(r'^\d+\.\d+\.\d+$')

fixed_files = []
skipped_files = []

for name in sorted(os.listdir(BASE)):
    if not DIR_PATTERN.match(name):
        continue
    html_path = os.path.join(BASE, name, "index.html")
    if not os.path.exists(html_path):
        continue

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    has_wrong_id = 'id="wrongAnswer"' in content
    has_correct_id = 'id="correctAnswer"' in content

    if has_wrong_id and has_correct_id:
        skipped_files.append(name)
        continue

    original = content

    # 修复 wrong-answer div（无 id 版）
    # 匹配 class="wrong-answer" 但没有 id= 的情况
    if not has_wrong_id:
        # 精确替换：class="wrong-answer"> (无 id)
        content = re.sub(
            r'<div\s+class="wrong-answer"(?!\s+id=)([^>]*)>',
            r'<div class="wrong-answer" id="wrongAnswer"\1>',
            content
        )

    # 修复 correct-answer div（无 id 版）
    if not has_correct_id:
        content = re.sub(
            r'<div\s+class="correct-answer"(?!\s+id=)([^>]*)>',
            r'<div class="correct-answer" id="correctAnswer"\1>',
            content
        )

    if content != original:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)
        fixed_files.append(name)
        print(f"[FIXED] {name}")
    else:
        print(f"[NO CHANGE] {name} - 可能 HTML 结构不同，需要手动检查")

print(f"\n=== 修复完成 ===")
print(f"已修复: {len(fixed_files)} 个文件: {fixed_files}")
print(f"已跳过(无需修复): {len(skipped_files)} 个文件: {skipped_files}")
