#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 14
# https://adventofcode.com/2022/day/14

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
    paths = []
    for line in text_data.strip().split("\n"):
        path = []
        for point in line.split(" -> "):
            path.append(tuple(int(p) for p in point.split(",")))
        paths.append(path)
    return paths


def bounding_box(paths: list):
    min_x = max_x = 500
    min_y = max_y = 0
    for path in paths:
        for x, y in path:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

    return (min_x, min_y, max_x, max_y)


def step(p1, p2):
    return +1 if p1 < p2 else -1 if p1 > p2 else 0


def _range(p1, p2):
    if p1 < p2:
        return range(p1, p2+1)
    elif p1 > p2:
        return range(p1, p2-1, -1)
    else:
        assert False


ORIGIN_X, ORIGIN_Y = 500, 0


def draw_paths(paths, min_x, min_y, max_x, max_y):
    w = max_x - min_x + 1 + 2
    h = max_y - min_y + 1 + 2
    grid = [["." for _ in range(w)] for _ in range(h)]
    for x in range(w):
        grid[0][x] = grid[h-1][x] = "@"
    for y in range(h):
        grid[y][0] = grid[y][w-1] = "@"
    grid[ORIGIN_Y - min_y + 1][ORIGIN_X - min_x + 1] = "+"
    for path in paths:
        sx, sy = path[0]
        for tx, ty in path[1:]:
            # logging.debug(f"{sx=} {sy=} {tx=} {ty=}")
            if sx != tx:
                assert sy == ty
                for x in _range(sx, tx):
                    # logging.debug(f"{sx=} {tx=} {x=} {x - min_x} {w=}")
                    grid[sy - min_y + 1][x - min_x + 1] = "#"
            else:
                for y in _range(sy, ty):
                    # logging.debug(f"{sy=} {ty=} {y=} {y - min_y} {h=}")
                    grid[y - min_y + 1][sx - min_x + 1] = "#"
            sx, sy = tx, ty
    return grid


def compute1(paths: list) -> int:
    min_x, min_y, max_x, max_y = bounding_box(paths)
    w = max_x - min_x + 1 + 2
    h = max_y - min_y + 1 + 2
    logging.debug(f"{min_x=}, {min_y=}, {max_x=}, {max_y=}")
    grid = draw_paths(paths, min_x, min_y, max_x, max_y)
    print(grid_to_str(grid))

    more = True
    sand = 1
    while more:
        x, y = ORIGIN_X - min_x, ORIGIN_Y - min_y
        grid[y + 1][x + 1] = "o"
        while more:
            assert y + 1 < h
            y1 = y + 1 + 1
            for dx in (0, -1, +1):
                x1 = x + 1 + dx
                if grid[y1][x1] == "@":
                    more = False
                    break
                if grid[y1][x1] == ".":
                    grid[y + 1][x + 1] = "." if y else "+"
                    x, y = x + dx, y + 1
                    grid[y + 1][x + 1] = "o"
                    break
            else:
                break
        print(f"{sand=} {x=} {y=} {more=}")
        print(grid_to_str(grid))
        if more:
            sand += 1
    return sand


def compute2(paths: list) -> int:
    return 0


def main():
    namespace = parse_args()
    payload = load_data(namespace)
    # logging.debug(json.dumps(payload, indent=4))
    result1 = compute1(payload)
    print(f"{result1=}")
    # payload = load_data(namespace)
    # result2 = compute2(payload)
    # print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
