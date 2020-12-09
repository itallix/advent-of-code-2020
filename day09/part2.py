import argparse

import pytest
from support import timing
from itertools import combinations


def get_invalid(numbers, preamble):
    chunks = (numbers[x:x+preamble] for x in range(0, len(numbers) - preamble))
    i = 0
    for chunk in chunks:
        pairs = list(combinations(chunk, 2))
        target = numbers[preamble + i]
        if any(sum(p) == target for p in pairs) is not True:
            return target
        i += 1
    return 0


def compute(s):
    numbers = [int(n) for n in s.splitlines()]
    invalid = get_invalid(numbers, 25)
    (i, j, r) = (0, 1, [])
    while sum(r) != invalid:
        r = numbers[i:j]
        if sum(r) < invalid:
            j += 1
        elif sum(r) > invalid:
            i += 1
    return min(r) + max(r)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ("""35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""", 62),
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
