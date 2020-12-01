import argparse

import pytest


def compute(s):
    nums = [int(line) for line in s.splitlines()]
    for i in range(0, len(nums) - 1):
        s = set()
        curr_sum = 2020 - nums[i]
        for j in range(i + 1, len(nums)):
            if (curr_sum - nums[j]) in s:
                return nums[i] * nums[j] * (curr_sum - nums[j])
            s.add(nums[j])

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
