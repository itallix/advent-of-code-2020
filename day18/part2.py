import argparse

import pytest
from support import timing
from collections import deque
import re
import math


def compute(s):
    stacks = []
    for expr in s.splitlines():
        stack = deque()
        for s in expr.replace(" ", ""):
            if s == ')':
                (a, x) = stack.pop(), stack.pop()
                if len(stack) > 0 and x == "*":
                    es = [a]
                    while stack[-1] != '(':
                        e = stack.pop()
                        if e != '*':
                            es.append(e)
                    stack.pop()
                    prod = math.prod(es)
                    if len(stack) > 0 and stack[-1] == "+":
                        stack.pop()
                        stack.append(prod + stack.pop())
                    else:
                        stack.append(prod)
                elif len(stack) > 0 and (x == "+" or stack[-1] == "+"):
                    (_, b) = stack.pop(), stack.pop()
                    stack.append(a + b)
                else:
                    stack.append(a)
            elif re.match("\\d", s):
                if len(stack) > 0 and stack[-1] == "+":
                    (_, a) = (stack.pop(), stack.pop())
                    stack.append(a + int(s))
                else:
                    stack.append(int(s))
            else:
                stack.append(s)
        stack.append(math.prod([e for e in [stack.pop() for _ in range(0, len(stack))] if e != '*']))
        stacks.append(stack)

    return sum([s.pop() for s in stacks])


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ("1 + 2 * 3 + 4 * 5 + 6", 231),
        ("2 * 3 + (4 * 5)", 46),
        ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
        ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340),
        ("(3 + 4 + 8) + 6 * (7 * 6 * (9 * 3 * 5 * 5 * 4 * 5) + (6 + 4) * (5 * 2 * 3 + 3) + (2 * 7)) + 2 * 4", 3527082888),
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
