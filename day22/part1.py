import argparse

import pytest
from support import timing
from collections import deque

def compute(s):
    p1, p2 = deque(), deque()
    (deck1, deck2) = s.split("\n\n")
    [p1.appendleft(int(c)) for c in deck1.splitlines()[1:]]
    [p2.appendleft(int(c)) for c in deck2.splitlines()[1:]]

    while len(p1) and len(p2):
        n1, n2 = p1.pop(), p2.pop()
        if n1 > n2:
            p1.appendleft(n1)
            p1.appendleft(n2)
        else:
            p2.appendleft(n2)
            p2.appendleft(n1)

    winner = p1 if len(p1) else p2

    return sum([m * winner.popleft() for m in range(1, len(winner) + 1)])


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ("""Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10""", 306),
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
