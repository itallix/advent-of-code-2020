import argparse

import pytest


def compute(s):
    total = 0
    for line in s.splitlines():
        values = line.split(" ")
        count = values[0].split("-")
        pos1 = int(count[0]) - 1
        pos2 = int(count[1]) - 1
        symbol = values[1][0]
        if symbol == values[2][pos1] and symbol != values[2][pos2] or symbol != values[2][pos1] and symbol == values[2][pos2]:
            total += 1
    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
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
