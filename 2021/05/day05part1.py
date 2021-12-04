#!/usr/bin/env python3

from __future__ import annotations

DAY = 5
# https://adventofcode.com/2021/day/5#part1

import argparse
import logging
import os


def parse_args() -> argparse.Namespace:
    TEST_DATA = f"day{DAY:02}test_input.txt"
    REAL_DATA = f"day{DAY:02}input.txt"
    parser = argparse.ArgumentParser(
        description=f"AdventOfCode: Day {DAY}")
    parser.set_defaults(
        input_filename=TEST_DATA,
        verbose=False,
    )
    parser.add_argument(
        "--test", "-t", dest="input_filename",
        const=TEST_DATA, action="store_const",
        help="Use %(const)r as input_filename")
    parser.add_argument(
        "--real", "-r", dest="input_filename",
        const=REAL_DATA, action="store_const",
        help="Use %(const)r as input_filename")
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="More verbose logging")
    namespace = parser.parse_args()

    log_level = logging.DEBUG if namespace.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    return namespace


def read_data(input_filename: str):
    with open(os.path.join(os.path.dirname(__file__), input_filename)) as f:
        return [l.strip() for l in f]
    

def main():
    namespace = parse_args()
    text_data = read_data(namespace.input_filename)
    logging.debug("%s: %s", namespace.input_filename, text_data)


if __name__ == "__main__":
    raise SystemExit(main())
