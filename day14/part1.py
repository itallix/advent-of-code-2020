import argparse

import pytest
from support import timing
import re


def compute(s):
    masks = [m for m in s.split("mask = ")]
    parsed = [m.splitlines() for m in masks if len(m) > 0]
    mem = {}
    for p in parsed:
        mask = p[0][::-1]
        for m in range(1, len(p)):
            groups = re.match("mem\\[(\\d+)\\] = (\\d+)", p[m]).groups()
            (idx, val) = int(groups[0]), int(groups[1])
            for i in range(0, len(mask)):
                if mask[i] == "1":
                    val |= (1 << i)
                if mask[i] == "0":
                    val &= ~(1 << i)
            mem[idx] = val

    return sum(mem.values())


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
("""mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""", 165),
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
