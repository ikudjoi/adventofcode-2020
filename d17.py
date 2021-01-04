import copy
from itertools import product

content = """..##.##.
#.#..###
##.#.#.#
#.#.##.#
###..#..
.#.#..##
#.##.###
#.#..##."""

train_content = """.#.
..#
###"""
#content = train_content


def create_initial_coordinates(content, dims):
    init_coords = []
    null_c = [0]*dims
    for y, line in enumerate(content.splitlines()):
        for x, c in enumerate(list(line)):
            if c == '#':
                v = copy.deepcopy(null_c)
                v[0] = x
                v[1] = y
                init_coords.append(tuple(v))
    return init_coords


def nearby_count(active_coords, vec):
    cnt = 0
    ranges = []
    for xn in vec:
        dim_range = range(xn-1, xn+2)
        ranges.append(dim_range)
    for nearby in product(*ranges):
        if nearby == vec:
            continue

        if nearby in active_coords:
            cnt += 1
    return cnt


def coordinate_boundaries(active_coords, extend_by_one=False):
    ranges = []
    mins, maxes = list(copy.deepcopy(active_coords[0])), list(copy.deepcopy(active_coords[0]))
    for vec in active_coords[1:]:
        for i, xn in enumerate(vec):
            if xn < mins[i]:
                mins[i] = xn
            if xn > maxes[i]:
                maxes[i] = xn

    for i in range(len(active_coords[0])):
        x_min, x_max = mins[i], maxes[i]
        if extend_by_one:
            x_min -= 1
            x_max += 1
        ranges.append(range(x_min, x_max + 1))

    return ranges


def print_layers(rnd, act_coord):
    print(f"round: {rnd}")
    if len(act_coord[0]) > 3:
        return

    bx, by, bz = coordinate_boundaries(act_coord)
    for z in bz:
        print(f"z={z}")
        for y in by:
            for x in bx:
                c = '#' if (x,y,z) in act_coord else '.'
                print(c, end='')
            print('')
        print('')
    print('')


def run_iteration(dims, iterations):
    active_coordinates = create_initial_coordinates(content, dims)
    for rnd in range(iterations):
        print_layers(rnd, active_coordinates)
        prev_coordinates = copy.deepcopy(active_coordinates)
        ranges = coordinate_boundaries(active_coordinates, extend_by_one=True)
        for v in product(*ranges):
            nc = nearby_count(prev_coordinates, v)
            if nc == 3:
                if v not in active_coordinates:
                    active_coordinates.append(v)
                continue
            if nc == 2:
                # preserve state
                continue
            if v in active_coordinates:
                active_coordinates.remove(v)
        pass

    print_layers(iterations, active_coordinates)
    print(len(active_coordinates))


# part 1
run_iteration(3, 6)
# part 2, painfully slow!!
run_iteration(4, 6)