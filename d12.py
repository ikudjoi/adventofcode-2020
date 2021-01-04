import os

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.readlines()

content_train = """F10
N3
F7
R90
F11""".splitlines()
#content = content_train

current_direction = 0
x = 0
y = 0


def trans(direc, d):
    if direc == 0: # east
        return d, 0
    if direc == 90: # north
        return 0, d
    if direc == 180: # west
        return -d, 0
    if direc == 270: # south
        return 0, -d
    raise Exception("perkele")


instructions = [(line[0], int(line[1:])) for line in content]
for ins, d in instructions:
    xt, yt = 0, 0
    if ins == 'F':
        xt, yt = trans(current_direction, d)
    elif ins == 'E':
        xt, yt = trans(0, d)
    elif ins == 'N':
        xt, yt = trans(90, d)
    elif ins == 'W':
        xt, yt = trans(180, d)
    elif ins == 'S':
        xt, yt = trans(270, d)
    elif ins == 'L':
        current_direction = (current_direction + d) % 360
    elif ins == 'R':
        current_direction = (current_direction - d) % 360
    else:
        raise Exception("saatana")
    x += xt
    y += yt

print(x)
print(y)
print(abs(x) + abs(y))

# part 2
x, y = 0, 0
wx, wy = 10, 1
for ins, d in instructions:
    wxt, wyt = 0, 0
    if ins == 'F':
        x += wx * d
        y += wy * d
    elif ins == 'E':
        wxt, wyt = trans(0, d)
    elif ins == 'N':
        wxt, wyt = trans(90, d)
    elif ins == 'W':
        wxt, wyt = trans(180, d)
    elif ins == 'S':
        wxt, wyt = trans(270, d)
    elif ins == 'L' or ins == 'R':
        # convert left turn to right turn
        if ins == 'L':
            d = -d % 360
        if d == 90:
            wx, wy = wy, -wx
        if d == 180:
            wx, wy = -wx, -wy
        if d == 270:
            wx, wy = -wy, wx
    else:
        raise Exception("saatana")
    wx += wxt
    wy += wyt

print(x)
print(y)
print(abs(x) + abs(y))