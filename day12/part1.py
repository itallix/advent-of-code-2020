import argparse

import pytest
from support import timing
from dataclasses import dataclass
import re


@dataclass
class Navigation:
    dir: int
    x: int
    y: int

    def left(self, n):
        self.dir = (self.dir - n) % 360

    def right(self, n):
        self.dir = (self.dir + n) % 360

    def forward(self, n):
        if self.dir == 0:
            self.x += n
        elif self.dir == 180:
            self.x -= n
        elif self.dir == 90:
            self.y -= n
        elif self.dir == 270:
            self.y += n

    def east(self, n):
        self.x += n

    def west(self, n):
        self.x -= n

    def north(self, n):
        self.y += n

    def south(self, n):
        self.y -= n

    def dist(self):
        return abs(self.x) + abs(self.y)


def compute(s):
    instructions = [re.match("(\\A.)(\\d*)", line).groups() for line in s.splitlines()]
    moves = {'F': 'forward', 'S': 'south', 'N': 'north', 'L': 'left', 'R': 'right', 'W': 'west', 'E': 'east'}
    current = Navigation(0, 0, 0)
    [getattr(current, moves[ins[0]])(int(ins[1])) for ins in instructions]
    return current.dist()


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ("""F10
N3
F7
R90
F11""", 25),
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
