import argparse
import re

import pytest
from support import timing


def execute(instructions):
    visited = []
    i = 0
    acc = 0
    while i not in visited:
        (ins, step) = instructions[i]
        visited.append(i)
        if ins == "acc":
            acc += int(step)
            i += 1
        elif ins == "jmp":
            i += int(step)
        else:
            i += 1
        if i == len(instructions):
            return True, acc
    return False, visited


def compute(s):
    instructions = [re.match("([nop|acc|jmp]+) ([+|-][\\d]+)", line).groups() for line in s.splitlines()]
    swaps = {
        "nop": "jmp",
        "jmp": "nop"
    }
    first_run = execute(instructions)
    if not first_run[0]:
        for i in first_run[1]:
            (op, _) = instructions[i]
            if op in ["nop", "jmp"]:
                instructions[i] = (swaps[op], instructions[i][1])
                (finished, acc) = execute(instructions)
                if finished:
                    return acc
                instructions[i] = (op, instructions[i][1])


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
""", 8),
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
