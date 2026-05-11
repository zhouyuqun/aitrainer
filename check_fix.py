import os

base = r'C:\Users\76272\Documents\GitHub\aitrainer'
qids_4x = ['4.1.1','4.1.2','4.1.3','4.1.4','4.1.5','4.2.1','4.2.2','4.2.3','4.2.4','4.2.5']

for qid in qids_4x:
    path = os.path.join(base, qid, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    has_calc = 'calculateScore' in content or 'checkScore' in content
    has_score_div = 'id="scoreResult"' in content
    has_ans_div = 'id="answerComparison"' in content
    has_func_def = 'function calculateScore' in content or 'function checkScore' in content
    ends_ok = '</html>' in content[-100:]
    print(f'{qid}: call={has_calc} funcDef={has_func_def} scoreDiv={has_score_div} ansDiv={has_ans_div} ends_html={ends_ok}')

# 检查 1.x/2.x/3.x 是否也有问题
print('\n--- Checking 1.x/2.x/3.x ---')
for series in ['1.1','1.2','2.1','2.2','3.1','3.2']:
    for num in ['1','2','3','4','5']:
        qid = f'{series}.{num}'
        path = os.path.join(base, qid, 'index.html')
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        has_score_div = 'id="scoreResult"' in content
        has_ans_div = 'id="answerComparison"' in content
        has_func_def = 'function calculateScore' in content or 'btnCheck' in content
        ends_ok = '</html>' in content[-100:]
        if not (has_score_div and has_ans_div and ends_ok):
            print(f'  ISSUE {qid}: scoreDiv={has_score_div} ansDiv={has_ans_div} ends_html={ends_ok}')
        else:
            print(f'  OK    {qid}')
