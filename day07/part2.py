import argparse
import re

import networkx as nx
import pytest
from support import timing


def compute(s):
    bags = nx.DiGraph()
    my_bag = "shiny gold"
    for rule in s.splitlines():
        (outer, inner) = rule.split("contain")
        matches = re.findall("(\\d) ([a-z]* [a-z]*) bag", inner)
        for m in matches:
            bags.add_edge(re.match("([a-z]* [a-z]*) bag", outer).group(1), m[1], weight=m[0])

    def calc(node, acc=0):
        for edge in nx.edges(bags, node):
            (e0, e1) = edge
            edge_data = bags.get_edge_data(e0, e1)
            if edge_data:
                weight = int(edge_data['weight'])
                acc += weight + weight * calc(e1)
        return acc

    return calc(my_bag)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
(
  """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""", 32
),
("""shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.""", 126)
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
