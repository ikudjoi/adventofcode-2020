import os
import math

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.readlines()

train_content = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""".splitlines()
#content = train_content

res_dict = {}

for line in content:
    line = line.strip()
    if line.startswith('mask = '):
        mask = line[7:]
        and_mask = int(mask.replace('X', '1'), 2)
        or_mask = int(mask.replace('X', '0'), 2)
    if line.startswith('mem['):
        slot, value = [int(i) for i in line[4:].split('] = ')]
        conv_value = (value & and_mask) | or_mask
        res_dict[slot] = conv_value

print(sum(res_dict.values()))

# part 2

train_content = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".splitlines()
#content = train_content


def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]

res_dict = {}

for line in content:
    line = line.strip()
    if line.startswith('mask = '):
        mask = line[7:]
        or_mask = int(mask.replace('X', '0'), 2)
        floats_to_zero_mask = int(mask.replace('0', '1').replace('X', '0'), 2)
        floating_bits = []
        for i, v in enumerate(reversed(list(mask))):
            if v != 'X':
                continue
            floating_bits.append(int(math.pow(2, i)))

    if line.startswith('mem['):
        slot, value = [int(i) for i in line[4:].split('] = ')]
        min_conv_slot = (slot | or_mask) & floats_to_zero_mask
        combinations = powerset(floating_bits)
        for comb in combinations:
            conv_slot = min_conv_slot + sum(comb)
            res_dict[conv_slot] = value

print(sum(res_dict.values()))
