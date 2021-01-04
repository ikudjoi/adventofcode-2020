import os

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.readlines()

values = [int(v.strip()) for v in content]


def find_pair():
    for a in values:
        for b in values:
            if a + b == 2020:
                return a * b


def find_triplet():
    for a in values:
        for b in values:
            for c in values:
                if a + b + c == 2020:
                    return a * b * c


print(find_pair())
print(find_triplet())