import argparse

import pytest
from support import timing
from operator import concat
from functools import reduce


def compute(s):
    group_totals = [len(set(
        reduce(concat, [list(a) for a in group.split()]))
    ) for group in s.split("\n\n")]
    return sum(group_totals)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (
                """abc

a
b
c

ab
ac

a
a
a
a

b""", 11
            ),
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
