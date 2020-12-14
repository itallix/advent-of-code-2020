import argparse

import pytest
from support import timing
import re
import itertools


def compute(s):
    masks = [m for m in s.split("mask = ")]
    parsed = [m.splitlines() for m in masks if len(m) > 0]
    mem = {}
    for p in parsed:
        mask = p[0][::-1]
        for m in range(1, len(p)):
            groups = re.match("mem\\[(\\d+)\\] = (\\d+)", p[m]).groups()
            (mem_idx, target_value) = int(groups[0]), int(groups[1])
            target_idx = list("{:036b}".format(mem_idx))
            for i in range(0, len(mask)):
                if mask[i] in ["X", "1"]:
                    target_idx[len(mask) - i - 1] = mask[i]
            f_count = target_idx.count("X")
            prod = list(itertools.product([0, 1], repeat=f_count))
            for tup in prod:
                b_idx = "".join(target_idx).replace("X", "%s") % tup
                mem[int(b_idx, 2)] = target_value
    return sum(mem.values())


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
("""mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""", 208),
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
