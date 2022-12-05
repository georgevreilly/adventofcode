#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 4
# https://adventofcode.com/2022/day/4

import argparse
import logging
import os


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

    namespace.input_filename = REAL_DATA if namespace.real else TEST_DATA
    log_level = logging.DEBUG if namespace.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    return namespace


def read_data(input_filename: str):
    with open(os.path.join(os.path.dirname(__file__), input_filename)) as f:
        return f.readlines()


def parse_data(text_data: list[str]) -> list[list[str]]:
    pairs = []
    for line in text_data:
        items = []
        for elves in line.strip().split(","):
            ids = [ids for ids in elves.split("-", 2)]
            items.append(set(range(int(ids[0]), int(ids[1])+1)))
        pairs.append(items)
    return pairs


def load_data(namespace) -> list[list[int]]:
    if namespace.custom:
        text_data = ["-1"]
        data = parse_data(text_data)
    else:
        text_data = read_data(namespace.input_filename)
        logging.info("%s", namespace.input_filename)
        logging.debug("%s", text_data)
        data = parse_data(text_data)
        logging.debug("%s", data)
    return data


def grid_to_str(grid: list[list[int]], prefix="") -> str:
    return prefix + ("\n" + prefix).join(
        "".join([str(n) for n in row]) for row in grid) + "\n"


def compute1(pairs: list[Any]) -> int:
    return sum(1 if x.issubset(y) or y.issubset(x) else 0 for x, y in pairs)
    total = 0
    for x, y in pairs:
        if x.issubset(y) or y.issubset(x):
            total +=1
    return total


def compute2(pairs: list[Any]) -> int:
    return sum(1 if x & y else 0 for x, y in pairs)
    total = 0
    for x, y in pairs:
        if x & y:
            total +=1
    return total


def main():
    namespace = parse_args()
    payload = load_data(namespace)
    result1 = compute1(payload)
    print(f"{result1=}")
    result2 = compute2(payload)
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
