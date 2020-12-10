import argparse

import pytest
from support import timing


def compute(s):
    numbers = [int(line) for line in s.splitlines()]
    sn = sorted(numbers)
    sn.insert(0, 0)
    sn.append(sn[-1] + 3)
    (d1, d3) = (0, 0)
    for i in range(0, len(sn) - 1):
        diff = sn[i + 1] - sn[i]
        if diff == 3:
            d3 += 1
        elif diff == 1:
            d1 += 1
    return d1 * d3


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ("""16
10
15
5
1
11
7
19
6
12
4""", 7 * 5),
        ("""28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""", 22 * 10),
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
