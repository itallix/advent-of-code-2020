import argparse

import pytest
from support import timing


def get_id(bottom, top, part, symbol):
    for s in part:
        if s == symbol:
            bottom = bottom + (top - bottom) // 2 + 1
        else:
            top = top - (top - bottom) // 2 - 1
    return bottom


def compute(s):
    ids = []
    for line in s.splitlines():
        r = get_id(0, 127, line[0:7], 'B')
        c = get_id(0, 7, line[7:10], 'R')
        ids.append(r * 8 + c)
    return max(ids)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ("FBFBBFFRLR", 357),
        ("BFFFBBFRRR", 567),
        ("FFFBBBFRRR", 119),
        ("BBFFBBFRLL", 820),
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
