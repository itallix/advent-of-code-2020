import argparse

import pytest


def compute(s):
    nums = [int(line) for line in s.splitlines()]
    s = set()
    for i in range(0, len(nums)):
        if 2020 - nums[i] in s:
            return nums[i] * (2020 - nums[i])
        s.add(nums[i])


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('1000\n1020\n10', 1020000),
        ('100\n1920\n20', 192000),
        ('1010\n2019\n1', 2019),
        ('1010\n1010', 1020100),
        ('1010', None),
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
