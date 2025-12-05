#!/usr/bin/env python3

"""Advent of Code: 2025, day 1
https://adventofcode.com/2025/day/1
"""

from __future__ import annotations

import argparse
import json
import logging
import os

YEAR = 2025
DAY = 1

TEST_DATA = "test_input.txt"
REAL_DATA = "input.txt"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments"""
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
    """Render a grid from a list of lists of numbers"""
    return prefix + ("\n" + prefix).join(
        separator.join([str(n) for n in row]) for row in grid) + "\n"


def read_data(input_filename: str):
    """Read contents of input_filename"""
    with open(os.path.join(os.path.dirname(__file__), input_filename),
              encoding="utf-8") as f:
        return f.read()


def parse_data(text_data: str) -> list[tuple[str, int]]:
    """Parse text_data for this problem"""
    return [(s[0], int(s[1:])) for s in text_data.split("\n") if s]


def load_data(namespace) -> list[tuple[str, int]]:
    """Read and parse the data, in the format required for this problem"""
    if namespace.custom:
        text_data = "noop\naddx 3\naddx -5"
        data = parse_data(text_data)
    else:
        text_data = read_data(namespace.input_filename)
        logging.info("%s", namespace.input_filename)
        # logging.debug("read [%s]", text_data)
        data = parse_data(text_data)
        # logging.debug("parsed: [%s]", data)
    return data


def compute1(records: list[tuple[str, int]]) -> int:
    """Compute a solution to the initial, simpler problem"""
    dial = 50
    count = 0
    for lr, amount in records:
        if lr == "R":
            dial = (dial + amount) % 100
        elif lr == "L":
            dial = (dial + 100 - amount) % 100
        else:
            print(f"What {lr!r}")
        if dial == 0:
            count += 1
        logging.debug("%s", f"{lr=}, {amount=}, {dial=}, {count=}")
    return count


def compute2(records: list[tuple[str, int]]) -> int:
    """Compute a solution to the second, harder problem"""
    dial = 50
    count = 0
    click = 0
    for lr, amount in records:
        for i in range(amount - 1, -1, -1):
            if lr == "R":
                dial = (dial + 1) % 100
            elif lr == "L":
                dial = (dial + 100 - 1) % 100
            if dial == 0:
                if i == 0:
                    count += 1
                else:
                    click += 1
        logging.debug("%s", f"{lr=}, {amount=}, {dial=}, {count=}, {click=}")
    return count + click


def main():
    """Main"""
    namespace = parse_args()
    payload = load_data(namespace)
    logging.debug("%s", json.dumps(payload, indent=4))
    result1 = compute1(payload)
    print(f"{result1=}")

    payload = load_data(namespace)
    result2 = compute2(payload)
    print(f"{result2=}")


if __name__ == "__main__":
    main()
