import argparse

import pytest
from support import timing


def compute(s):
    schedule = [x for x in s.splitlines()[1].split(",")]
    bus_ids = [int(x) for x in schedule if x != "x"]
    (step, t) = bus_ids[0], 0
    for b in bus_ids[1:]:
        while (t + schedule.index(str(b))) % b:
            t += step
        step *= b
    return t


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ("""123
7,13,x,x,59,x,31,19""", 1068781),
        ("""123
17,x,13,19""", 3417),
        ("""234
1789,37,47,1889""", 1202161486),
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
