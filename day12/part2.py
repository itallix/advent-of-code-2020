import argparse

import pytest
from support import timing
from dataclasses import dataclass
import re


@dataclass
class Navigation:
    x: int
    y: int
    w: ()

    def left(self, n):
        for i in range(n // 90):
            self.w = (-self.w[1], self.w[0])

    def right(self, n):
        for i in range(n // 90):
            self.w = (self.w[1], -self.w[0])

    def forward(self, n):
        (x, y) = self.w
        self.x += n * x
        self.y += n * y

    def east(self, n):
        self.w = (self.w[0] + n, self.w[1])

    def west(self, n):
        self.w = (self.w[0] - n, self.w[1])

    def north(self, n):
        self.w = (self.w[0], self.w[1] + n)

    def south(self, n):
        self.w = (self.w[0], self.w[1] - n)

    def dist(self):
        return abs(self.x) + abs(self.y)


def compute(s):
    instructions = [re.match("(\\A.)(\\d*)", line).groups() for line in s.splitlines()]
    moves = {'F': 'forward', 'S': 'south', 'N': 'north', 'L': 'left', 'R': 'right', 'W': 'west', 'E': 'east'}
    current = Navigation(0, 0, (10, 1))
    [getattr(current, moves[ins[0]])(int(ins[1])) for ins in instructions]
    return current.dist()


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ("""F10
N3
F7
R90
F11""", 286),
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
