#!/usr/bin/env python3

from __future__ import annotations

DAY = 17
# https://adventofcode.com/2021/day/17

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
    xy = text_data[0].split("target area: ")[1].split(", ")
    pairs = [r.split("..") for r in [q.split("=")[1] for q in xy]]
    return [int(n) for pair in pairs for n in pair]


def load_data(namespace) -> list[list[int]]:
    if namespace.custom:
        text_data = ["-1"]
        data = parse_data(text_data)
    else:
        text_data = read_data(namespace.input_filename)
        logging.info("from: %s", namespace.input_filename)
        logging.debug("%s", text_data)
        data = parse_data(text_data)
    return data


def grid_to_str(grid: list[list[int]], prefix="") -> str:
    return prefix + ("\n" + prefix).join(
        "".join([str(n) for n in row]) for row in grid) + "\n"


def x_velocities(x1, x2):
    values = []
    for xv1 in range(x2, 1, -1):
        px = 0
        for xv2 in range(xv1, -1, -1):
            px += xv2
            if x1 <= px <= x2:
                values.append((xv1, xv1 - xv2 + 1))
                break
            elif px > x2:
                break
    values.reverse()
    return values


def probe_path(xv, yv, x1, x2, y1, y2):
    px = py = 0
    path = [(px, py)]
    y_max = y1
    logging.debug(f"{px=},{py=} {xv=},{yv=} {x1=},{x2=} {y1=},{y2=}")
    while True:
        px += xv; py += yv
        y_max = max(py, y_max)
        path.append((px, py))
        if xv:
            xv += -1 if xv > 0 else +1
        yv -= 1
        msg = f"{px=},{py=} {xv=},{yv=}"
        if x1 <= px <= x2 and y1 <= py <= y2:
            logging.debug("%s hit target!", msg)
            return path, y_max
        if px > x2 or py < y1:
            logging.debug("%s missed target!", msg)
            return None, y1


def compute1(x1, x2, y1, y2) -> int:
    # print(f"{x1=} {x2=} {y1=} {y2=}") 
    # path, y_max = probe_path(7, 2, x1, x2, y1, y2)
    # print(f"{path=} {y_max=}\n")
    # path, y_max = probe_path(6, 3, x1, x2, y1, y2)
    # print(f"{path=} {y_max=}\n")
    # path, y_max = probe_path(9, 0, x1, x2, y1, y2)
    # print(f"{path=} {y_max=}\n")
    # path, y_max = probe_path(17, -4, x1, x2, y1, y2)
    # print(f"{path=} {y_max=}\n")
    # path, y_max = probe_path(6, 9, x1, x2, y1, y2)
    # print(f"{path=} {y_max=}\n")
    xv, steps = x_velocities(x1, x2)[0]
    best_y_max = y1
    best_yv = None
    for yv in range(1, 1000):
        path, y_max = probe_path(xv, yv, x1, x2, y1, y2)
        logging.debug(yv, y_max)
        if y_max > best_y_max:
            best_y_max = y_max
            best_yv = yv
    return best_y_max, best_yv


def compute2(x1, x2, y1, y2) -> int:
    count = 0
    for xv, steps in x_velocities(x1, x2):
        for yv in range(y1, 4000):
            path, y_max = probe_path(xv, yv, x1, x2, y1, y2)
            if path is not None:
                count += 1
    return count


def main():
    namespace = parse_args()
    result1 = compute1(*load_data(namespace))
    print(f"{result1=}")
    result2 = compute2(*load_data(namespace))
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
