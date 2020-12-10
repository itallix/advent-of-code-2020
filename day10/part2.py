import argparse

import pytest
from support import timing


def compute(s):
    numbers = [int(line) for line in s.splitlines()]
    sn = sorted(numbers)
    sn.append(sn[-1] + 3)
    jolts = [1, 2, 3]
    paths = {0: 1}
    for num in sn:
        paths[num] = sum([paths.get(num - i, 0) for i in jolts])

    return paths[sn[-1]]


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
4""", 8),
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
3""", 19208),
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
