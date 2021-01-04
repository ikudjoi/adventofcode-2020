import os

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.read()

train_content = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""
#content = train_content


def reduce_line(value):
    e_count = value.count('ne')
    w_count = value.count('sw')
    c_ne = e_count - w_count
    value = value.replace('ne', '').replace('sw', '')

    e_count = value.count('se')
    w_count = value.count('nw')
    c_se = e_count - w_count
    value = value.replace('se', '').replace('nw', '')

    e_count = value.count('e')
    w_count = value.count('w')
    c_e = e_count - w_count

    return c_ne - c_se, c_e + c_se


reduced_coords = [reduce_line(line) for line in content.splitlines()]
counts = {}
for c in reduced_coords:
    if c in counts:
        counts[c] += 1
    else:
        counts[c] = 1

black_tiles = set([coord for coord, cnt in counts.items() if cnt % 2 == 1])
print(len(black_tiles))


def coord_neighbors(coord, itself):
    x, y = coord
    if itself:
        return [(x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y), (x, y + 1), (x + 1, y), (x + 1, y - 1)]
    else:
        return [(x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y), (x + 1, y - 1)]
    # if itself:
    #     return [(x-1, y-1), (x-1, y), (x, y-1), (x, y), (x, y+1), (x+1, y), (x+1, y+1)]
    # else:
    #     return [(x - 1, y - 1), (x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y), (x + 1, y + 1)]


prev_black = black_tiles
for round in range(100):
    all_potentially_flipping_tiles = [coord_neighbors(c, True) for c in prev_black]
    all_potentially_flipping_tiles = set([item for sublist in all_potentially_flipping_tiles for item in sublist])
    new_black = set()
    for tile in all_potentially_flipping_tiles:
        cnt_black = 0
        currently_black = (tile in prev_black)
        for n in coord_neighbors(tile, False):
            if n in prev_black:
                cnt_black += 1
        if currently_black and 1 <= cnt_black <= 2:
            new_black.add(tile)
        elif not currently_black and cnt_black == 2:
            new_black.add(tile)
    prev_black = new_black
    print(len(prev_black))



    pass
