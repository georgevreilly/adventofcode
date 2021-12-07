#!/usr/bin/env python3

from __future__ import annotations

DAY = 7
# https://adventofcode.com/2021/day/7#part1

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
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--test", "-t", dest="real", action="store_false",
        help=f"Use {TEST_DATA!r} as input_filename")
    group.add_argument(
        "--real", "-r", dest="real", action="store_true",
        help="Use {REAL_DATA!r} as input_filename")

    parser.add_argument(
        "--target", "-T", type=int,
        help="Target")
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
        return f.read().strip()


def parse_data(text_data: str) -> list[int]:
    return [int(n.strip()) for n in text_data.split(",")]


def fuel_align(crabs: list[int]) -> int:
    min_cost = 9999999999
    seen = set()
    for target in crabs:
        if target not in seen:
            cost = sum(abs(c - target) for c in crabs)
            seen.add(target)
            min_cost = min(cost, min_cost)
    return min_cost


def sum_to_n(n: int) -> int:
    return n * (n + 1) // 2


def fuel_align2(crabs: list[int]) -> int:
    min_cost = 9999999999
    positions = sorted(crabs)
    for target in range(positions[0], positions[-1]+1):
        # for c in crabs:
        #     local_cost = sum_to_n(abs(c - target))
        #     print(f"{target=} {local_cost=}")
        cost = sum(sum_to_n(abs(c - target)) for c in crabs)
        min_cost = min(cost, min_cost)
    return min_cost


def main():
    namespace = parse_args()
    text_data = read_data(namespace.input_filename)
    logging.info("%s", namespace.input_filename)
    logging.debug("%s", text_data)
    crabs = parse_data(text_data)
    logging.debug("\ncrabs: %s", crabs)
    result = fuel_align2(crabs)
    print(f"Result: {result}")


if __name__ == "__main__":
    raise SystemExit(main())
