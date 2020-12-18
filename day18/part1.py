import argparse

import pytest
from support import timing
from collections import deque
import re


def compute(s):
    stacks = []
    for expr in s.splitlines():
        stack = deque()
        for s in expr.replace(" ", ""):
            if s == ')' or re.match("\\d", s):
                if s == ')':
                    (a, _) = (stack.pop(), stack.pop())
                else:
                    a = int(s)
                if len(stack) > 0 and stack[-1] in ["+", "*"]:
                    (op, b) = (stack.pop(), stack.pop())
                    if op == '+':
                        stack.append(a + b)
                    elif op == '*':
                        stack.append(a * b)
                else:
                    stack.append(a)
            else:
                stack.append(s)
        stacks.append(stack)

    return sum([s.pop() for s in stacks])


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ("1 + 2 * 3 + 4 * 5 + 6", 71),
        ("2 * 3 + (4 * 5)", 26),
        ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
        ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632)
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
