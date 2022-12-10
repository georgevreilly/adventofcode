#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 9
# https://adventofcode.com/2022/day/9

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
        "--file", "-f", dest="input_filename",
        help="Use file")
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
    return [(line[0], int(line[1])) for line in [
        line.strip().split() for line in text_data.strip().split('\n')]]


def draw_grid(hx, hy, tx, ty, min_x, min_y, max_x, max_y):
    w = max_x - min_x + 1
    h = max_y - min_y + 1
    # print(f"{hx=} {hy=} {tx=} {ty=} {min_x=} {min_y=} {max_x=} {max_y=} {w=} {h=}")
    grid = [["." for _ in range(w)] for _ in range(h)]
    grid[0-min_y][0-min_x] = "s"
    grid[ty-min_y][tx-min_x] = "T"
    grid[hy-min_y][hx-min_x] = "H"
    # print(grid_to_str(reversed(grid)))


def delta(dir) -> tuple[int, int]:
    if dir == "R":
        dx, dy = (+1, 0)
    elif dir == "L":
        dx, dy = (-1, 0)
    elif dir == "U":
        dx, dy = (0, +1)
    elif dir == "D":
        dx, dy = (0, -1)
    else:
        raise ValueError(f"Unknown direction {dir}")
    return dx, dy


def bounding_box(moves: list[tuple[str, int]]):
    min_x = min_y = max_x = max_y = 0
    hx = hy = 0
    for dir, n in moves:
        dx, dy = delta(dir)
        hx += n * dx; hy += n * dy
        min_x = min(min_x, hx)
        min_y = min(min_y, hy)
        max_x = max(max_x, hx)
        max_y = max(max_y, hy)

    return (min_x, min_y, max_x, max_y)


def compute1(moves: list[tuple[str, int]]) -> int:
    hx = hy = tx = ty = 0
    min_x, min_y, max_x, max_y = bounding_box(moves)
    draw_grid(hx, hy, tx, ty, min_x, min_y, max_x, max_y)
    tail_positions = set()
    tail_positions.add((tx, ty))
    for dir, n in moves:
        logging.debug(f"\n\n== {dir} {n} ==")
        dx, dy = delta(dir)
        for i in range(n):
            px, py = abs(hx - tx), abs(hy - ty)
            hx += dx; hy += dy
            sx, sy = abs(hx - tx), abs(hy - ty)
            logging.debug(f"{hx=} {hy=} {tx=} {ty=} {sx=} {sy=}")
            if sx == 2 and sy == 0:
                tx += dx
                tail_positions.add((tx, ty))
            elif sy == 2 and sx == 0:
                ty += dy
                tail_positions.add((tx, ty))
            elif (hx, hy) != (tx, ty):
                if sx == 2:
                    assert sy == 1
                    assert px == 1 and py == 1
                    tx += dx
                    ty = hy
                elif sy == 2:
                    assert sx == 1
                    assert px == 1 and py == 1
                    ty += dy
                    tx = hx
                else:
                    assert 0 <= sx < 2 and 0 <= sy < 2
                tail_positions.add((tx, ty))

            draw_grid(hx, hy, tx, ty, min_x, min_y, max_x, max_y)

    logging.info(tail_positions)
    return len(tail_positions)


def draw_rope(rope, min_x, min_y, max_x, max_y):
    if not logging.root.isEnabledFor(logging.DEBUG):
        return

    width = max_x - min_x + 1
    height = max_y - min_y + 1
    grid = [["." for _ in range(width)] for _ in range(height)]
    grid[rope[0][1]-min_y][rope[0][0]-min_x] = "H"
    for i, (kx, ky) in enumerate(rope[1:], 1):
        if grid[ky-min_y][kx-min_x] == ".":
            grid[ky-min_y][kx-min_x] = str(i)
    if grid[0-min_y][0-min_x] == ".":
        grid[0-min_y][0-min_x] = "s"
    print(grid_to_str(reversed(grid)))


def offset(h, t):
    if h > t:
        return -1
    elif h < t:
        return +1
    else:
        return 0


def compute2(moves: list[tuple[str, int]], knots=10) -> int:
    min_x, min_y, max_x, max_y = bounding_box(moves)
    rope = [(0, 0) for _ in range(knots)]
    draw_rope(rope, min_x, min_y, max_x, max_y)
    tail_positions = set()

    for dir, n in moves:
        logging.debug(f"\n\n== {dir} {n} ==")
        dx, dy = delta(dir)
        for i in range(n):
            rope[0] = (rope[0][0] + dx, rope[0][1] + dy)
            places = set()
            for k in range(1, knots):
                hx, hy = rope[k-1]
                tx, ty = rope[k]
                nx, ny = rope[k]
                sx, sy = abs(hx - tx), abs(hy - ty)
                logging.debug(f"{k=} {hx=} {hy=} {tx=} {ty=} {sx=} {sy=}")
                if sy == 0:
                    nx = hx + offset(hx, tx)
                elif sx == 0:
                    ny = hy + offset(hy, ty)
                elif sy > sx:
                    ny = hy + offset(hy, ty)
                    nx = hx
                elif sx > sy:
                    nx = hx + offset(hx, tx)
                    ny = hy
                else:
                    nx = hx + offset(hx, tx)
                    ny = hy + offset(hy, ty)
                logging.debug(f"\t{nx=} {ny=}")
                rope[k] = (nx, ny)
                if k == knots - 1:
                    tail_positions.add((nx, ny))
                if abs(nx - tx) not in {0,1} or abs(ny - ty) not in {0,1}:
                    draw_rope(rope, min_x, min_y, max_x, max_y)
                    assert False

            logging.debug(rope)
            draw_rope(rope, min_x, min_y, max_x, max_y)

    # logging.info(tail_positions)
    return len(tail_positions)


def main():
    namespace = parse_args()
    payload = load_data(namespace)
    result1 = compute2(payload, knots=2)
    print(f"{result1=}")
    payload = load_data(namespace)
    result2 = compute2(payload)
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
