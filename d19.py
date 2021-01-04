import os
import re

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.read()

train_content = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
#content = train_content

rules, input = content.split('\n\n')
rules = {int(line.split(': ')[0]): line.split(': ')[1] for line in rules.splitlines()}
input = input.splitlines()

def gen_regex_for_rule(rule_num):
    rule = rules[rule_num]
    alt_rules = [rule]
    if ' | ' in rule:
        alt_rules = rule.split(' | ')
    alt_regexes = []
    for ar in alt_rules:
        if '"' in ar:
            alt_regexes.append(ar.strip('"'))
            continue

        alt_rules = ar.split(' ')
        sub_regexes = [gen_regex_for_rule(int(sr)) if sr.isdigit() else sr for sr in alt_rules]
        alt_regexes.append("".join(sub_regexes))

    if len(alt_regexes) == 1:
        return alt_regexes[0]

    return f"({'|'.join(alt_regexes)})"


r0 = gen_regex_for_rule(0)
r0 = rf"^{r0}$"

mp = re.compile(r0)
match_count = 0
for line in input:
    m = mp.match(line)
    if m:
        match_count += 1

print(match_count)

rules[8] = '42 +'
rules[11] = "42 (?: 42 (?: 42 (?: 42 (?: 42 (?: 42 31 )? 31 )? 31 )? 31 )? 31 )? 31"
new_r0 = gen_regex_for_rule(0)
new_r0 = rf"^{new_r0}$"

mp = re.compile(new_r0)
match_count = 0
for line in input:
    m = mp.match(line)
    if m:
        match_count += 1

print(match_count)

#8: 42 | 42 8
#11: 42 31 | 42 11 31

