import argparse

import pytest
from support import timing
import re
from collections import Counter


def compute(s):
    allergens = {}
    appearances = Counter()
    all_ingredients = {*()}
    allergic = {*()}
    for line in s.splitlines():
        (g1, g2) = re.search(r"([a-z ]*) .contains ([a-z, ]*).", line).groups()
        ingredients = set(g1.split())
        appearances.update(ingredients)
        all_ingredients.update(ingredients)
        for a in set(g2.split(", ")):
            if a not in allergens:
                allergens[a] = []
            allergens[a].append(ingredients)

    for a, ins in allergens.items():
        dis = set(ins[0])
        for i in ins:
            dis &= i
        [allergic.add(ci) for ci in dis]

    total = 0
    for u in all_ingredients - allergic:
        total += appearances[u]
    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
("""mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""", 5),
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
