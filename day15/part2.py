import argparse

import pytest
from support import timing


def compute(s):
    starting_nums = [int(n) for n in s.split(",")]
    spoken_nums = {v: k for k, v in enumerate(starting_nums)}
    last_spoken = 0
    for turn in range(len(starting_nums) + 1, 30_000_000):
        prev_spoken = spoken_nums.get(last_spoken)
        spoken_nums.update({last_spoken: turn - 1})
        if prev_spoken is None:
            last_spoken = 0
        else:
            last_spoken = turn - 1 - prev_spoken
    return last_spoken


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ("0,3,6", 175594),
        ("1,3,2", 2578),
        ("2,1,3", 3544142),
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
