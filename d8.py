import os
import copy

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.readlines()

orig_rules_with_indices = {idx: val.strip().split(' ') for idx, val in enumerate(content)}


def run_program(rules_with_indices):
    accumulator = 0
    visited_indices = set()
    current_index = 0
    while current_index not in visited_indices:
        visited_indices.add(current_index)
        if current_index >= len(rules_with_indices):
            return accumulator, True
        rule, value = rules_with_indices[current_index]
        value = int(value)

        if rule == 'acc':
            accumulator += value
            current_index += 1
        elif rule == 'jmp':
            current_index += value
        elif rule == 'nop':
            current_index += 1
        else:
            raise Exception(f"Invalid rule {rule}!")

    return accumulator, False


# part 1
acc, _ = run_program(orig_rules_with_indices)
print(acc)


# part 2
for i in range(len(orig_rules_with_indices)):
    rule, value = orig_rules_with_indices[i]
    if rule == 'acc':
        continue

    modified_rules = copy.deepcopy(orig_rules_with_indices)
    modified_rules[i][0] = 'nop' if rule == 'jmp' else 'jmp'
    acc, program_exited_normally = run_program(modified_rules)
    if program_exited_normally:
        print(acc)
        break

