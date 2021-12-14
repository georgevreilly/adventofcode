#!/usr/bin/env python3

# https://www.reddit.com/r/adventofcode/comments/rfzq6f/2021_day_14_solutions/hohimq4/
from collections import defaultdict

polymer, pairs = open("day14input.txt").read().split('\n\n')

pairs = dict(line.split(' -> ') for line in pairs.splitlines())

def polymer_counts(polymer):
    elem_count = defaultdict(int)
    pair_count = defaultdict(int)

    for i in range(len(polymer) - 1):
        elem_count[polymer[i]] += 1
        pair_count[polymer[i:i+2]] += 1
    elem_count[polymer[-1]] += 1

    return elem_count, pair_count

def insert_pairs():
    for pair, count in pair_count.copy().items():
        pair_count[pair] -= count
        add = pairs[pair]
        elem_count[add] += count
        pair_count[pair[0] + add] += count
        pair_count[add + pair[1]] += count

elem_count, pair_count = polymer_counts(polymer)
print(f"{pairs=}")
print(f"{elem_count=}")
print(f"{pair_count=}")

for i in range(40):
    insert_pairs()
    print(f"\n{i+1}: {elem_count=}")
    print(f"{i+1}: {pair_count=}")

print(max(elem_count.values()) - min(elem_count.values()))
