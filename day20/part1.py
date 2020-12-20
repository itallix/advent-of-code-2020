import argparse

import pytest
from support import timing
import math
import re
import itertools


class Tile:
    def __init__(self, tid, data):
        self.id = tid
        self.data = data
        self.edges = [
            self.data[0],
            "".join([i[0] for i in self.data]),
            self.data[-1],
            "".join([i[-1] for i in self.data])
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


def compute(s):

    tiles = [
        Tile(int(re.search("(\\d+)", lines[0]).group()), lines[1:])
        for lines in [t.splitlines() for t in s.split("\n\n")]
    ]
    size = int(math.sqrt(len(tiles)))

    candidates = []
    for t in tiles:
        for r in range(2):
            candidates.extend([t, t.h_flip(), t.v_flip()])
            candidates.append(candidates[-1].h_flip())
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

    res = reassemble_image()
    m = math.prod([res[p[0]][p[1]].id for p in list(itertools.product([0, -1], repeat=2))])
    return m


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
..#.###...""", 20899048083289),
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
