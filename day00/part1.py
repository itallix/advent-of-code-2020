import argparse

import pytest


def compute(s):
    # TODO: implement solution here!
    return 0


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
