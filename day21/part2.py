import argparse

import pytest
from support import timing
import re
from collections import Counter


def compute(s):
    allergens = {}
    appearances = Counter()
    all_ingredients = {*()}
    for line in s.splitlines():
        (g1, g2) = re.search(r"([a-z ]*) .contains ([a-z, ]*).", line).groups()
        ingredients = set(g1.split())
        appearances.update(ingredients)
        all_ingredients.update(ingredients)
        for a in set(g2.split(", ")):
            if a not in allergens:
                allergens[a] = []
            allergens[a].append(ingredients)

    allergic = {}
    for a, ins in allergens.items():
        dis = set(ins[0])
        for i in ins:
            dis &= i
        for ci in dis:
            if a not in allergic:
                allergic[a] = set()
            allergic[a].add(ci)

    detected = set([next(iter(i)) for i in allergic.values() if len(i) == 1])
    while any(len(i) != 1 for i in allergic.values()):
        for k in sorted(allergic):
            values = allergic[k]
            if len(values) > 1:
                values -= detected
                if len(values) == 1:
                    detected.add(next(iter(values)))

    return ",".join([next(iter(allergic[k])) for k in sorted(allergic)])


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
("""mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""", "mxmxvkd,sqjhc,fvjkl"),
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
