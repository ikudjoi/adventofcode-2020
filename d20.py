import os
import math
import numpy

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.read()

train_content = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""
#content = train_content

tiles = content.split('\n\n')


class Tile:
    def __init__(self, str_content):
        self.unique_hashes = []
        tile_lines = str_content.splitlines()
        self.tile_num = int(tile_lines[0].split(' ')[1][:-1])
        tile_lines = tile_lines[1:]
        self.size = len(tile_lines)
        self.a = numpy.full((self.size, self.size), 0, dtype=int)
        for row, line in enumerate(tile_lines):
            for col, c in enumerate(list(line)):
                if c == '#':
                    self.a[row][col] = 1
        pass

    def top_border(self):
        return self.a[0]

    def top_hash(self):
        return self.tile_border_hash(self.top_border())

    def right_border(self):
        return self.a[:,-1]

    def right_hash(self):
        return self.tile_border_hash(self.right_border())

    def bottom_border(self):
        return self.a[-1]

    def bottom_hash(self):
        return self.tile_border_hash(self.bottom_border())

    def left_border(self):
        return self.a[:,0]

    def left_hash(self):
        return self.tile_border_hash(self.left_border())

    def top_unique(self):
        if not self.unique_hashes:
            return False
        return self.top_hash() in self.unique_hashes

    def right_unique(self):
        if not self.unique_hashes:
            return False
        return self.right_hash() in self.unique_hashes

    def bottom_unique(self):
        if not self.unique_hashes:
            return False
        return self.bottom_hash() in self.unique_hashes

    def left_unique(self):
        if not self.unique_hashes:
            return False
        return self.left_hash() in self.unique_hashes

    @staticmethod
    def tile_border_hash(border):
        return min(hash(tuple(border)), hash(tuple(reversed(border))))

    def all_hashes(self):
        return {self.top_hash(), self.right_hash(), self.bottom_hash(), self.left_hash()}

    def rotate_right(self, times=1):
        for _ in range(times):
            self.__rotate_right_once()

    def __rotate_right_once(self):
        self.a = numpy.rot90(self.a)

    def flipud(self):
        self.a = numpy.flipud(self.a)

    def fliplr(self):
        self.a = numpy.fliplr(self.a)

    def flip(self):
        pass


tiles = [Tile(tile) for tile in tiles]
tiles = {t.tile_num: t for t in tiles}

tile_border_hashes = {t.tile_num: t.all_hashes() for t in tiles.values()}
hash_occurrences_in_tiles = {}
for tile_num, tile_hashes in tile_border_hashes.items():
    for hsh in tile_hashes:
        if hsh not in hash_occurrences_in_tiles:
            hash_occurrences_in_tiles[hsh] = set()
        hash_occurrences_in_tiles[hsh].add(tile_num)

tiles_with_two_non_matching_sides = []
for tile_num, tile_hashes in tile_border_hashes.items():
    count_hashes_with_no_matches = 0
    uniq_hashes = set()
    for hsh in tile_hashes:
        if len(hash_occurrences_in_tiles[hsh]) == 1:
            count_hashes_with_no_matches += 1
            uniq_hashes.add(hsh)
    tiles[tile_num].unique_hashes = (tiles[tile_num].all_hashes() & uniq_hashes)
    if count_hashes_with_no_matches == 2:
        tiles_with_two_non_matching_sides.append(tile_num)

# There luckily are exactly four of them for train and actual input
print(math.prod(tiles_with_two_non_matching_sides))

# part 2
sq_size = int(math.sqrt(len(tiles)))
start_tile = tiles_with_two_non_matching_sides[0]
start_tile = tiles[start_tile]
while not start_tile.left_unique() or not start_tile.top_unique():
    start_tile.rotate_right()

