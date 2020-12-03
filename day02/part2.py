import argparse
import re

import pytest


def compute(s):
    total = 0
    parsed = [re.search("(\\d+)-(\\d+) ([a-z]+): ([a-z]*)", line) for line in s.splitlines()]
    for p in parsed:
        (pos1, pos2, search, pwd) = (int(p.group(1)) - 1, int(p.group(2)) - 1, p.group(3), p.group(4))

        def matches(pos):
            return search == pwd[pos]

        if (matches(pos1)) ^ (matches(pos2)):
            total += 1
    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('1-3 a: abcde', 1),
            ('1-3 b: cdefg', 0),
            ('2-9 c: ccccccccc', 0)
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
