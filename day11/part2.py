import argparse

import pytest
from support import timing
import copy
import itertools


def compute(s):
    seat_layout = [line for line in s.splitlines()]

    def get_visible(matrix, rn, cn):
        visible = []
        directions = list(filter(lambda x: x != (0, 0), list(itertools.product([-1, 0, 1], [-1, 0, 1]))))
        for d in directions:
            current = d
            while 0 <= rn + d[0] < len(matrix) and 0 <= cn + d[1] < len(matrix[0]):
                place = matrix[rn + d[0]][cn + d[1]]
                if place != '.':
                    visible.append(place)
                    break
                else:
                    d = (d[0] + current[0], d[1] + current[1])

        return visible

    def visit_seat(i, j, func):
        s = seat_layout[i][j]
        if s == 'L':
            ns = func(seat_layout, i, j)
            if all(x != '#' for x in ns):
                return '#', True
        elif s == '#':
            ns = func(seat_layout, i, j)
            if len(list(filter(lambda x: x == '#', ns))) >= 5:
                return 'L', True
        return s, False

    updated_layout = []
    while True:
        updated_layout.clear()
        changed = False
        for i in range(0, len(seat_layout)):
            updated_layout.append([])
            for j in range(0, len(seat_layout[i])):
                updated = visit_seat(i, j, get_visible)
                changed = changed or updated[1]
                updated_layout[i].append(updated[0])
        seat_layout = copy.deepcopy(updated_layout)
        if not changed:
            break

    # def printer():
    #     for r in seat_layout:
    #         for c in r:
    #             if c == '#':
    #                 print(c, end="")
    #         print()
    # printer()

    return [c for r in seat_layout for c in r].count('#')


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
("""L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""", 26),
("""#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##""", 26),
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