# construct grid
rows = []
previous_row = None
current_row = [start_tile]
col = 2
left_tile = start_tile
while len(rows) < sq_size:
    above_tile = None
    while len(current_row) < sq_size:
        if previous_row:
            above_tile = previous_row[col-1]

        req_left_hash = left_tile.right_hash() if left_tile else None
        req_top_hash = above_tile.bottom_hash() if above_tile else None

        search_next_tile_by_hash = req_left_hash if req_left_hash else req_top_hash
        prev_tile = left_tile if left_tile else above_tile
        next_tiles = [tile_num for tile_num in hash_occurrences_in_tiles[search_next_tile_by_hash] if tile_num != prev_tile.tile_num]
        if len(next_tiles) != 1:
            raise Exception("saatana")
        next_tile = tiles[next_tiles[0]]
        if req_left_hash:
            while next_tile.left_hash() != req_left_hash:
                next_tile.rotate_right()
            prb = left_tile.right_border()
            nlb = next_tile.left_border()
            if not (prb == nlb).all():
                next_tile.flipud()
                nlb = next_tile.left_border()
                if not (prb == nlb).all():
                    raise Exception("perkele")
        else:
            while next_tile.top_hash() != req_top_hash:
                next_tile.rotate_right()
            abb = above_tile.bottom_border()
            ntb = next_tile.top_border()
            if not (abb == ntb).all():
                next_tile.fliplr()
                ntb = next_tile.top_border()
                if not (abb == ntb).all():
                    raise Exception("hemmetti")

        current_row.append(next_tile)
        left_tile = next_tile
        col += 1

    rows.append(current_row)
    previous_row = current_row
    current_row = []
    left_tile = None
    col = 1

tile_size = next_tile.size
big_sq_size = tile_size * sq_size
reduced_size = (tile_size - 2) * sq_size
big_sq = numpy.full((reduced_size, reduced_size), 0, dtype=int)
for i in range(big_sq_size):
    bit_line = []
    line = int(i / tile_size)
    tile_line = i % tile_size
    for j in range(sq_size):
        line_con = rows[line][j].a[tile_line]
        bit_line.extend(line_con)
        if tile_line == 0 or tile_line == tile_size - 1:
            continue
        for a, b in enumerate(line_con[1:(tile_size-1)]):
            if b == 0:
                continue

            big_sq[(tile_size - 2)*line + (tile_line - 1)][(tile_size - 2)*j + a] = 1
    str = "".join(['#' if b == 1 else ' ' for b in bit_line])
    #print(str)
pass

sea_monster_str = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.strip('\n')
monster_relative_coordinates = []
for row, line in enumerate(sea_monster_str.splitlines()):
    for col, c in enumerate(list(line)):
        if c == '#':
            monster_relative_coordinates.append((col, row))

monster_width = max([x for x, _ in monster_relative_coordinates]) + 1
monster_height = max([y for _, y in monster_relative_coordinates]) + 1


def monster_count():
    match_cnt = 0
    for x in range(reduced_size-monster_width):
        for y in range(reduced_size-monster_height):
            all_match = True
            for mrx, mry in monster_relative_coordinates:
                mx = x + mrx
                my = y + mry
                if big_sq[mx, my] == 0:
                    all_match = False
                    break
            if all_match:
                match_cnt += 1
    return match_cnt


# This seems to flip the pic right.
big_sq = numpy.flipud(big_sq)
big_sq = numpy.rot90(big_sq)
big_sq = numpy.rot90(big_sq)
big_sq = numpy.rot90(big_sq)
mc = monster_count()
tot_cnt = numpy.sum(big_sq)
print(tot_cnt - mc*len(monster_relative_coordinates))


#
# print(monster_count())
# big_sq = numpy.rot90(big_sq)
# print(monster_count())
# big_sq = numpy.rot90(big_sq)
# print(monster_count())
# big_sq = numpy.rot90(big_sq)
# print(monster_count())
# big_sq = numpy.flipud(big_sq)
# print(monster_count())
# big_sq = numpy.rot90(big_sq)
# print(monster_count())
# big_sq = numpy.rot90(big_sq)
# print(monster_count())
# big_sq = numpy.rot90(big_sq)
# print(monster_count())

