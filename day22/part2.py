import argparse
from collections import deque

import pytest
from support import timing


def compute(s):
    p1, p2 = deque(), deque()
    (deck1, deck2) = s.split("\n\n")
    [p1.append(int(c)) for c in deck1.splitlines()[1:]]
    [p2.append(int(c)) for c in deck2.splitlines()[1:]]

    def clone_deck(stack, n):
        copy = deque()
        [copy.append(stack.popleft()) for _ in range(0, n)]
        return copy

    def recursive_combat(r1, r2, round_history=None):  # returns True if player 1 wins
        if not round_history:
            round_history = []
        while len(r1) and len(r2):
            round_conf = ''.join([str(c) for c in r1]).join([str(c) for c in r2])
            if round_conf in round_history:
                return True
            round_history.append(round_conf)
            c1, c2 = r1.popleft(), r2.popleft()
            if c1 <= len(r1) and c2 <= len(r2):
                p1_won = recursive_combat(
                    clone_deck(r1.copy(), c1),
                    clone_deck(r2.copy(), c2)
                )
                if p1_won:
                    r1.extend((c1, c2))
                else:
                    r2.extend((c2, c1))
            elif c1 > c2:
                r1.extend((c1, c2))
            else:
                r2.extend((c2, c1))

        return len(r1) > 0

    p1_won = recursive_combat(p1, p2)
    winner = p1 if p1_won else p2
    return sum([m * winner.pop() for m in range(1, len(winner) + 1)])


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
10""", 291),
#             ("""Player 1:
# 43
# 19
#
# Player 2:
# 2
# 29
# 14""", 12),
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
