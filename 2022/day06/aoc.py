#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 6
# https://adventofcode.com/2022/day/6

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


def grid_to_str(grid: list[list[int]], prefix="") -> str:
    return prefix + ("\n" + prefix).join(
        "".join([str(n) for n in row]) for row in grid) + "\n"


def read_data(input_filename: str):
    with open(os.path.join(os.path.dirname(__file__), input_filename)) as f:
        return f.read()


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


def parse_data(text_data: str) -> list[list[str]]:
    return [s.strip() for s in text_data.split('\n')]


def compute1(tx: str) -> int:
    for i in range(3, len(tx)):
        sub = tx[i-3:i+1]
        chars = set(sub)
        # print(f"{sub=}: {chars=}")
        if len(chars) == 4:
            return i + 1


def compute2(tx: str) -> int:
    for i in range(13, len(tx)):
        sub = tx[i-13:i+1]
        chars = set(sub)
        # print(f"{sub=}: {chars=}")
        if len(chars) == 14:
            return i + 1


def main():
    namespace = parse_args()
    payload = load_data(namespace)
    for tx in payload:
        result1 = compute1(tx)
        print(f"{tx=}: {result1=}")
    payload = load_data(namespace)
    for tx in payload:
        result2 = compute2(tx)
        print(f"{tx=}: {result2=}")
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
