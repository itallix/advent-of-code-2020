import argparse

import pytest
from support import timing
from collections import Counter


def compute(s):
    total = 0
    for group in s.split("\n\n"):
        c = Counter()
        answers = group.split()
        for ga in answers:
            for a in ga:
                c[a] += 1
        total += len(list(filter(lambda x: x == len(answers), c.values())))
    return total


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

b""", 6
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
