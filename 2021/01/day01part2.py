#!/usr/bin/env python3

# https://adventofcode.com/2021/day/1#part2

from __future__ import annotations

import os


def sliding_window_measurement(depths: list[int], window_size: int):
    count = 0
    prev = depths[0:window_size]
    for i in range(0, len(depths)-window_size+1):
        increased = decreased = same = 0
        curr = depths[i:i+window_size]
        if sum(curr) > sum(prev):
            increased = 1
            count += 1
        elif sum(curr) < sum(prev):
            decreased = 1
        else:
            same = 1
        # print(f"{chr(ord('A')+i)}: prev={prev!r}={sum(prev)}, curr={curr!r}={sum(curr)}, incr={increased}, decr={decreased}, same={same}")
        prev = curr
    return count


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

print("initial", sliding_window_measurement(initial_depths, 3))

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    input_depths = [int(l) for l in f]

print("input", sliding_window_measurement(input_depths, 3))
