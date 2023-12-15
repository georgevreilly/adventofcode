#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2023
DAY = 1
# https://adventofcode.com/2023/day/1

import argparse
import json
import logging
import os
import pprint
import re


TEST_DATA = "test_input.txt"
TEST_DATA2 = "test_input2.txt"
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
        "--file", "-f", dest="input_filename",
        help="Use file")
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="More verbose logging")
    namespace = parser.parse_args()

    if not namespace.input_filename:
        namespace.input_filename = REAL_DATA if namespace.real else TEST_DATA
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


def load_data(namespace, suffix: str = "") -> list[str]:
    if suffix:
        filename = REAL_DATA if namespace.real else TEST_DATA2
    else:
        filename = namespace.input_filename 
    text_data = read_data(filename)
    logging.info("%s", filename)
    logging.debug("%s", text_data)
    data = parse_data(text_data)
    logging.debug("%s", data)
    return data


def parse_data(text_data: str) -> list[list[int]]:
    return text_data.strip().split('\n')


def compute1(lines: list[str]) -> int:
    total = 0
    for s in lines:
        print(f"{s=!r}")
        l = next(i for i in range(len(s)) if s[i].isdigit())
        r = next(i for i in range(len(s)-1, -1, -1) if s[i].isdigit())
        total += int(s[l] + s[r])
    return total


NUM_RE = re.compile(r"(zero|one|two|three|four|five|six|seven|eight|nine|0|1|2|3|4|5|6|7|8|9)")
DIGITS = dict(
    zero="0",
    one="1",
    two="2",
    three="3",
    four="4",
    five="5",
    six="6",
    seven="7",
    eight="8",
    nine="9",
)

def tokenize(s: str):
    tokens = NUM_RE.findall(s)
    return [DIGITS.get(tok, tok) for tok in tokens]


def compute2(lines: list[str]) -> int:
    total = 0
    for s in lines:
        numbers = tokenize(s)
        logging.info("%s -> %r", s, numbers)
        total += int(numbers[0] + numbers[-1])
    return total


def main():
    namespace = parse_args()
    payload = load_data(namespace)
    result1 = compute1(payload)
    print(f"{result1=}")
    payload = load_data(namespace, "2")
    result2 = compute2(payload)
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
