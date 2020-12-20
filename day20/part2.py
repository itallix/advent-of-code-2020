import argparse
import math
import re

import pytest
from support import timing


SM_PATTERN = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """


class Tile:
    def __init__(self, tid, data):
        self.id = tid
        self.data = data
        self.edges = [
            self.data[0],
            "".join([i[-1] for i in self.data]),
            self.data[-1],
            "".join([i[0] for i in self.data])
        ]

    def top(self):
        return self.edges[0]

    def right(self):
        return self.edges[1]

    def bottom(self):
        return self.edges[2]

    def left(self):
        return self.edges[3]

    def h_flip(self):
        return Tile(self.id, [r[::-1] for r in self.data])

    def v_flip(self):
        return Tile(self.id, self.data[::-1])

    def rotate(self):
        return Tile(self.id, ["".join(r) for r in zip(*self.data[::-1])])

    def crop(self):
        return [r[1:-1] for r in self.data[1:-1]]


def compute(s):

    tiles = [
        Tile(int(re.search("(\\d+)", lines[0]).group()), lines[1:])
        for lines in [t.splitlines() for t in s.split("\n\n")]
    ]
    size = int(math.sqrt(len(tiles)))

    candidates = []
    for t in tiles:
        for _ in range(2):
            candidates.extend([t, t.h_flip(), t.v_flip(), t.v_flip().h_flip()])
            t = t.rotate()

    def reassemble_image(image=None, seen=None, pos=(0, 0)):
        if not image:
            image = [[None for _ in range(size)] for _ in range(size)]
        if not seen:
            seen = set()

        x, y = pos
        if y == len(image):
            return image

        for tile in candidates:
            if tile.id in seen:
                continue

            if x > 0 and image[y][x - 1].right() != tile.left():
                continue

            if y > 0 and image[y - 1][x].bottom() != tile.top():
                continue

            image[y][x] = tile
            result = reassemble_image(
                image,
                seen | {tile.id},
                (x + 1, y) if x < len(image[0]) - 1 else (0, y + 1)
            )
            if result is not None:
                return result

        return None

    img = reassemble_image()
    img_s = []
    for row in img:
        pr = [[] for _ in range(len(row[0].bottom()) - 2)]
        for tile in row:
            for i, crop in enumerate(tile.crop()):
                pr[i] += [c for c in crop]
        img_s += pr

    def rotate(pixels):
        return [list(r) for r in zip(*pixels[::-1])]

    def h_flip(pixels):
        return [r[::-1] for r in pixels]

    def v_flip(pixels):
        return pixels[::-1]

    def mark_sea_monsters(image):
        x, y = 0, 0
        pp = []
        for i, l in enumerate(SM_PATTERN.splitlines()):
            for j, c in enumerate(l):
                if c == '#':
                    pp.append((i, j))

        sea_monsters = 0
        rows, cols = len(image), len(image[0])

        while y < rows - 3:
            while x < cols - 20:
                if [image[y + p[0]][x + p[1]] for p in pp].count('#') == len(pp):
                    sea_monsters += 1
                    for p in pp:
                        image[y + p[0]][x + p[1]] = '0'
                    x += 20
                else:
                    x += 1

            x, y = 0, y + 1

        return sea_monsters

    for _ in range(2):
        try:
            img_s = next(
                o for o in [img_s, h_flip(img_s), v_flip(img_s), h_flip(v_flip(img_s))]
                if mark_sea_monsters(o)
            )
        except StopIteration:
            img_s = rotate(img_s)

    return sum(row.count('#') for row in img_s)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
("""Tile 2311:
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
..#.###...""", 273),
    ),
)
def test(input_s, expected):
    assert compute(input_s) == expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
