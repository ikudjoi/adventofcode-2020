import os

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.read()

train_content = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
#content = train_content

_validity_rules, my_ticket, nearby_tickets = content.split('\n\n')

# Strip header
my_ticket = [int(i) for i in my_ticket.splitlines()[1].split(',')]

_validity_rules = dict([line.split(': ') for line in _validity_rules.splitlines()])
validity_rules = {}
for r_name, vrs in _validity_rules.items():
    ab, cd = vrs.split(' or ')
    a, b = [int(v) for v in ab.split('-')]
    c, d = [int(v) for v in cd.split('-')]

    def rule_factory(a, b, c, d):
        def rule(x):
            return a <= x <= b or c <= x <= d

        return rule

    rule = rule_factory(a, b, c, d)
    validity_rules[r_name] = rule

nearby_tickets = nearby_tickets.splitlines()[1:]
nearby_tickets = [[int(v) for v in t.split(',')] for t in nearby_tickets]

# part 1
error_rate = 0
valid_tickets = []
for values in nearby_tickets:

    ticket_valid = True
    for v in values:
        valid_found = False
        for rule in validity_rules.values():
            if rule(v):
                valid_found = True
                break
        if not valid_found:
            error_rate += v
            ticket_valid = False
            break
    if ticket_valid:
        valid_tickets.append(values)

print(error_rate)

# part 2
valid_rules_per_field = { i: list(validity_rules.keys()) for i in range(len(valid_tickets[0])) }

for values in valid_tickets:
    for idx, v in enumerate(values):
        valid_found = False
        for rule_name, rule in validity_rules.items():
            if not rule(v):
                if rule_name in valid_rules_per_field[idx]:
                    valid_rules_per_field[idx].remove(rule_name)

determined_fields = []
while any([rules for rules in valid_rules_per_field.values() if len(rules) > 1]):
    all_rules = list(valid_rules_per_field.values())
    unambiguous_rules = [rules[0] for rules in all_rules if len(rules) == 1 and rules[0] not in determined_fields]
    for rule in unambiguous_rules:
        for rules in valid_rules_per_field.values():
            if len(rules) == 1:
                continue
            if rule in rules:
                rules.remove(rule)
                if not rule in determined_fields:
                    determined_fields.append(rule)

res_prod = 1
for idx, rule in valid_rules_per_field.items():
    if rule[0].startswith('departure'):
        res_prod *= my_ticket[idx]

print(res_prod)