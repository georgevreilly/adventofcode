#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 17
# https://adventofcode.com/2022/day/17

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
    return text_data.strip()


ROCK_SHAPES = (
    (
        '-',
        4, 1,
        0b1111,
    ),
    (
        '+',
        3, 3,
        0b010,
        0b111,
        0b010,
    ),
    (
        'L',
        3, 3,
        0b001,
        0b001,
        0b111,
    ),
    (
        '|',
        1, 4,
        0b1,
        0b1,
        0b1,
        0b1,
    ),
    (
        '.',
        2, 2,
        0b11,
        0b11,
    ),
)
HEADER = 3  # label, width, height
WIDTH = 7
HORIZ_OFS = 2
VERT_OFS = 3
EMPTY_LEVEL = 0b0000000
FULL_LEVEL  = 0b1111111


def print_chamber(label, chamber, force=False):
    if force or logging.root.isEnabledFor(logging.DEBUG):
        print(f"\n{label}")
        for row in reversed(chamber):
            print(f"{row:07b}".replace("0", ".").replace("1", "#"))


def simulate(jets: str, rock_count: int) -> int:
    chamber = []
    rocks = 0
    j = -1
    snipped = 0

    while rocks < rock_count:
        if rocks % 1_000_000 == 0: print(rocks)
        rock = ROCK_SHAPES[rocks % len(ROCK_SHAPES)]
        label, rw, rh = rock[0], rock[1], rock[2]
        chamber.extend([EMPTY_LEVEL for _ in range(rh + VERT_OFS)])
        rx = HORIZ_OFS
        ry = len(chamber) - rh
        shift = (WIDTH - rw - rx)
        for y in range(rh):
            chamber[ry + y] = rock[-y - 1] << shift
        for y in range(VERT_OFS):
            chamber[ry - 1 - y] = EMPTY_LEVEL
        print_chamber(f"Rock {rocks + 1} '{label}' at {ry}", chamber)

        while True:
            j = (j + 1) % len(jets)
            dx = +1 if jets[j] == ">" else -1

            # clear
            for y in range(rh):
                chamber[ry + y] ^= rock[-y - 1] << shift

            if 0 <= shift - dx <= WIDTH - rw:
                for y in range(rh):
                    cr = chamber[ry + y]
                    rk = rock[-y - 1] << (shift - dx)
                    if (cr ^ rk) & cr != cr:
                        logging.debug(f"horiz overlap at {ry+y}: {cr:07b} {rk=:07b}")
                        dx = 0
                        break
            else:
                dx = 0
            
            rx += dx
            shift -= dx
            for y in range(rh):
                chamber[ry + y] |= rock[-y - 1] << shift

            print_chamber(f"{jets[j]} {rx=} {dx=}", chamber)

            if ry == 0:
                logging.debug("floor")
                top = 0
                chamber = chamber[:1]
                break

            dy = -1
            for y in range(rh):
                chamber[ry + y] ^= rock[-y - 1] << shift
            for y in range(rh):
                cr = chamber[ry + y - 1]
                rk = rock[-y - 1] << shift
                if (cr ^ rk) & cr != cr:
                    logging.debug(f"vert overlap at {ry+y}: {cr:07b} {rk=:07b}")
                    dy = 0
                    break
            ry += dy
            for y in range(rh):
                chamber[ry + y] ^= rock[-y - 1] << shift

            if dy == 0:
                logging.debug(f"Finished with rock {rocks + 1}")
                break
            if chamber[-1] == EMPTY_LEVEL:
                chamber = chamber[:-1]
            print_chamber(f"fall to {ry}", chamber)

        rocks += 1

        if True:
            mask = 0
            for y in range(len(chamber) - 1, ry, -1):
                mask |= chamber[y]
                if mask == FULL_LEVEL:
                    snipped += y
                    # print_chamber(f"Full at {y}. {snipped=}", chamber, True)
                    chamber = chamber[y:]
                    # print_chamber(f"Net", chamber, True)
                    assert functools.reduce(lambda x, y: x | y, chamber, 0) == FULL_LEVEL
                    break


    print_chamber(f"Finished", chamber, force=True)

    return len(chamber) + snipped


def main():
    namespace = parse_args()
    payload = load_data(namespace)
    # logging.debug(json.dumps(payload, indent=4))
    rock_count = 2022
    result1 = simulate(payload, rock_count)
    print(f"{result1=}")

    # Too slow. Find cycles
    # rock_count = 1_000_000_000_000
    # payload = load_data(namespace)
    # result2 = simulate(payload, rock_count)
    # print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
