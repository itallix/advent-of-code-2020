import argparse

import pytest
from support import timing


def compute(s):
    starting_nums = [int(n) for n in s.split(",")]
    spoken_nums = starting_nums.copy()
    for turn in range(len(starting_nums), 2020):
        last_spoken = spoken_nums[-1]
        freq = spoken_nums.count(last_spoken)
        if freq == 1:
            spoken_nums.append(0)
        else:
            no_last = spoken_nums[-2::-1]
            prev_index = len(no_last) - no_last.index(last_spoken) - 1
            spoken_nums.append(turn - 1 - prev_index)

    return spoken_nums[-1]


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ("0,3,6", 436),
        ("1,3,2", 1),
        ("2,1,3", 10),
        ("1,2,3", 27),
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
