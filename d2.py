import os

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.readlines()

valid_count_part1 = 0
valid_count_part2 = 0
for line in content:
    min_max, letter, pwd = line.split(' ')
    min_v, max_v = [int(v) for v in min_max.split('-')]
    letter = letter.rstrip(':')
    letter_count = pwd.count(letter)
    if min_v <= letter_count <= max_v:
        valid_count_part1 += 1
    first_letter_match = pwd[min_v - 1] == letter
    second_letter_match = pwd[max_v - 1] == letter
    if first_letter_match != second_letter_match:
        valid_count_part2 += 1

print(valid_count_part1)
print(valid_count_part2)
