"""
fix_3_1x_html_inject.py
精确修复 3.1.x 文件中被注入到 HTML 属性里的破损 <script> 片段
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

def fix_html_inject(qid):
    content = read(qid)
    
    # 破损注入模式：
    # class="block <script>        const QID = 'X.X.X';\n        const QNAME = '';\n        const QMAX = 0;\n(被截掉的部分)ium mb-1"
    # 正确应为：class="block font-medium mb-1"
    
    # 匹配并修复该注入
    broken = re.compile(
        r'class="block\s+<script>\s*\n\s*const QID\s*=\s*\'[^\']+\';\s*\n\s*const QNAME\s*=\s*\'\';\s*\n\s*const QMAX\s*=\s*0;\s*\n([a-z]*\s+[a-z-]*\s*")',
        re.DOTALL
    )
    m = broken.search(content)
    if m:
        # 提取被截掉的正常类名后缀
        leftover = m.group(1)
        # 正确内容应该是 class="block font-medium mb-1" 或类似
        # 尝试推断：截断了 "font-me"，留下了 "dium mb-1""
        # 完整正确：class="block font-medium mb-1"
        correct = 'class="block font-medium mb-1"'
        # 替换整个注入片段
        content_new = content[:m.start()] + correct + content[m.end():]
        write(qid, content_new)
        print(f'  OK  {qid}: fixed HTML inject, leftover was: {repr(leftover)}')
        return True
    else:
        # 尝试更宽松的匹配
        broken2 = re.compile(
            r'<script>\s*const QID\s*=\s*\'[^\']+\';\s*\n\s*const QNAME\s*=\s*\'\';\s*\n\s*const QMAX\s*=\s*0;\s*\n([^\n<]+)',
        )
        m2 = broken2.search(content)
        if m2:
            leftover2 = m2.group(1)
            # 找到这个注入在HTML属性中的位置
            inject_start = m2.start()
            # 找到注入前的 class="block 
            before = content[:inject_start]
            if before.rstrip().endswith('class="block'):
                inject_end = m2.end()
                content_new = before.rstrip()[:-len('class="block')] + 'class="block font-' + leftover2 + content[inject_end:]
                write(qid, content_new)
                print(f'  OK  {qid}: fixed HTML inject (method 2), leftover: {repr(leftover2[:30])}')
                return True
            else:
                # 直接删除整个注入片段
                content_new = content[:inject_start] + content[m2.end():]
                write(qid, content_new)
                print(f'  OK  {qid}: removed inject (method 3), leftover kept: {repr(leftover2[:50])}')
                return True
        else:
            print(f'  SKIP {qid}: no inject found')
            return False

for qid in ['3.1.1', '3.1.2', '3.1.3', '3.1.5']:
    print(f'Processing {qid}...')
    fix_html_inject(qid)

# 也要处理顶部破损的 script 块（3.1.x 的第一个script已被第一次修复脚本移除了一部分）
# 现在检查 3.1.x 顶部 script 是否有问题
print('\n--- Check 3.1.x top script ---')
for qid in ['3.1.1', '3.1.2', '3.1.3', '3.1.5']:
    content = read(qid)
    # 找顶部 <script> (不含 src=)
    m = re.search(r'<script>\s*\n\s*const QID\s*=', content)
    if m:
        snippet = content[m.start():m.start()+200]
        print(f'  {qid}: found top script at line, snippet={repr(snippet[:100])}')
    else:
        print(f'  {qid}: no broken top script found (OK)')
