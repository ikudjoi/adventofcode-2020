import os

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.readlines()

tree_map = [row.strip() for row in content]
pattern_width = len(tree_map[0])
height = len(tree_map)


def tree_count(x_trans, y_trans):
    cnt = 0
    x = 0
    y = 0
    while y < height:
        if tree_map[y][x] == '#':
            cnt += 1
        y += y_trans
        x = (x + x_trans) % pattern_width
    return cnt


print(tree_count(3,1))
print(tree_count(1,1) * tree_count(3,1) * tree_count(5,1) * tree_count(7,1) * tree_count(1,2))
