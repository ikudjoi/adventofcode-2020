import os

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.readlines()

joltages = sorted([int(line) for line in content])
prev_jolt = 0

diff_counts = {1: 0, 3: 1}
for jolt in joltages:
    diff = jolt - prev_jolt
    prev_jolt = jolt
    diff_counts[diff] += 1

print(diff_counts[1] * diff_counts[3])

# part 2
lengths_of_continous_steps = []
current_length = 1
prev_jolt = 0
for jolt in joltages:
    diff = jolt - prev_jolt
    prev_jolt = jolt
    if diff == 1:
        current_length += 1
        continue

    if current_length > 2:
        lengths_of_continous_steps.append(current_length)

    current_length = 1

if current_length > 2:
    lengths_of_continous_steps.append(current_length)

multipliers = [2 if v == 3 else v for v in lengths_of_continous_steps]
multipliers = [7 if v == 5 else v for v in multipliers]
prod = 1
for v in multipliers:
    prod *= v
print(prod)

#
# 3 -> 2
# 4 -> 4
# 5 -> 7
#
# 1 2 3 4
# 1 3 4
# 1 2 4
# 1 4
#
# 1 2 3 4 5
# 1 2 3 5
# 1 2 4 5
# 1 3 4 5
# 1 2 5
# 1 3 5
# 1 4 5
