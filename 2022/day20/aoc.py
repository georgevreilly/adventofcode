#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 20
# https://adventofcode.com/2022/day/20

import argparse
import functools
import itertools
import json
import logging
import math
import operator
import os
import pprint


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
        text_data = "noop\naddx 3\naddx -5"
        data = parse_data(text_data)
    else:
        text_data = read_data(namespace.input_filename)
        logging.info("%s", namespace.input_filename)
        logging.debug("%s", text_data)
        data = parse_data(text_data)
        logging.debug("%s", data)
    return data


def parse_data(text_data: str) -> list[str]:
    return [int(n) for n in text_data.strip().split("\n")]


def modulo(x: int, n: int) -> int:
    r = (x + n - 1) % (n - 1)
    assert 0 <= r < n - 1
    return r


def compute1(records: list[int]) -> int:
    mixed = records[:]
    n = len(records)
    print(f"{n=} {mixed=}")
    for r in records:
        assert -n < r < n
        i = mixed.index(r)
        j = modulo(i + r, n)
        if r > 0:
            for k in range(r):
                mixed[modulo(i + k, n)] = mixed[modulo(i + k + 1, n)]
            mixed[modulo(i + r, n)] = r
        else:
            for k in range(-r):
                mixed[modulo(i + k, n)] = mixed[modulo(i + k + 1, n)]
            mixed[modulo(i - r, n)] = r
        print(f"{r=} {i=} {j=} {mixed=}\n")
    return 0


def compute2(records: list[int]) -> int:
    return 0


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
