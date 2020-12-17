import argparse
import re

import pytest
from support import timing
import math


def get_valid_tickets(nearby_tickets, rules):
    invalid_tickets = []
    for ticket in nearby_tickets:
        for idx, n in enumerate(ticket):
            i_n = int(n)
            if all([not int(l1) <= i_n <= int(u1) and not int(l2) <= i_n <= int(u2) for (_, l1, u1, l2, u2) in rules]):
                invalid_tickets.append(ticket)
    return [t for t in nearby_tickets if invalid_tickets.count(t) == 0]


def compute(s):
    (rules_raw, my_ticket_raw, nearby_tickets_raw) = s.split("\n\n")
    rules = [re.match("(.*): (\\d+)-(\\d+) or (\\d+)-(\\d+)", rule).groups() for rule in rules_raw.splitlines()]
    nearby_tickets = [ticket.split(",") for ticket in nearby_tickets_raw.splitlines()[1:]]
    my_ticket = [int(n) for n in my_ticket_raw.splitlines()[1].split(",")]
    valid_tickets = get_valid_tickets(nearby_tickets, rules)

    field_count = len(my_ticket)
    ticket_columns = {i: [int(n[i]) for n in valid_tickets] for i in range(field_count)}
    matches = [list() for _ in range(0, field_count)]

    for i, numbers in ticket_columns.items():
        for ri, r in enumerate(rules):
            (name, l1, u1, l2, u2) = r
            if all([(int(l1) <= t <= int(u1)) or (int(l2) <= t <= int(u2)) for t in numbers]):
                matches[i].append(name)

    (ticket_fields, field_order) = [], []
    for match in sorted(matches, key=len):
        field_order.append(matches.index(match))
        for m in match:
            if m not in ticket_fields:
                ticket_fields.append(m)

    departure_idx = [v for k, v in enumerate(field_order) if "departure" in ticket_fields[k]]
    return math.prod([my_ticket[i] for i in departure_idx])


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ("""class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9""", 1),
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
