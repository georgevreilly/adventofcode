#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 8
# https://adventofcode.com/2022/day/8

import argparse
import json
import logging
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


def grid_to_str(grid: list[list[int]], prefix="", separator="") -> str:
    return prefix + ("\n" + prefix).join(
        separator.join([str(n) for n in row]) for row in grid) + "\n"


def read_data(input_filename: str):
    with open(os.path.join(os.path.dirname(__file__), input_filename)) as f:
        return f.read()


def load_data(namespace) -> list[str]:
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


def parse_data(text_data: str) -> list[list[int]]:
    lines = [s.strip() for s in text_data.strip().split('\n')]
    return [[int(n) for n in line] for line in lines]


def neighbors(grid: list[list[int]], row: int, col: int) -> list[tuple[int, int]]:
    width, height = len(grid[0]), len(grid)
    result = []
    for r, c in ((-1, -1), (-1, +1), (+1, -1), (+1, +1)):
        r2, c2 = row + r, col + c
        if 0 <= r2 < height and 0 <= c2 < width:
            result.append((r2, c2))


def is_visible(grid, row, col) -> int:
    width, height = len(grid[0]), len(grid)
    cell = grid[row][col]

    for r in range(row-1, -1, -1):
        if grid[r][col] >= cell:
            break
    else:
        return 1
    for r in range(row+1, height, +1):
        if grid[r][col] >= cell:
            break
    else:
        return 1
    for c in range(col-1, -1, -1):
        if grid[row][c] >= cell:
            break
    else:
        return 1
    for c in range(col+1, width, +1):
        if grid[row][c] >= cell:
            break
    else:
        return 1
    return 0



def compute1(grid: list[list[int]]) -> int:
    width, height = len(grid[0]), len(grid)

    logging.debug(grid_to_str(grid))
    visible = [[0 for _ in range(width)] for _ in range(height)]

    for row in range(0, height):
        for col in range(0, width):
            visible[row][col] = is_visible(grid, row, col)

    logging.debug(grid_to_str(visible))
    return sum([sum(row) for row in visible])


def viewing_distance(grid, row, col) -> int:
    width, height = len(grid[0]), len(grid)
    cell = grid[row][col]

    for r in range(row-1, -1, -1):
        if grid[r][col] >= cell:
            left = row -r
            break
    else:
        left = row
    for r in range(row+1, height, +1):
        if grid[r][col] >= cell:
            right = r - row
            break
    else:
        right = height - 1 - row
    for c in range(col-1, -1, -1):
        if grid[row][c] >= cell:
            up = col - c
            break
    else:
        up = col
    for c in range(col+1, width, +1):
        if grid[row][c] >= cell:
            down = c - col
            break
    else:
        down = width - 1 - col
    dist = left * right * up * down
    logging.debug(f"{row=} {col=} {dist=} {left=} {right=} {up=} {down=}")
    return dist


def compute2(grid: list[list[int]]) -> int:
    width, height = len(grid[0]), len(grid)

    distance = [[0 for _ in range(width)] for _ in range(height)]

    for row in range(0, height):
        for col in range(0, width):
            distance[row][col] = viewing_distance(grid, row, col)

    logging.debug(grid_to_str(distance, separator=", "))
    return max([max(row) for row in distance])


def main():
    namespace = parse_args()
    payload = load_data(namespace)
    result1 = compute1(payload)
    print(f"{result1=}")
    payload = load_data(namespace)
    result2 = compute2(payload)
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
