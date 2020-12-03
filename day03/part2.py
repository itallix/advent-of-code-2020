import argparse

import pytest
import math


def detect_trees(steps, s):
    trees = []
    lines = s.splitlines()
    for step in steps:
        (i, j) = step
        total = 0
        while j < len(lines):
            if lines[j][i] == '#':
                total += 1
            i = (i + step[0]) % len(lines[j])
            j += step[1]
        trees.append(total)
    return trees


def compute(s):
    # part1_steps = [(3, 1)]
    # trees = detect_trees(part1_steps, s)
    # print(trees[0])
    steps = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    trees = detect_trees(steps, s)
    return math.prod(trees)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ("""..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""", 336),
    ),
)
def test(input_s, expected):
    assert compute(input_s) == expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
