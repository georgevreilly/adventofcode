#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 3
# https://adventofcode.com/2022/day/3

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
    return [l.strip() for l in text_data]


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


def priority(c):
    if c >= "a":
        return ord(c) - ord("a") + 1
    else:
        return ord(c) - ord("A") + 26 + 1


def compute1(rucksacks: list[Any]) -> int:
    compartments = [(set(l[:len(l)//2]), set(l[len(l)//2:])) for l in rucksacks]
    total = 0
    common = [a & b for a, b in compartments]
    print(f"{common=}")
    priorities = [sum(priority(c) for c in s) for s in common]
    print(f"{priorities=}")
    total = sum(priorities)
    return total


def compute2(rucksacks: list[Any]) -> int:
    total = 0
    groups = [rucksacks[r:r+3] for r in range(0, len(rucksacks), 3)]
    print(f"{groups=}")
    common = [set(a) & set(b) & set(c) for a, b, c in groups]
    print(f"{common=}")
    priorities = [sum(priority(c) for c in s) for s in common]
    print(f"{priorities=}")
    total = sum(priorities)
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
