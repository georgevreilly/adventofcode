#!/usr/bin/env python3

# https://adventofcode.com/2021/day/2#part1

from __future__ import annotations

import os


def compute_position(data):
    horiz = 0
    depth = 0
    for v, a in data:
        if v == "forward":
            horiz += a
        elif v == "down":
            depth += a
        elif v == "up":
            depth -= a
    return horiz * depth


def read_data():
    data = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        for l in f:
            v, a = l.split()
            data.append((v, int(a)))
    return data

print(compute_position([
    ("forward", 5),
    ("down", 5),
    ("forward", 8),
    ("up", 3),
    ("down", 8),
    ("forward", 2),
]))

print(compute_position(read_data()))
