import io
lines = io.open('data/rules.yml', encoding='utf-8').readlines()
new_lines = []
for i, l in enumerate(lines):
    if l.strip() == 'steps:' and not (new_lines and new_lines[-1].strip().startswith('- rule')):
        intent_line = lines[i+1].strip()
        if intent_line.startswith('- intent:'):
            intent = intent_line.split(':')[1].strip()
            new_lines.append(f'- rule: response to {intent}\n')
    new_lines.append(l)
io.open('data/rules.yml', 'w', encoding='utf-8').writelines(new_lines)
