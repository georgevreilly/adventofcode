#!/usr/bin/env python3

# https://adventofcode.com/2021/day/1#part1

from __future__ import annotations

import os


def measurement(depths: list[int]):
    increased = 0
    prev = depths[0]
    for curr in depths[1:]:
        if curr > prev:
            increased += 1
        prev = curr
    return increased


initial_depths = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]

print(measurement(initial_depths))

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    input_depths = [int(l) for l in f]

print(measurement(input_depths))
