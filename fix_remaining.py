"""
fix_remaining.py
针对1.x/2.x/3.x系列的特定问题进行修复
"""
import os, re

BASE = r'C:\Users\76272\Documents\GitHub\aitrainer'

def read(qid):
    path = os.path.join(BASE, qid, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write(qid, content):
    path = os.path.join(BASE, qid, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# ─────────────────────────────────────────────────────────
# 问题类型1：文件末尾缺少 </body></html>
# 影响：2.1.4, 2.1.5, 2.2.1~2.2.5, 3.2.1~3.2.5
# 修复：在末尾追加缺失的标签
# ─────────────────────────────────────────────────────────

MISSING_CLOSE_TAGS = [
    '2.1.4', '2.1.5',
    '2.2.1', '2.2.2', '2.2.3', '2.2.4', '2.2.5',
    '3.2.1', '3.2.2', '3.2.3', '3.2.4', '3.2.5',
]

def fix_missing_close(qid):
    content = read(qid)
    if '</html>' not in content[-100:]:
        # 找到最后一个 </script>，在它后面加上 </body></html>
        idx = content.rfind('</script>')
        if idx != -1:
            content = content[:idx+9] + '\n</body>\n</html>'
            write(qid, content)
            print(f'  OK  {qid}: added </body></html>')
        else:
            # 找 </body>
            idx2 = content.rfind('</body>')
            if idx2 != -1:
                content = content[:idx2+7] + '\n</html>'
                write(qid, content)
                print(f'  OK  {qid}: added </html>')
            else:
                content = content.rstrip() + '\n</body>\n</html>'
                write(qid, content)
                print(f'  OK  {qid}: appended </body></html>')
    else:
        print(f'  SKIP {qid}: already has </html>')

# ─────────────────────────────────────────────────────────
# 问题类型2：1.2.x 系列 - comparisonResult 换成 answerComparison
# 这些文件用的是 comparisonResult 而不是 answerComparison
# 已有 scoreResult，逻辑基本正常，只需添加 answerComparison div
# ─────────────────────────────────────────────────────────

def fix_1_2x_answerComparison(qid):
    content = read(qid)
    if 'id="answerComparison"' in content:
        print(f'  SKIP {qid}: already has answerComparison')
        return
    
    # 1.2.x 用 comparisonResult，我们给 resetThisQuestion 里的引用加上别名
    # 在 scoreResult div 后面插入一个 answerComparison div（指向同一内容）
    # 方案：在 scoreResult div 后面插入一个隐藏的 answerComparison div
    score_div_pattern = re.compile(r'(<div[^>]+id=["\']scoreResult["\'][^>]*>)', re.DOTALL)
    m = score_div_pattern.search(content)
    if m:
        insert_point = content.find('</div>', m.end())
        if insert_point != -1:
            alias_div = '\n<div id="answerComparison" style="display:none;"></div>'
            content = content[:insert_point+6] + alias_div + content[insert_point+6:]
            write(qid, content)
            print(f'  OK  {qid}: added answerComparison alias div')
        else:
            print(f'  WARN {qid}: could not find </div> after scoreResult')
    else:
        # 找 comparisonResult
        comp_pattern = re.compile(r'(<div[^>]+id=["\']comparisonResult["\'][^>]*>)', re.DOTALL)
        m2 = comp_pattern.search(content)
        if m2:
            alias_div = '<div id="answerComparison" style="display:none;"></div>\n'
            content = alias_div + content
            write(qid, content)
            print(f'  OK  {qid}: prepended answerComparison div')
        else:
            print(f'  WARN {qid}: no scoreResult or comparisonResult found')

# ─────────────────────────────────────────────────────────
# 问题类型3：1.2.2, 1.2.5 - 缺少 scoreResult div
# ─────────────────────────────────────────────────────────

def check_and_show_12x():
    for qid in ['1.2.1','1.2.2','1.2.3','1.2.4','1.2.5']:
        content = read(qid)
        has_score = 'id="scoreResult"' in content
        has_ans = 'id="answerComparison"' in content
        has_comp = 'id="comparisonResult"' in content
        has_check = 'checkScore' in content or 'checkBtn' in content or 'btnCheck' in content
        ends = '</html>' in content[-100:]
        print(f'  {qid}: scoreDiv={has_score} ansDiv={has_ans} compDiv={has_comp} checkFn={has_check} ends={ends}')

# ─────────────────────────────────────────────────────────
# 问题类型4：3.1.1~3.1.3, 3.1.5 - 破损的 script 被注入到 HTML 中
# 需要移除破损的 script 注入
# ─────────────────────────────────────────────────────────

def fix_3_1x_broken_inject(qid):
    content = read(qid)
    # 破损模式：<script>        const QID = '3.1.x';\n        const QNAME = '';\n        const QMAX = 0;\n被注入到属性或文本中
    # 找到这个破损注入片段
    broken_pattern = re.compile(
        r'<script>\s*\n\s*const QID\s*=\s*[\'"][^\'\"]+[\'"]\s*;\s*\n\s*const QNAME\s*=\s*[\'"]{2}\s*;\s*\n\s*const QMAX\s*=\s*0\s*;\s*\n(.*?)\n(.*?)(?=\s*\w)',
        re.DOTALL
    )
    
    # 更精确：找到被截断注入的位置
    # 破损内容格式: <script>        const QID = '3.1.x';\n        const QNAME = '';\n        const QMAX = 0;\n后面跟着正常html文本
    broken_inline = re.compile(
        r'<script>\s*const QID = \'[^\']+\';\s*\n\s*const QNAME = \'\';\s*\n\s*const QMAX = 0;\s*\n([^\n]*)\n',
    )
    m = broken_inline.search(content)
    if m:
        # 被截断后的剩余文本（正常的html）
        leftover = m.group(1)
        # 替换掉整个破损注入（包括其后的残余文本），恢复原本html内容
        content = content[:m.start()] + leftover + '\n' + content[m.end():]
        write(qid, content)
        print(f'  OK  {qid}: removed broken script inject, leftover: {repr(leftover[:50])}')
    else:
        print(f'  WARN {qid}: broken inject pattern not found')

# ─────────────────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────────────────

print('=== Step 1: Fix missing </body></html> ===')
for qid in MISSING_CLOSE_TAGS:
    fix_missing_close(qid)

print('\n=== Step 2: Check 1.2.x structure ===')
check_and_show_12x()

print('\n=== Step 3: Fix 3.1.1~3.1.3, 3.1.5 broken inject ===')
for qid in ['3.1.1', '3.1.2', '3.1.3', '3.1.5']:
    fix_3_1x_broken_inject(qid)

print('\nDone!')
