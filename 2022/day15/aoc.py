#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 15
# https://adventofcode.com/2022/day/15

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


def at_xy(text, prefix):
    assert text.startswith(prefix), f"{text=!r} {prefix=!r}"
    xy = text[len(prefix):].split(", ")
    return tuple(int(ordinate.split("=")[-1]) for ordinate in xy)


def parse_data(text_data: str) -> list[str]:
    data = []
    for line in text_data.strip().split("\n"):
        sensor, beacon = line.split(": ")
        sx, sy = at_xy(sensor, "Sensor at ")
        bx, by = at_xy(beacon, "closest beacon is at ")
        data.append([(sx, sy), (bx, by)])
    return data


def manhattan_dist(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


def compute1(records: list, row) -> int:
    impossible = set()
    row_data = set()
    for (sx, sy), (bx, by) in records:
        dx, dy = abs(bx - sx), abs(by - sy)
        dist = dx + dy
        included = sy - dist <= row <= sy + dist
        # print(f"S={sx},{sy} B={bx},{by} {dx=} {dy=} {dist=} {included=}")
        for v in range(0, dist+1):
            if sy - v == row or sy + v == row:
                h = dist - v
                for x in range(v - dist, dist - v + 1):
                    row_data.add(sx + x)
    row_data = sorted(row_data)
    logging.debug(f"{row_data=}")

    return row_data[-1] - row_data[0]


BEACON_MAX = 4_000_000

def compute2(records: list, biggest) -> int:
    rx = ry = 0
    grid = set()
    for (sx, sy), (bx, by) in records:
        dx, dy = abs(bx - sx), abs(by - sy)
        dist = dx + dy
        for v in range(0, dist+1):
            if sy - v == row or sy + v == row:
                h = dist - v
                for x in range(v - dist, dist - v + 1):
                    row_data.add(sx + x)

    return rx * 4_000_000 + ry


def main():
    namespace = parse_args()
    payload = load_data(namespace)
    # logging.debug(json.dumps(payload, indent=4))
    result1 = compute1(payload, row=2_000_000 if namespace.real else 10)
    print(f"{result1=}")
    payload = load_data(namespace)
    result2 = compute2(payload, biggest=4_000_000 if namespace.real else 20)
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
