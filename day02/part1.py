import argparse

import pytest


def compute(s):
    total = 0
    for line in s.splitlines():
        values = line.split(" ")
        print(values)
        count = values[0].split("-")
        print(count)
        min = int(count[0])
        max = int(count[1])
        apps = 0
        for v in values[2]:
            if v == values[1][0]:
                apps += 1
        if min <= apps <= max:
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
