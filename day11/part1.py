import argparse

import pytest
from support import timing
import copy


def compute(s):
    seat_layout = [list(line) for line in s.splitlines()]

    def get_neighbours(matrix, rn, cn):
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if rn + i == rn and cn + j == cn:
                    continue
                if (0 <= rn + i < len(matrix)) and (0 <= cn + j < len(matrix[rn])):
                    neighbours.append(matrix[rn + i][cn + j])
        return neighbours

    def visit_seat(layout, i, j, func):
        s = layout[i][j]
        if s == 'L':
            ns = func(layout, i, j)
            if all(x != '#' for x in ns):
                return '#', True
        elif s == '#':
            ns = func(layout, i, j)
            if len(list(filter(lambda x: x == '#', ns))) >= 4:
                return 'L', True
        return s, False

    def arrange_seats(layout):
        original = copy.deepcopy(layout)
        changed = False
        for i in range(0, len(layout)):
            for j in range(0, len(layout[i])):
                updated = visit_seat(original, i, j, get_neighbours)
                changed = changed or updated[1]
                layout[i][j] = updated[0]
        if changed:
            arrange_seats(layout)

    arrange_seats(seat_layout)

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
L.LLLLL.LL""", 37),
("""#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##""", 37),
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
