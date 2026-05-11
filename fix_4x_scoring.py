#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_4x_scoring.py
修复 4.1.x 和 4.2.x 题目的评分明细显示问题：
1. 修复顶部 <script> 块的破损代码（乱码行、引号不闭合）
2. 为 4.1.x 添加完整的 calculateScore / showAnswers / resetForm 函数 + 页脚 div
3. 为 4.2.x 添加完整的 checkScore / resetAll 函数 + scoreResult / answerComparison div
"""

import re
import os

BASE = r'C:\Users\76272\Documents\GitHub\aitrainer'

# ─────────────────────────────────────────────
# 4.2.x 各题正确答案
# ─────────────────────────────────────────────
ANSWERS_42 = {
    '4.2.1': {
        'q1': '顾客的年龄、性别、购买历史和偏好等信息',
        'q2': '处理缺失值、去除重复记录、纠正错误数据',
        'q3': '将不同来源的数据统一格式，如日期格式、货币单位',
        'q4': '利用机器学习算法分析顾客购买模式，预测库存需求，优化定价策略',
        'q5': '提升顾客满意度、增加销售额和优化库存管理',
    },
    '4.2.2': {
        'q1': '专业医学影像标注（由经验丰富的医生对影像进行标注，标记病灶位置、类型、大小等关键信息）',
        'q2': '去除噪声、校正对比度、归一化像素值，使影像数据适合模型输入',
        'q3': '使用标注数据集训练AI模型，通过交叉验证等方法评估模型性能',
        'q4': '在未参与训练的测试集上评估模型，根据结果调整模型参数提高准确性',
        'q5': '模型对新疾病类型的识别准确率和泛化能力',
    },
    '4.2.3': {
        'q1': '监控区域',
        'q2': '数据存储系统',
        'q3': '对视频帧进行降噪、增强和压缩，提高后续分析的准确性和效率',
        'q4': '利用深度学习模型分析视频中人员行为，识别可疑或异常行为并触发警报',
        'q5': '异常行为识别的准确率和响应速度',
    },
    '4.2.4': {
        'q1': '整合摄像头、雷达、激光雷达（LiDAR）等多种传感器数据，提高感知精度',
        'q2': '覆盖多种驾驶场景，如城市、高速、山区、雨天、夜间等，确保数据多样性',
        'q3': '建立自动质量检查流程，过滤低质量或损坏的数据，确保数据集的可靠性',
        'q4': '标注员培训',
        'q5': '高质量、结构化的',
    },
    '4.2.5': {
        'q1': 'LabelImg、CVAT 或 VGG Image Annotator（VIA）',
        'q2': '能够自动识别文化遗产特定特征',
        'q3': '多学科协作',
        'q4': '加密技术',
        'q5': '增强现实（AR）或虚拟现实（VR）',
    },
}

# 4.1.x 题目标题（用于日志）
TITLES_41 = {
    '4.1.1': '数据标注',
    '4.1.2': '网页爬虫',
    '4.1.3': '数据清洗',
    '4.1.4': 'Pandas数据清洗',
    '4.1.5': '数据可视化',
}

# ─────────────────────────────────────────────
# 正确的顶部 script 块模板（替换破损部分）
# ─────────────────────────────────────────────
def make_top_script_41(qid):
    return f'''<script>
        const QID = '{qid}';

        function getStudentInfo() {{
            return {{
                name: localStorage.getItem('exam_student_name') || '',
                id: localStorage.getItem('exam_student_id') || ''
            }};
        }}

        function resetAll() {{
            localStorage.removeItem('exam_score_' + QID);
            localStorage.removeItem('exam_done_' + QID);
            localStorage.removeItem('exam_wrong_' + QID);
            localStorage.removeItem('exam_answers_' + QID);
            document.querySelectorAll('input[type=text], input[type=number], textarea').forEach(function(i){{i.value='';}});
            var el;
            el = document.getElementById('scoreResult'); if(el) el.style.display='none';
            el = document.getElementById('answerComparison'); if(el) el.style.display='none';
            el = document.getElementById('analysisBox'); if(el) el.style.display='none';
        }}

        // 重做本题（清除所有记录）
        function resetThisQuestion() {{
            if (!confirm('确定要重做本题吗？成绩记录将被清除。')) return;
            localStorage.removeItem('exam_score_' + QID);
            localStorage.removeItem('exam_done_' + QID);
            localStorage.removeItem('exam_wrong_' + QID);
            localStorage.removeItem('exam_answers_' + QID);
            document.querySelectorAll('.answer-input').forEach(function(i){{i.value='';}});
            var el;
            el = document.getElementById('scoreResult'); if(el) el.style.display='none';
            el = document.getElementById('answerComparison'); if(el) el.style.display='none';
            el = document.getElementById('analysisBox'); if(el) el.style.display='none';
            el = document.getElementById('finalScore'); if(el) el.textContent='?';
            alert('已重置，可重新作答！');
        }}
</script>'''


def make_top_script_42(qid):
    return f'''<script>
        const QID = '{qid}';

        function getStudentInfo() {{
            return {{
                name: localStorage.getItem('exam_student_name') || '',
                id: localStorage.getItem('exam_student_id') || ''
            }};
        }}

        function resetAll() {{
            localStorage.removeItem('exam_score_' + QID);
            localStorage.removeItem('exam_done_' + QID);
            localStorage.removeItem('exam_wrong_' + QID);
            localStorage.removeItem('exam_answers_' + QID);
            document.querySelectorAll('input[type=text], input[type=number], textarea').forEach(function(i){{i.value='';}});
            var el;
            el = document.getElementById('scoreResult'); if(el) el.style.display='none';
            el = document.getElementById('answerComparison'); if(el) el.style.display='none';
            el = document.getElementById('analysisBox'); if(el) el.style.display='none';
        }}

        // 重做本题（清除所有记录）
        function resetThisQuestion() {{
            if (!confirm('确定要重做本题吗？成绩记录将被清除。')) return;
            localStorage.removeItem('exam_score_' + QID);
            localStorage.removeItem('exam_done_' + QID);
            localStorage.removeItem('exam_wrong_' + QID);
            localStorage.removeItem('exam_answers_' + QID);
            document.querySelectorAll('.blank-input').forEach(function(i){{i.value='';}});
            var el;
            el = document.getElementById('scoreResult'); if(el) el.style.display='none';
            el = document.getElementById('answerComparison'); if(el) el.style.display='none';
            el = document.getElementById('analysisBox'); if(el) el.style.display='none';
            el = document.getElementById('finalScore'); if(el) el.textContent='?';
            alert('已重置，可重新作答！');
        }}
</script>'''


# ─────────────────────────────────────────────
# 4.1.x 页脚：scoreResult + answerComparison + 完整 script
# ─────────────────────────────────────────────
FOOTER_41 = '''
        </div><!-- end btn-group -->

        <div id="scoreResult" style="display:none;text-align:center;font-size:18px;font-weight:bold;
            color:#e74c3c;margin-top:15px;padding:12px;background:#fff5f5;border-radius:6px;">
            本次得分：<span id="finalScore">0</span> / 25 分
        </div>

        <div id="answerComparison" style="display:none;margin-top:15px;padding:15px;
            background:#f8f9fa;border-radius:6px;border:1px solid #dee2e6;">
            <div style="font-weight:bold;margin-bottom:10px;color:#2c5282;">答案对比</div>
            <div id="wrongAnswer"></div>
            <div id="rightAnswer" style="margin-top:8px;"></div>
        </div>

    </div><!-- end right-answer -->
</div><!-- end container -->

<script>
    // 模糊匹配
    function fuzzyMatch(user, correct) {
        if (!user) return false;
        user = user.trim().toLowerCase().replace(/\\s+/g, '');
        correct = correct.trim().toLowerCase().replace(/\\s+/g, '');
        if (user === correct) return true;
        if (correct.length >= 4 && user.includes(correct.substring(0, Math.floor(correct.length * 0.6)))) return true;
        if (user.length >= 4 && correct.includes(user.substring(0, Math.floor(user.length * 0.6)))) return true;
        return false;
    }

    // 页面加载还原答案
    window.addEventListener('DOMContentLoaded', function() {
        var saved = localStorage.getItem('exam_answers_' + QID);
        if (saved) {
            try {
                var answers = JSON.parse(saved);
                var inputs = document.querySelectorAll('.answer-input');
                var items = document.querySelectorAll('.question-item');
                items.forEach(function(item, idx) {
                    var input = item.querySelector('.answer-input');
                    if (input && answers['q' + (idx+1)]) input.value = answers['q' + (idx+1)];
                });
            } catch(e) {}
        }
        var score = localStorage.getItem('exam_score_' + QID);
        if (score !== null) {
            document.getElementById('finalScore').textContent = score;
            document.getElementById('scoreResult').style.display = 'block';
        }
    });

    // 自动保存答案
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.answer-input').forEach(function(input, idx) {
            input.addEventListener('input', function() {
                var answers = {};
                document.querySelectorAll('.answer-input').forEach(function(inp, i) {
                    answers['q' + (i+1)] = inp.value;
                });
                localStorage.setItem('exam_answers_' + QID, JSON.stringify(answers));
            });
        });
    });

    // 自动评分
    function calculateScore() {
        var items = document.querySelectorAll('.question-item');
        var total = 0;
        var wrongHtml = '';
        var rightHtml = '';

        items.forEach(function(item, idx) {
            var input = item.querySelector('.answer-input');
            var correctAttr = item.getAttribute('data-correct') || '';
            var scoreVal = parseInt(item.getAttribute('data-score') || '5');
            var label = item.querySelector('.question-text') ? item.querySelector('.question-text').textContent.trim() : ('第' + (idx+1) + '题');
            var userVal = input ? input.value.trim() : '';

            if (fuzzyMatch(userVal, correctAttr)) {
                total += scoreVal;
                rightHtml += '<div style="color:#27ae60;margin:4px 0;">✅ ' + label + ' <span style="color:#555">（+' + scoreVal + '分）</span></div>';
                if (input) { input.style.borderColor = '#27ae60'; input.style.backgroundColor = '#f0fff4'; }
            } else {
                wrongHtml += '<div style="color:#e74c3c;margin:4px 0;">❌ ' + label + '</div>';
                wrongHtml += '<div style="font-size:13px;color:#555;margin:2px 0 8px 16px;">你的答案：' + (userVal || '（未填写）') + '<br>正确答案：' + correctAttr + '</div>';
                if (input) { input.style.borderColor = '#e74c3c'; input.style.backgroundColor = '#fff0f0'; }
            }
        });

        document.getElementById('finalScore').textContent = total;
        document.getElementById('scoreResult').style.display = 'block';
        document.getElementById('answerComparison').style.display = 'block';
        document.getElementById('wrongAnswer').innerHTML = wrongHtml || '<div style="color:#27ae60;">全部正确！</div>';
        document.getElementById('rightAnswer').innerHTML = rightHtml;

        localStorage.setItem('exam_score_' + QID, total);
        localStorage.setItem('exam_done_' + QID, new Date().toISOString());
        if (wrongHtml) {
            localStorage.setItem('exam_wrong_' + QID, '1');
        } else {
            localStorage.removeItem('exam_wrong_' + QID);
        }
    }

    // 显示答案
    function showAnswers() {
        document.querySelectorAll('.correct-answer').forEach(function(el) {
            el.style.display = 'block';
        });
    }

    // 重置表单（不清除localStorage）
    function resetForm() {
        document.querySelectorAll('.answer-input').forEach(function(i) {
            i.value = '';
            i.style.borderColor = '';
            i.style.backgroundColor = '';
        });
        document.querySelectorAll('.correct-answer').forEach(function(el) {
            el.style.display = 'none';
        });
        document.getElementById('scoreResult').style.display = 'none';
        document.getElementById('answerComparison').style.display = 'none';
    }
</script>
</body>
</html>'''


# ─────────────────────────────────────────────
# 4.2.x 页脚：scoreResult + answerComparison + 完整 script
# ─────────────────────────────────────────────
def make_footer_42(qid):
    ans = ANSWERS_42[qid]

    scoring_js = ''
    for i, (k, v) in enumerate(ans.items(), 1):
        scoring_js += f"    {{ id: '{k}', ans: {repr(v)}, score: 5 }},\n"

    return f'''
        </div><!-- end btn-group -->

        <div id="scoreResult" class="result-box" style="display:none;background:#f0fff4;border:1px solid #9ae6b4;">
            <div class="score">本次得分：<span id="finalScore">0</span> / 25 分</div>
            <div class="answer-list" id="answerComparison"></div>
        </div>

    </div><!-- end answer-side -->
</div><!-- end main-box -->

<script>
    // 标准答案
    const scoring = [
{scoring_js}    ];

    // 模糊匹配
    function fuzzyMatch(user, correct) {{
        if (!user) return false;
        user = user.trim().toLowerCase().replace(/\\s+/g, '');
        correct = correct.trim().toLowerCase().replace(/\\s+/g, '');
        if (user === correct) return true;
        if (correct.length >= 4 && user.includes(correct.substring(0, Math.floor(correct.length * 0.6)))) return true;
        if (user.length >= 4 && correct.includes(user.substring(0, Math.floor(user.length * 0.6)))) return true;
        return false;
    }}

    // 页面加载还原答案
    window.addEventListener('DOMContentLoaded', function() {{
        var saved = localStorage.getItem('exam_answers_' + QID);
        if (saved) {{
            try {{
                var answers = JSON.parse(saved);
                Object.keys(answers).forEach(function(id) {{
                    var el = document.getElementById(id);
                    if (el) el.value = answers[id];
                }});
            }} catch(e) {{}}
        }}
        var score = localStorage.getItem('exam_score_' + QID);
        if (score !== null) {{
            document.getElementById('finalScore').textContent = score;
            document.getElementById('scoreResult').style.display = 'block';
        }}
    }});

    // 自动保存答案
    document.addEventListener('DOMContentLoaded', function() {{
        document.querySelectorAll('.blank-input').forEach(function(input) {{
            input.addEventListener('input', function() {{
                var answers = {{}};
                document.querySelectorAll('.blank-input').forEach(function(inp) {{
                    if (inp.id) answers[inp.id] = inp.value;
                }});
                localStorage.setItem('exam_answers_' + QID, JSON.stringify(answers));
            }});
        }});
    }});

    // 提交评分
    function checkScore() {{
        var total = 0;
        var html = '';

        scoring.forEach(function(item) {{
            var el = document.getElementById(item.id);
            var userVal = el ? el.value.trim() : '';
            var label = el ? (el.previousElementSibling ? el.previousElementSibling.textContent.trim() : item.id) : item.id;

            if (fuzzyMatch(userVal, item.ans)) {{
                total += item.score;
                html += '<div class="right">✅ ' + label + ' （+' + item.score + '分）</div>';
                if (el) {{ el.style.borderColor = '#38a169'; el.style.backgroundColor = '#f0fff4'; }}
            }} else {{
                html += '<div class="wrong">❌ ' + label + '</div>';
                html += '<div style="font-size:13px;color:#555;margin:2px 0 8px 16px;">你的答案：' + (userVal || '（未填写）') + '<br>正确答案：' + item.ans + '</div>';
                if (el) {{ el.style.borderColor = '#e53e3e'; el.style.backgroundColor = '#fff5f5'; }}
            }}
        }});

        document.getElementById('finalScore').textContent = total;
        document.getElementById('scoreResult').style.display = 'block';
        document.getElementById('answerComparison').innerHTML = html;

        localStorage.setItem('exam_score_' + QID, total);
        localStorage.setItem('exam_done_' + QID, new Date().toISOString());
        if (html.includes('❌')) {{
            localStorage.setItem('exam_wrong_' + QID, '1');
        }} else {{
            localStorage.removeItem('exam_wrong_' + QID);
        }}
    }}
</script>
</body>
</html>'''


# ─────────────────────────────────────────────
# 修复顶部破损 script 块的正则
# ─────────────────────────────────────────────
# 匹配从 <script> 到第一个 </script></script> 结束（4.x 特有的双 </script>）
BROKEN_SCRIPT_PATTERN = re.compile(
    r'<script>\s*\n\s*const QID\s*=\s*[\'"][^\'\"]+[\'"];.*?</script>\s*\n</script>',
    re.DOTALL
)


def fix_41(qid):
    path = os.path.join(BASE, qid, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 替换破损的顶部 script 块
    new_top = make_top_script_41(qid)
    content_new = BROKEN_SCRIPT_PATTERN.sub(new_top, content, count=1)
    if content_new == content:
        print(f'  WARN  {qid}: top script not matched, check manually')
    else:
        print(f'  OK  {qid}: top script replaced')

    # 2. 替换截断的文件尾部（从 btn-group 闭合到文件末尾）
    # 4.1.x 的文件在 </div>（最后一个）就截断了，我们找到 analysis-box 后的截断点
    # 用 </div>\n$ 作为截断标志（最后只有一个 </div> 且没有 script/body/html）
    # 匹配从 <!-- 解析区 --> 到文件末尾（分析框后面直接就没了）
    tail_pattern = re.compile(
        r'\s*<!-- 解析区 -->.*$',
        re.DOTALL
    )
    m = tail_pattern.search(content_new)
    if m:
        content_new = content_new[:m.start()] + FOOTER_41
        print(f'  OK  {qid}: footer added')
    else:
        print(f'  WARN  {qid}: footer cutoff not matched, check manually')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content_new)
    return content_new != content


def fix_42(qid):
    path = os.path.join(BASE, qid, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 替换破损的顶部 script 块
    new_top = make_top_script_42(qid)
    content_new = BROKEN_SCRIPT_PATTERN.sub(new_top, content, count=1)
    if content_new == content:
        print(f'  WARN  {qid}: top script not matched, check manually')
    else:
        print(f'  OK  {qid}: top script replaced')

    # 匹配从 <!-- 解析区 --> 到文件末尾
    tail_pattern = re.compile(
        r'\s*<!-- 解析区 -->.*$',
        re.DOTALL
    )
    m = tail_pattern.search(content_new)
    if m:
        content_new = content_new[:m.start()] + make_footer_42(qid)
        print(f'  OK  {qid}: footer added')
    else:
        print(f'  WARN  {qid}: footer cutoff not matched, check manually')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content_new)
    return content_new != content


if __name__ == '__main__':
    print('=== Fix 4.1.x ===')
    for qid in ['4.1.1', '4.1.2', '4.1.3', '4.1.4', '4.1.5']:
        print(f'Processing {qid}...')
        fix_41(qid)

    print('\n=== Fix 4.2.x ===')
    for qid in ['4.2.1', '4.2.2', '4.2.3', '4.2.4', '4.2.5']:
        print(f'Processing {qid}...')
        fix_42(qid)

    print('\nDone!')
