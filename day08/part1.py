import argparse
import re

import pytest
from support import timing


def compute(s):
    visited = set()
    acc = 0
    instructions = [re.match("([nop|acc|jmp]+) ([+|-][\\d]+)", line).groups() for line in s.splitlines()]
    i = 0
    while True:
        if i in visited:
            break
        (ins, step) = instructions[i]
        visited.add(i)
        if ins == "acc":
            acc += int(step)
        elif ins == "jmp":
            i += int(step)
            continue
        i += 1
    return acc


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ("""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""", 5),
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
