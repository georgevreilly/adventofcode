#!/usr/bin/env python3

from __future__ import annotations

DAY = 15
# https://adventofcode.com/2021/day/15

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


def parse_data(text_data: list[str]) -> list[list[int]]:
    return [[int(d) for d in line.strip()]
            for line in text_data]


def load_data(namespace) -> list[list[int]]:
    if namespace.custom:
        text_data = ["-1"]
        data = parse_data(text_data)
    else:
        text_data = read_data(namespace.input_filename)
        logging.info("%s", namespace.input_filename)
        logging.debug("%s", text_data)
        data = parse_data(text_data)
    return data


def grid_to_str(grid: list[list[int]], prefix="") -> str:
    return prefix + ("\n" + prefix).join(
        "".join([str(n) for n in row]) for row in grid) + "\n"



def explore(grid, row, col, visited, cum_risk, path):
    logging.debug(f"explore: {row=},{col=}, {visited=}, {cum_risk=}, {path=}")
    width =  5 # len(grid[0])
    height =  5 # len(grid)
    visited = visited | {(row, col)}
    if row == height - 1 and col == width - 1:
        print(f"\tEnd: returning {cum_risk=} {path=}")
        return cum_risk, path

    risk_paths = []
    choices = []
    for r, c in [(0, +1), (+1, 0), (0, -1), (-1, 0)]:
        r2 = row + r
        c2 = col + c
        if (r2, c2) not in visited:
            if 0 <= r2 < height and 0 <= c2 < width:
                choices.append((grid[r2][c2], r2, c2))
    choices.sort()
    for cell_risk, r2, c2 in choices:
        risk, new_path = explore(grid,
                        r2, c2,
                        visited,
                        cum_risk + cell_risk,
                        path + [(r2, c2)])
        if risk is not None:
            risk_paths.append((risk, new_path))
    if len(risk_paths) == 0:
        return None, None
    print(f"\t{row=},{col=}, #{len(risk_paths)} {risk_paths=}")
    risk, new_path = sorted(risk_paths)[0]
    logging.debug(f"{row=},{col=}, chose {risk=} {new_path=}")
    return risk, new_path


def distance_matrix(grid):
    width = len(grid[0])
    height = len(grid)
    d = [[0 for _ in range(width)] for _ in range(height)]
    for r in range(1, height):
        d[r][0] = d[r-1][0] + grid[r][0]
    for c in range(1, width):
        d[0][c] = d[0][c-1] + grid[0][c]
    for r in range(1, height):
        for c in range(1, width):
            d[r][c] = grid[r][c] + min(d[r-1][c], d[r][c-1])
    for row in d:
        logging.debug(",".join(f"{n:2}" for n in row))
    return d[-1][-1]


def compute1(grid: list[list[int]]) -> int:
    return distance_matrix(grid)
    # total, path = explore(grid, 0, 0, set(), 0, [(0, 0)])
    # print(f"\ncompute1: {total=} {path=}")
    # return total


def multiply_tile(tile: list[list[int]], mult: int) -> int:
    succ = [n + 1 for n in range(9)] + [1]
    tile_width = len(tile[0])
    tile_height = len(tile)
    width, height = mult * tile_width, mult * tile_height    
    grid = [[0 for _ in range(width)] for _ in range(height)]

    for gr in range(mult):
        for gc in range(mult):
            for sr in range(tile_height):
                dr = gr * tile_height + sr
                for sc in range(tile_width):
                    dc = gc * tile_width + sc
                    risk = tile[sr][sc]
                    assert 1 <= risk <= 9
                    for _ in range(gr + gc):
                        risk = succ[risk]
                        assert 1 <= risk <= 9
                    grid[dr][dc] = risk
                    assert gr + gc == 0 or risk != tile[sr][sc]


def compute2(tile: list[list[int]]) -> int:
    grid = multiply_tile(tile, 5)
    # Need to use A* for a correct solution
    return distance_matrix(grid)


def main():
    namespace = parse_args()
    result1 = compute1(load_data(namespace))
    print(f"{result1=}")
    result2 = compute2(load_data(namespace))
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
