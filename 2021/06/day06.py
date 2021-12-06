#!/usr/bin/env python3

from __future__ import annotations

DAY = 6
# https://adventofcode.com/2021/day/6#part1

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
        "--num-days", "-n", type=int, default=18,
        help="Days of simulation")
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
        return f.read().strip()


def parse_data(text_data: str) -> list[int]:
    return [int(n.strip()) for n in text_data.split(",")]


def simulate_growth(fish: list[int], num_days: int) -> int:
    logging.info("Initial state: %3d %r", len(fish), fish)
    for day in range(1, num_days + 1):
        new_fish = []
        extra = []
        for f in fish:
            if f == 0:
                extra.append(8)
                f = 6
            else:
                f -= 1
            new_fish.append(f)
        fish = new_fish + extra
        logging.debug("%s", f"After {day:2} days: {len(fish):2}: {fish!r}")
    return len(fish)


def simulate_growth2(fish: list[int], num_days: int) -> int:
    logging.info("Initial state: %3d %r", len(fish), fish)
    MAX = 10
    counts = [0 for _ in range(MAX)]
    for f in fish:
        counts[f] += 1
    for day in range(1, num_days + 1):
        spawn = counts[0]
        for i in range(MAX-1):
            counts[i] = counts[i+1]
        counts[MAX-1] = 0
        counts[6] += spawn
        counts[8] = spawn
        logging.debug("%s", f"After {day:2} days: {counts!r}")
    return sum(counts)


def main():
    namespace = parse_args()
    text_data = read_data(namespace.input_filename)
    logging.info("%s", namespace.input_filename)
    logging.debug("%s", text_data)
    lanternfish = parse_data(text_data)
    logging.debug("\nlanternfish: %s", lanternfish)
    result = simulate_growth2(lanternfish, namespace.num_days)
    print(f"Result: {result}")


if __name__ == "__main__":
    raise SystemExit(main())
