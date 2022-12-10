#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 10
# https://adventofcode.com/2022/day/10

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


def parse_data(text_data: str) -> list[list[int]]:
    return [(line[0], int(line[1]) if len(line) > 1 else 0) for line in [
        line.strip().split() for line in text_data.strip().split('\n')]]


def compute1(instructions: list[tuple[str, int]]) -> int:
    x_vals = []
    x = 1
    cycles = 1
    for inst, value in instructions:
        logging.debug(f"{cycles=} {x=} {inst=} {value=}")
        if inst == "noop":
            x_vals.append(x)
            cycles += 1
        elif inst == "addx":
            x_vals.append(x)
            cycles += 1
            x_vals.append(x)
            cycles += 1
            x += value

    samples = [(x, (i+1)) for i, x in enumerate(x_vals) if i % 40 == 19]
    logging.debug(samples)
    return sum([x * t for x, t in samples])


CRT_WIDTH = 40


def compute2(instructions: list[tuple[str, int]]) -> int:
    row = ["." for _ in range(CRT_WIDTH)]
    cycles = 1
    x = 1

    def render():
        c = (cycles - 1) % CRT_WIDTH
        if c - 1 <= x <= c + 1:
            row[c] = "#"
        if c == CRT_WIDTH - 1:
            print("".join(row))
            for i in range(CRT_WIDTH):
                row[i] = "."

    for inst, value in instructions:
        logging.debug(f"{cycles=} {x=} {inst=} {value=}")
        if inst == "noop":
            render()        
            cycles += 1

        elif inst == "addx":
            render()
            cycles += 1

            render()
            cycles += 1

            x += value


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
