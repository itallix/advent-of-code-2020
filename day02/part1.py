import argparse

import pytest
import re


def compute(s):
    total = 0
    parsed = [re.search("(\d+)-(\d+) ([a-z]{1}): ([a-z]*)", line) for line in s.splitlines()]
    for p in parsed:
        mn = int(p.group(1))
        mx = int(p.group(2))
        search = p.group(3)
        pwd = p.group(4)
        if mn <= pwd.count(search) <= mx:
            total += 1
    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('1-3 a: abcde\n1-3 b: cdefg\n2-9 c: ccccccccc', 2),
        ('1-3 g: abcde\n1-3 b: cdefg\n2-9 c: ccccccccc', 1)
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
