import argparse

import pytest
from support import timing
import re


def compute(s):
    (rules_raw, my_ticket_raw, nearby_tickets_raw) = s.split("\n\n")
    rules = [re.match(".*: (\\d+)-(\\d+) or (\\d+)-(\\d+)", rule).groups() for rule in rules_raw.splitlines()]
    nearby_tickets = [ticket.split(",") for ticket in nearby_tickets_raw.splitlines()[1:]]
    error_rate = 0
    for ticket in nearby_tickets:
        for idx, n in enumerate(ticket):
            i_n = int(n)
            if all([not int(l1) <= i_n <= int(u1) and not int(l2) <= i_n <= int(u2) for (l1, u1, l2, u2) in rules]):
                error_rate += i_n
    return error_rate


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ("""class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12""", 71),
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
