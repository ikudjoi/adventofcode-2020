import os
from itertools import permutations


script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.readlines()

window_size = 25
numbers = [int(line) for line in content]


def additive_pair_exists(current_location):
    requested_sum = numbers[current_location]
    previous_window = numbers[(current_location-window_size):current_location]
    for a, b in permutations(previous_window, 2):
        if a > b:
            continue
        if a + b == requested_sum:
            return True
    return False


current_location = window_size

# part 1
while True:
    if additive_pair_exists(current_location):
        current_location += 1
        continue
    part_1_result = numbers[current_location]
    break

print(part_1_result)


def look_for_additive_range():
    window_size = 3
    while True:
        print(window_size)
        for current_location in range(window_size, len(numbers)):
            window = numbers[(current_location - window_size):current_location]
            if sum(window) == part_1_result:
                return min(window) + max(window)
        window_size += 1


# part 2
print(look_for_additive_range())