import argparse
import re

import pytest
from support import timing


def compute(s):
    (rules_raw, messages_raw) = s.split("\n\n")
    messages = [msg for msg in messages_raw.splitlines()]
    rules = {
        key: rr.strip("\"") for (key, rr) in
        [re.match("(\\d+): (.*)", r).groups() for r in rules_raw.splitlines()]
    }

    def build_re(k):
        if k == '|':
            return k

        rule = rules[k]
        if rule in ["a", "b"]:
            return rule
        return f'({"".join(build_re(part) for part in rule.split())})'

    return sum(bool(re.compile(build_re("0")).fullmatch(m)) for m in messages)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
("""0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb""", 2),
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
