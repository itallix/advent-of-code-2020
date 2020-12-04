import argparse
import re

import pytest
from support import timing


class Rule:
    def __init__(self, regex, mn=None, mx=None):
        self.regex = regex
        self.min = mn
        self.max = mx

    def is_valid(self, test_value):
        match = re.match(self.regex, test_value)
        if match:
            if not match.groups():
                return True
            return self.min <= int(match.group(1)) <= self.max

        return False


required = {
    "byr": [Rule("^(\\d{4})$", 1920, 2002)],
    "iyr": [Rule("^(\\d{4})$", 2010, 2020)],
    "eyr": [Rule("^(\\d{4})$", 2020, 2030)],
    "hgt": [Rule("^(\\d{3})cm$", 150, 193), Rule("^(\\d{2})in$", 59, 76)],
    "hcl": [Rule("^#[0-9a-f]{6}$")],
    "ecl": [Rule("^amb|blu|brn|gry|grn|hzl|oth$")],
    "pid": [Rule("^\\d{9}$")]
}


def compute(s):
    total = 0

    for line in s.split("\n\n"):
        passport = dict()
        for f in line.split():
            pair = f.split(":")
            passport[pair[0]] = pair[1]

        if passport.keys() - {"cid"} == required.keys():
            is_valid = True
            for key in passport.keys() - {"cid"}:
                rules = required.get(key)
                value = passport.get(key)
                is_valid = is_valid and True in [rule.is_valid(value) for rule in rules]
                if not is_valid:
                    break
            if is_valid:
                total += 1
    return total


def fcompute(s):
    # bonus implementation with for comprehensions
    passports = [{k: v for k, v in [f.split(":") for f in pdata.split()] if k != "cid"} for pdata in s.split("\n\n")]

    return len(list(filter(lambda x: x is True, [all([True in [rule.is_valid(passport.get(key))
                                                               for rule in required.get(key)]
                                                      for key in passport.keys()])
                                                 for passport in passports if passport.keys() == required.keys()])))


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ("""pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719\n\n""", 4),
            ("""eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007\n\n""", 0)
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
