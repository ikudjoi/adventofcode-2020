import os
import re

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.read()

train_content = "1 + 2 * 3 + 4 * 5 + 6"
#train_content = "1 + (2 * 3) + (4 * (5 + 6))"
#train_content = """1 + 2 * 3 + 4 * 5 + 6
#1 + (2 * 3) + (4 * (5 + 6))"""
train_content = "2 * 3 + (4 * 5)"
train_content = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
train_content = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
train_content = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
#content = train_content

inner_parenthesis = re.compile(r".*(\([^\(\)]+\)).*")
sum_stmt_pattern = re.compile(r".*(\b\d+ \+ \d+\b).*")


def calc_statement_without_parenthesis(stmt):
    items = stmt.split(' ')
    if len(items) == 2:
        raise Exception("Perkele")
    while len(items) > 2:
        atomic_stmt = "".join(items[:3])
        value = eval(atomic_stmt)
        del items[0]
        del items[0]
        items[0] = str(value)
    if not len(items) == 1:
        raise Exception("Saatana")
    return items[0]


def calc_sum1():
    calc_results = []
    for line in content.splitlines():
        m = inner_parenthesis.match(line)
        while m:
            inner_stmt = m.groups()[0]
            stmt_result = calc_statement_without_parenthesis(inner_stmt[1:-1])
            line = line.replace(inner_stmt, stmt_result)
            m = inner_parenthesis.match(line)
        res = calc_statement_without_parenthesis(line)
        calc_results.append(int(res))
    return calc_results


def calc_statement_without_parenthesis_sums_first(stmt):
    m = sum_stmt_pattern.match(stmt)
    while m:
        m.start()
        sum_stmt = m.groups()[0]
        stmt_result = eval(sum_stmt)
        start = m.start(1)
        end = m.end(1)
        # Replace is too greedy!
        stmt = stmt[:start] + str(stmt_result) + stmt[end:]
        m = sum_stmt_pattern.match(stmt)
    return calc_statement_without_parenthesis(stmt)


def calc_sum2():
    calc_results = []
    for line in content.splitlines():
        m = inner_parenthesis.match(line)
        while m:
            inner_stmt = m.groups()[0]
            stmt_result = calc_statement_without_parenthesis_sums_first(inner_stmt[1:-1])
            line = line.replace(inner_stmt, stmt_result)
            m = inner_parenthesis.match(line)
        res = calc_statement_without_parenthesis_sums_first(line)
        calc_results.append(int(res))
    return calc_results


# part 1
print(sum(calc_sum1()))
vals = calc_sum2()
print(sum(vals))