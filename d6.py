import os

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.read()

groups = content.split('\n\n')

# part 1
counts = []
for group in groups:
    no_newlines = group.replace('\n', '')
    distinct_chars = set(list(no_newlines))
    counts.append(len(distinct_chars))

print(sum(counts))

# part 2
counts = []
for group in groups:
    individuals = group.splitlines(keepends=False)
    distinct_answers = [set(list(i)) for i in individuals]
    intersection = None
    for answers in distinct_answers:
        if intersection is None:
            intersection = answers
            continue

        intersection = intersection.intersection(answers)

    counts.append(len(intersection))

print(sum(counts))