#!/usr/bin/env python3

from __future__ import annotations

DAY = 9
# https://adventofcode.com/2021/day/9

import argparse
import logging
import os


TEST_DATA = f"day{DAY:02}test_input.txt"
REAL_DATA = f"day{DAY:02}input.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"AdventOfCode: Day {DAY}")
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

    parser.add_argument(
        "--custom", "-C", action="store_true",
        help="Use custom data")
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="More verbose logging")
    namespace = parser.parse_args()

    namespace.input_filename = REAL_DATA if namespace.real else TEST_DATA
    log_level = logging.DEBUG if namespace.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    return namespace


def read_data(input_filename: str):
    with open(os.path.join(os.path.dirname(__file__), input_filename)) as f:
        return f.readlines()


def parse_data(text_data: list[str]) -> list[str]:
    results = []
    for line in text_data:
        results.append([int(d) for d in line.strip()])
    return results


def lowest_points(data) -> int:
    width = len(data[0])
    height = len(data)
    low_points = []
    for r, row in enumerate(data):
        for c, loc in enumerate(row):
            lowest = True
            for dx, dy in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                if 0 <= c + dx < width and 0 <= r + dy < height:
                    if loc >= data[r + dy][c + dx]:
                        lowest = False
                        break
            if lowest:
                low_points.append((r, c))
    return low_points


def compute1(data) -> int:
    return sum(1+data[r][c] for r, c in lowest_points(data))


def basin_neighbors(data, r, c, seen):
    if (r, c) in seen:
        return
    elif data[r][c] == 9:
        return
    seen.add((r, c))
    width = len(data[0])
    height = len(data)
    for dx, dy in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
        if 0 <= c + dx < width and 0 <= r + dy < height:
            basin_neighbors(data, r+dy, c+dx, seen)


def compute2(data) -> int:
    basins = []
    for r, c in lowest_points(data):
        seen = set()
        basin_neighbors(data, r, c, seen)
        count = len(seen)
        basins.append(count)
    largest = sorted(basins)[-3:]
    n = 1
    for l in largest:
        n *= l
    return n


def main():
    namespace = parse_args()
    if namespace.custom:
       data = parse_data(None)
    else:
        text_data = read_data(namespace.input_filename)
        logging.info("%s", namespace.input_filename)
        logging.debug("%s", text_data)
        data = parse_data(text_data)
    logging.debug("\ndata: %s", data)
    result1 = compute1(data)
    print(f"{result1=}")
    result2 = compute2(data)
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
