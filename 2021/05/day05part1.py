#!/usr/bin/env python3

from __future__ import annotations

DAY = 5
# https://adventofcode.com/2021/day/5#part1

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
        "--verbose", "-v", action="store_true",
        help="More verbose logging")
    namespace = parser.parse_args()

    namespace.input_filename = REAL_DATA if namespace.real else TEST_DATA
    log_level = logging.DEBUG if namespace.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    return namespace


def read_data(input_filename: str):
    with open(os.path.join(os.path.dirname(__file__), input_filename)) as f:
        return [l.strip() for l in f]


def parse_data(text_data: list[str]) -> list:
    result = []
    for text_line in text_data:
        pieces = [part.split(",") for part in text_line.split("->")]
        coord_pair = []
        for pair in pieces:
            coord_pair.append(tuple(int(n.strip()) for n in pair))
        result.append(coord_pair)
    return result


def hydrothermal_vents(lines, width: int) -> int:
    grid = [[0 for _ in range(width)] for _ in range(width)]
    for (x1, y1), (x2, y2) in lines:
        # print("---")
        # for r, row in enumerate(grid):
        #     print(r, row)
        assert 0 <= x1 < width
        assert 0 <= y1 < width
        assert 0 <= x2 < width
        assert 0 <= y2 < width

        count = 0
        x_dist = x2 - x1
        y_dist = y2 - y1
        x_step = +1 if x_dist > 0 else -1 if x_dist < 0 else 0
        y_step = +1 if y_dist > 0 else -1 if y_dist < 0 else 0
        if x_dist == 0:
            count = abs(y_dist) + 1
        elif y_dist == 0:
            count = abs(x_dist) + 1
        elif abs(x_dist) == abs(y_dist):
            count = abs(x_dist) + 1

        for i in range(count):
            grid[y1 + i * y_step][x1 + i * x_step] += 1

    # print("=====\nfinished")
    total = 0
    for r, row in enumerate(grid):
        count = sum(1 if c>=2 else 0 for c in row)
        # print(r, ": ", count,  "".join([str(c) if c else '.' for c in row]))
        total += count
    return total


def main():
    namespace = parse_args()
    text_data = read_data(namespace.input_filename)
    logging.info("%s", namespace.input_filename)
    logging.debug("%s", text_data)
    lines = parse_data(text_data)
    logging.debug("\nlines: %s", lines)
    overlapped_lines = hydrothermal_vents(
        lines, 1000 if namespace.real else 10)
    print(f"Overlap: {overlapped_lines}")


if __name__ == "__main__":
    raise SystemExit(main())
