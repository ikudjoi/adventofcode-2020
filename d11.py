import os
import copy

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.readlines()

content_alt = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".splitlines()

lines = [list(line.strip()) for line in content]
orig_lines = copy.deepcopy(lines)
height = len(lines)
width = len(lines[0])

while True:
    prev_lines = copy.deepcopy(lines)
    change_count = 0
    for x in range(width):
        for y in range(height):
            center_cell = prev_lines[y][x]
            if center_cell == '.':
                continue

            min_x, max_x = max(0, x-1), min(width-1, x+1)
            min_y, max_y = max(0, y-1), min(height-1, y+1)
            occupied_neighbors = 0
            for adj_x in range(min_x, max_x+1):
                for adj_y in range(min_y, max_y+1):
                    if adj_x == x and adj_y == y:
                        continue
                    if prev_lines[adj_y][adj_x] == '#':
                        occupied_neighbors += 1

            if occupied_neighbors == 0 and center_cell == 'L':
                lines[y][x] = '#'
                change_count += 1
            elif occupied_neighbors >= 4 and center_cell == '#':
                lines[y][x] = 'L'
                change_count += 1

    if change_count == 0:
        occupied_count = 0
        for line in lines:
            occupied_count += len([c for c in line if c == '#'])
        print(occupied_count)
        break

    with open('d11_result1.txt', 'w') as f:
        for line in lines:
            s = "".join(line) + '\n'
            f.write(s)


lines = orig_lines
while True:
    prev_lines = copy.deepcopy(lines)
    change_count = 0
    for x in range(width):
        for y in range(height):
            center_cell = prev_lines[y][x]
            if center_cell == '.':
                continue

            occupied_neighbors = 0
            for x_trans in range(-1, 2):
                for y_trans in range(-1, 2):
                    if x_trans == 0 and y_trans == 0:
                        continue
                    dist = 1
                    while True:
                        adj_x, adj_y = x + dist * x_trans, y + dist * y_trans
                        if adj_x < 0 or adj_y < 0:
                            break
                        if adj_x >= width or adj_y >= height:
                            break
                        if prev_lines[adj_y][adj_x] == '#':
                            occupied_neighbors += 1
                            break
                        if prev_lines[adj_y][adj_x] == 'L':
                            break
                        dist += 1

            if occupied_neighbors == 0 and center_cell == 'L':
                lines[y][x] = '#'
                change_count += 1
            elif occupied_neighbors >= 5 and center_cell == '#':
                lines[y][x] = 'L'
                change_count += 1

    if change_count == 0:
        occupied_count = 0
        for line in lines:
            occupied_count += len([c for c in line if c == '#'])
        print(occupied_count)
        break

    with open('d11_result2.txt', 'w') as f:
        for line in lines:
            s = "".join(line) + '\n'
            f.write(s)

    pass

