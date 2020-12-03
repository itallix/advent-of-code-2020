import argparse

import pytest


def compute(s):
    total = 0
    i = 0
    for line in s.splitlines()[1:]:
        i = (i + 3) % len(line)
        if line[i] == '#':
            total += 1
    return total


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
.#..#...#.#""", 7),
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
