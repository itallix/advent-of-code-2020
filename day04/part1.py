import argparse

import pytest


def compute(s):
    total = 0
    required = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    for line in s.split("\n\n"):
        current = set([f.split(":")[0] for f in line.split()])
        if current - {"cid"} == required:
            total += 1

    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ("""ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in""", 2),
    ),
)
def test(input_s, expected):
    assert compute(input_s) == expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
