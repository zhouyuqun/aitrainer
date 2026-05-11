"""
fix_3_1x_full.py
完整修复 3.1.1、3.1.2、3.1.3、3.1.5、1.2.2、1.2.5 这些严重破损的文件
策略：
  1. 移除所有破损的 <script>...const QID... 碎片（不论出现在哪里）
  2. 修复被截断的 HTML 属性（class="block font-medium mb-1" 等）
  3. 在文件末尾（</script> 之后）追加正确的 </body></html>
  4. 在最后一个 <script> 块前，插入 scoreResult/answerComparison 的 alias div
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

def remove_broken_script_injections(content, qid_str):
    """
    移除所有被插入到HTML中的破损 <script>...const QID = '...'...\n(...leftover...)
    返回清理后的内容
    """
    # 匹配：任意位置出现的 <script> + QID 定义 + 被截断的原始内容
    # 破损模式1: <script>        const QID = 'X.X.X';\n        const QNAME = '';\n        const QMAX = 0;\n(任意截断内容)
    # 后面跟着被截断后的正常内容（如 "urn;" 是 "if (!confirm...return;" 的后半段）
    pattern = re.compile(
        r'<script>\s*\n?\s*const QID\s*=\s*\'[^\']+\';\s*\n\s*const QNAME\s*=\s*\'\';\s*\n\s*const QMAX\s*=\s*0;\s*\n([^\n<>]*)',
    )
    count = 0
    while True:
        m = pattern.search(content)
        if not m:
            break
        leftover = m.group(1).strip()
        # 检查这个注入是否在 HTML 属性中（前面有 class=" 等）
        before = content[:m.start()]
        if before.rstrip().endswith(('class="block', 'class="', '"block')):
            # 修复 HTML 属性：恢复 font-medium mb-1
            attr_part = 'font-' + leftover if leftover.startswith('medium') or leftover.startswith('m') else leftover
            if leftover.startswith('medium'):
                attr_part = 'font-medium mb-1"'
            elif leftover.startswith('m'):
                attr_part = 'font-medium mb-1"'
            else:
                attr_part = leftover
            content = content[:m.start()] + attr_part + content[m.end():]
        elif leftover.startswith('urn') or leftover.startswith('u'):
            # 在 resetThisQuestion 内部的注入，leftover 是 "urn;" = return;的后半
            content = content[:m.start()] + 'return;\n' + content[m.end():]
        elif leftover.startswith('ply') or leftover.startswith('p'):
            # apply 的后半
            content = content[:m.start()] + content[m.end():]
        else:
            # 直接删除注入片段，保留 leftover
            content = content[:m.start()] + leftover + '\n' + content[m.end():]
        count += 1
    
    # 还需要处理: </script>  if (!confirm ...的破损
    # 这种格式：</script>  if (!confirm('...
    # 需要删掉 </script> 后面到下一个 <script> 之前的破损内容
    script_close_inject = re.compile(
        r'</script>\s+if\s*\(!confirm\([^<]*<script>'
    )
    m2 = script_close_inject.search(content)
    if m2:
        # 找到后面的 <script> 继续
        content = content[:m2.start()] + content[m2.end()-len('<script>'):]
        count += 1
    
    print(f'  {qid_str}: removed {count} broken injections')
    return content

def fix_broken_top_script(content, qid_str):
    """
    修复文件开头处游离的 getStudentInfo 代码（顶部破损 script 的残骸）
    这些代码既不在 <script> 内也不在任何标签内，直接是纯文本
    """
    # 找到 </head><body 的位置
    head_end = content.find('</head>')
    if head_end == -1:
        # 找 <style>
        head_end = content.find('<style>')
    if head_end == -1:
        return content
    
    head_section = content[:head_end]
    body_and_rest = content[head_end:]
    
    # 在 head 之前（<script src=...> 之后）找游离的 JS 代码残骸
    # 游离代码特征：
    #   1. 以 "        function getStudentInfo() {" 开头
    #   2. 包含 "e_3.1.x');" 或 "2.5');" 这类 localStorage 残骸
    #   3. 以 "    }" 结尾
    
    # 找 <script src="../auth.js"></script> 后面的游离代码
    auth_script_end = head_section.rfind('</script>')
    if auth_script_end != -1:
        after_auth = head_section[auth_script_end+9:]
        if after_auth.strip() and not after_auth.strip().startswith('<'):
            # 有游离代码，删掉它
            head_section = head_section[:auth_script_end+9]
            print(f'  {qid_str}: removed orphan JS from head section ({len(after_auth)} chars)')
            content = head_section + body_and_rest
    
    return content

def ensure_close_tags(content, qid_str):
    """确保文件以 </body></html> 结尾"""
    if '</html>' not in content[-200:]:
        if '</script>' in content[-500:]:
            content = content.rstrip() + '\n</body>\n</html>'
            print(f'  {qid_str}: added </body></html>')
        elif '</body>' in content[-200:]:
            content = content.rstrip() + '\n</html>'
            print(f'  {qid_str}: added </html>')
    return content

def add_scoreresult_alias(content, qid_str):
    """在最后一个 </script> 之前添加 scoreResult/answerComparison alias div（如果不存在）"""
    if 'id="scoreResult"' not in content and 'id=\'scoreResult\'' not in content:
        # 在 </script></body> 之前插入
        insert_before = content.rfind('</script>')
        if insert_before != -1:
            alias = '\n<!-- score alias divs for resetThisQuestion compatibility -->\n'
            alias += '<div id="scoreResult" style="display:none;"></div>\n'
            alias += '<div id="answerComparison" style="display:none;"></div>\n'
            alias += '<div id="analysisBox" style="display:none;"></div>\n'
            # 插入在最后 </script> 之后
            pos = insert_before + len('</script>')
            content = content[:pos] + '\n' + alias + content[pos:]
            print(f'  {qid_str}: added score alias divs')
    return content

# ─────────────────────────────────────────────
# 处理 3.1.1, 3.1.2, 3.1.3
# ─────────────────────────────────────────────
for qid in ['3.1.1', '3.1.2', '3.1.3', '3.1.5']:
    print(f'\nProcessing {qid}...')
    content = read(qid)
    content = remove_broken_script_injections(content, qid)
    content = fix_broken_top_script(content, qid)
    content = ensure_close_tags(content, qid)
    content = add_scoreresult_alias(content, qid)
    write(qid, content)

# ─────────────────────────────────────────────
# 处理 1.2.2 - 用 resultPanel 代替 scoreResult
# ─────────────────────────────────────────────
print('\nProcessing 1.2.2...')
content = read('1.2.2')
# 1.2.2 的 resetThisQuestion 引用了不存在的 scoreResult/answerComparison
# 需要在文件里添加这些 alias div，但要指向 resultPanel
if 'id="scoreResult"' not in content:
    # 在 resultPanel div 后面插入别名
    m = re.search(r'<div[^>]+id=["\']resultPanel["\'][^>]*>', content)
    if m:
        end = content.find('</div>', m.end())
        if end != -1:
            alias = '\n<div id="scoreResult" style="display:none;"></div>\n<div id="answerComparison" style="display:none;"></div>\n'
            content = content[:end+6] + alias + content[end+6:]
            print('  1.2.2: added scoreResult/answerComparison alias after resultPanel')
    else:
        # 在 </body> 前插入
        body_end = content.rfind('</body>')
        if body_end != -1:
            alias = '<div id="scoreResult" style="display:none;"></div>\n<div id="answerComparison" style="display:none;"></div>\n'
            content = content[:body_end] + alias + content[body_end:]
            print('  1.2.2: added alias divs before </body>')
write('1.2.2', content)

# ─────────────────────────────────────────────
# 处理 1.2.3, 1.2.4 - 有 scoreResult 但缺 answerComparison
# ─────────────────────────────────────────────
for qid in ['1.2.3', '1.2.4']:
    print(f'\nProcessing {qid}...')
    content = read(qid)
    if 'id="answerComparison"' not in content:
        # 在 scoreResult div 后面找到结束，插入别名
        m = re.search(r'id=["\']scoreResult["\']', content)
        if m:
            # 找到这个 div 的结束
            div_start = content.rfind('<div', 0, m.start())
            end = content.find('</div>', m.end())
            if end != -1:
                alias = '\n<div id="answerComparison" style="display:none;"><div id="wrongAnswer"></div><div id="correctAnswer"></div></div>\n'
                content = content[:end+6] + alias + content[end+6:]
                print(f'  {qid}: added answerComparison after scoreResult')
        write(qid, content)

# ─────────────────────────────────────────────
# 处理 1.2.5 - 和 4.1.x 同类型，需要修复顶部 script + 添加页脚
# ─────────────────────────────────────────────
print('\nProcessing 1.2.5...')
content = read('1.2.5')

# 修复顶部破损 script
top_script_fix = '''<script>
        const QID = '1.2.5';

        function getStudentInfo() {
            return {
                name: localStorage.getItem('exam_student_name') || '',
                id: localStorage.getItem('exam_student_id') || ''
            };
        }

        function resetAll() {
            localStorage.removeItem('exam_score_' + QID);
            localStorage.removeItem('exam_done_' + QID);
            localStorage.removeItem('exam_wrong_' + QID);
            localStorage.removeItem('exam_answers_' + QID);
            document.querySelectorAll('input[type=text], textarea').forEach(function(i){i.value='';});
            var el;
            el = document.getElementById('scoreResult'); if(el) el.style.display='none';
            el = document.getElementById('answerComparison'); if(el) el.style.display='none';
            el = document.getElementById('analysisBox'); if(el) el.style.display='none';
        }

        function resetThisQuestion() {
            if (!confirm('确定要重做本题吗？成绩记录将被清除。')) return;
            resetAll();
            alert('已重置，可重新作答！');
        }
</script>'''

BROKEN_SCRIPT_PATTERN = re.compile(
    r'<script>\s*\n\s*const QID\s*=\s*[\'"][^\'\"]+[\'"];.*?</script>\s*\n</script>',
    re.DOTALL
)
content_new = BROKEN_SCRIPT_PATTERN.sub(top_script_fix, content, count=1)
if content_new == content:
    print('  1.2.5: WARN top script pattern not matched')
else:
    print('  1.2.5: top script fixed')
    content = content_new

# 添加页脚（从 <!-- 解析区 --> 截断处开始）
FOOTER_125 = '''
        </div>

        <div id="scoreResult" style="display:none;text-align:center;font-size:18px;font-weight:bold;
            color:#e74c3c;margin-top:15px;padding:12px;background:#fff5f5;border-radius:6px;">
            本次得分：<span id="finalScore">0</span> / 25 分
        </div>
        <div id="answerComparison" style="display:none;margin-top:15px;padding:15px;
            background:#f8f9fa;border-radius:6px;border:1px solid #dee2e6;">
            <div style="font-weight:bold;margin-bottom:10px;color:#2c5282;">答案对比</div>
            <div id="wrongAnswer"></div>
        </div>
    </div>
</div>

<script>
    // 1.2.5 评分（文字题，模糊匹配关键词）
    const standardAnswer_125 = {
        part1: {
            keywords: ['响应不准确','个性化','缺乏个性','交互能力','语音识别','准确率','用户体验','满意度'],
            score: 12
        },
        part2: {
            keywords: ['优化','数据采集','模型训练','迭代','个性化推荐','知识库','提升','效果'],
            score: 13
        }
    };

    function checkScore() {
        var ans1 = document.getElementById('answer1') ? document.getElementById('answer1').value.trim() : '';
        var ans2 = document.getElementById('answer2') ? document.getElementById('answer2').value.trim() : '';
        var score = 0;
        var html = '';

        // 评分：问题识别（12分，按关键词覆盖率）
        var kw1 = standardAnswer_125.part1.keywords;
        var hit1 = kw1.filter(function(k){return ans1.includes(k);}).length;
        var s1 = Math.min(Math.round(hit1 / kw1.length * standardAnswer_125.part1.score), standardAnswer_125.part1.score);
        score += s1;
        html += '<div style="color:' + (s1 >= 8 ? '#27ae60' : '#e74c3c') + ';margin:4px 0;">';
        html += '1.2.5-1 问题识别：' + s1 + '/' + standardAnswer_125.part1.score + '分（命中关键词：' + hit1 + '/' + kw1.length + '）</div>';

        // 评分：优化方案（13分）
        var kw2 = standardAnswer_125.part2.keywords;
        var hit2 = kw2.filter(function(k){return ans2.includes(k);}).length;
        var s2 = Math.min(Math.round(hit2 / kw2.length * standardAnswer_125.part2.score), standardAnswer_125.part2.score);
        score += s2;
        html += '<div style="color:' + (s2 >= 9 ? '#27ae60' : '#e74c3c') + ';margin:4px 0;">';
        html += '1.2.5-2 优化方案：' + s2 + '/' + standardAnswer_125.part2.score + '分（命中关键词：' + hit2 + '/' + kw2.length + '）</div>';

        document.getElementById('finalScore').textContent = score;
        document.getElementById('scoreResult').style.display = 'block';
        document.getElementById('answerComparison').style.display = 'block';
        document.getElementById('wrongAnswer').innerHTML = html;

        localStorage.setItem('exam_score_' + QID, score);
        localStorage.setItem('exam_done_' + QID, new Date().toISOString());
    }

    function resetAnswer() {
        document.getElementById('answer1').value = '';
        document.getElementById('answer2').value = '';
        document.getElementById('scoreResult').style.display = 'none';
        document.getElementById('answerComparison').style.display = 'none';
    }

    // 页面加载还原
    window.addEventListener('DOMContentLoaded', function() {
        var saved = localStorage.getItem('exam_answers_' + QID);
        if (saved) {
            try {
                var a = JSON.parse(saved);
                if (a.answer1 && document.getElementById('answer1')) document.getElementById('answer1').value = a.answer1;
                if (a.answer2 && document.getElementById('answer2')) document.getElementById('answer2').value = a.answer2;
            } catch(e) {}
        }
    });

    // 自动保存
    ['answer1','answer2'].forEach(function(id) {
        var el = document.getElementById(id);
        if (el) el.addEventListener('input', function() {
            var answers = {
                answer1: document.getElementById('answer1') ? document.getElementById('answer1').value : '',
                answer2: document.getElementById('answer2') ? document.getElementById('answer2').value : ''
            };
            localStorage.setItem('exam_answers_' + QID, JSON.stringify(answers));
        });
    });
</script>
</body>
</html>'''

tail_pattern = re.compile(r'\s*<!-- 解析区 -->.*$', re.DOTALL)
m_tail = tail_pattern.search(content)
if m_tail:
    content = content[:m_tail.start()] + FOOTER_125
    print('  1.2.5: footer added')
else:
    print('  1.2.5: WARN footer cutoff not found')

write('1.2.5', content)

print('\nAll done!')
