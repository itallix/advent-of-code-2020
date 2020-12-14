import argparse

import pytest
from support import timing


def compute(s):
    (depart_time, bus_line) = s.splitlines()
    bus_ids = [int(x) for x in bus_line.split(",") if x != "x"]
    (dt, wt, target_bus) = int(depart_time), 0, None
    for bi in bus_ids:
        delta = bi - dt % bi
        if wt == 0 or delta < wt:
            (wt, target_bus) = delta, bi
    return wt * target_bus


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ("""939
7,13,x,x,59,x,31,19""", 295),
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
