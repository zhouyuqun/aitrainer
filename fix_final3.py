import os, re

BASE = r'C:\Users\76272\Documents\GitHub\aitrainer'

def read(qid):
    with open(os.path.join(BASE, qid, 'index.html'), 'r', encoding='utf-8') as f:
        return f.read()
def write(qid, c):
    with open(os.path.join(BASE, qid, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(c)

# Fix 1.2.1: add answerComparison after scoreResult
content = read('1.2.1')
if 'id="answerComparison"' not in content:
    m = re.search(r'id=["\']scoreResult["\']', content)
    if m:
        end = content.find('</div>', m.end())
        if end != -1:
            alias = '\n<div id="answerComparison" style="display:none;"><div id="wrongAnswer"></div><div id="correctAnswer"></div></div>\n'
            content = content[:end+6] + alias + content[end+6:]
            write('1.2.1', content)
            print('1.2.1: added answerComparison')

# Fix 3.1.2, 3.1.3: add </html>
for qid in ['3.1.2', '3.1.3']:
    content = read(qid)
    if '</html>' not in content[-200:]:
        content = content.rstrip() + '\n</html>'
        write(qid, content)
        print(f'{qid}: added </html>')

print('Done!')
