import argparse
import re

import pytest
from support import timing


class RegMonster:

    def __init__(self, rules, k):
        self.rules = rules
        self.reg = re.compile(self._build_re(k))

    def _build_re(self, k):
        if k == '|':
            return k

        rule = self.rules[k]
        if rule in ["a", "b"]:
            return rule
        return f'({"".join(self._build_re(part) for part in rule.split())})'

    def matches(self, idx, msg):
        c = 0
        while m := self.reg.match(msg, idx):
            c += 1
            idx = m.end()
        return c, idx


def compute(s):
    (rules_raw, messages_raw) = s.split("\n\n")
    messages = [msg for msg in messages_raw.splitlines()]
    rules = {
        key: rr.strip("\"") for (key, rr) in
        [re.match("(\\d+): (.*)", r).groups() for r in rules_raw.splitlines()]
    }

    total = 0
    (re42, re31) = RegMonster(rules, "42"), RegMonster(rules, "31")
    for message in messages:
        k = 0
        (c42, k) = re42.matches(k, message)
        (c31, k) = re31.matches(k, message)

        if 0 < c31 < c42 and k == len(message):
            total += 1

    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
("""42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba""", 12),
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
