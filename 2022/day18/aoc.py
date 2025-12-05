#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 18
# https://adventofcode.com/2022/day/18

import argparse
import functools
import itertools
import json
import logging
import math
import operator
import os
import pprint

from collections import defaultdict


TEST_DATA = "test_input.txt"
REAL_DATA = "input.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"AdventOfCode: {YEAR} Day {DAY}")
    parser.set_defaults(
        input_filename=None,
        real=True,
        verbose=False,
        custom=False,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--test", "-t", dest="real", action="store_false",
        help=f"Use {TEST_DATA!r} as input_filename")
    group.add_argument(
        "--real", "-r", dest="real", action="store_true",
        help="Use {REAL_DATA!r} as input_filename")
    group.add_argument(
        "--file", "-f", dest="input_filename",
        help="Use file")

    parser.add_argument(
        "--steps", "-s", type=int,
        help="Number of steps")
    parser.add_argument(
        "--custom", "-C", action="store_true",
        help="Use custom data")
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="More verbose logging")
    namespace = parser.parse_args()

    if not namespace.input_filename:
        namespace.input_filename = REAL_DATA if namespace.real else TEST_DATA
    log_level = logging.DEBUG if namespace.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    return namespace


def grid_to_str(grid: list[list[int]], prefix="", separator="") -> str:
    return prefix + ("\n" + prefix).join(
        separator.join([str(n) for n in row]) for row in grid) + "\n"


def read_data(input_filename: str):
    with open(os.path.join(os.path.dirname(__file__), input_filename)) as f:
        return f.read()


def load_data(namespace) -> list[str]:
    if namespace.custom:
        text_data = "1,1,1\n2,1,1\n"
        data = parse_data(text_data)
    else:
        text_data = read_data(namespace.input_filename)
        logging.info("%s", namespace.input_filename)
        logging.debug("%s", text_data)
        data = parse_data(text_data)
    logging.debug("%s", data)
    return data


def parse_data(text_data: str) -> list[str]:
    positions = []
    for line in text_data.strip().split("\n"):
        positions.append(tuple(int(n) for n in line.split(",")))
    return positions


def adjacent_positions(x, y, z):
    return {
        (x+dx, y+dy, z+dz) for dx, dy, dz in (
            (-1, 0, 0), (+1, 0, 0),
            (0, -1, 0), (0, +1, 0),
            (0, 0, -1), (0, 0, +1),
        )}


def compute1(positions: list[tuple]) -> int:
    exposed = 0
    for i, (x1, y1, z1) in enumerate(positions):
        neighbors = adjacent_positions(x1, y1, z1)
        logging.debug(f"({x1},{y1},{z1}) {neighbors=}")
        sides = 0
        for j, (x2, y2, z2) in enumerate(positions):
            if i == j:
                continue
            if (x2, y2, z2) in neighbors:
                sides += 1
                logging.debug(f"({x1},{y1},{z1}) ({x2},{y2},{z2})")
        exposed += 6 - sides
    return exposed


def compute2(positions: list[tuple]) -> int:
    exposed = 0
    neighbor_counts = defaultdict(int)
    for i, (x1, y1, z1) in enumerate(positions):
        neighbors = adjacent_positions(x1, y1, z1)
        for n in neighbors:
            neighbor_counts[n] = neighbor_counts[n] + 1
        logging.debug(f"({x1},{y1},{z1}) {neighbors=}")
        sides = 0
        for j, (x2, y2, z2) in enumerate(positions):
            if i == j:
                continue
            if (x2, y2, z2) in neighbors:
                sides += 1
                logging.debug(f"({x1},{y1},{z1}) ({x2},{y2},{z2})")
        exposed += 6 - sides
    interior = []
    for n, c in neighbor_counts.items():
        if c == 6 and n not in positions:
            interior.append(n)
    interior.sort()
    print(f"{interior=}")
    return exposed - 6 * len(interior)


def main():
    namespace = parse_args()
    payload = load_data(namespace)
    # logging.debug(json.dumps(payload, indent=4))
    result1 = compute1(payload)
    print(f"{result1=}")
    payload = load_data(namespace)
    result2 = compute2(payload)
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
