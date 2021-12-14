#!/usr/bin/env python3

from __future__ import annotations

DAY = 14
# https://adventofcode.com/2021/day/14

import argparse
import logging
import os

from collections import Counter


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


def parse_data(text_data: list[str]) -> tuple[list[str], dict[str, str]]:
    template = [c for c in text_data[0].strip()]
    rules = {}
    for rule in text_data[2:]:
        pair, element = [x.strip() for x in rule.split("->")]
        pair0 = pair[0] + element
        pair1 = element + pair[1]
        # logging.debug(f"{pair} -> {element} = {pair0},{pair1}")
        rules[pair] = (pair0, pair1)
    return template, rules


def load_data(namespace) -> list[list[int]]:
    if namespace.custom:
        text_data = ["-1"]
    else:
        text_data = read_data(namespace.input_filename)
        logging.info("%s", namespace.input_filename)
        # logging.debug("%s", text_data)
    data = parse_data(text_data)
    # logging.debug("%s", data)
    return data


def compute1(template, rules, steps) -> int:
    polymer = template
    for step in range(1, steps+1):
        new_polymer = []
        new_pairs = []
        pair_counts = {}
        for i in range(len(polymer) - 1):
            pair = polymer[i] + polymer[i+1]
            pair0, pair1 = rules[pair]
            new_polymer.append(pair0[0])
            new_polymer.append(pair0[1])

            pair_counts[pair0] = pair_counts.get(pair0, 0) + 1
            pair_counts[pair1] = pair_counts.get(pair1, 0) + 1
            new_pairs.extend([pair0, pair1])
        new_polymer.append(polymer[-1])
        logging.debug(f"{step=}: {''.join(polymer)} -> {''.join(new_polymer)}")
        logging.debug(f"{step=}: {''.join(new_polymer)} -> {pair_counts=} {new_pairs=}")
        logging.debug(f"{step=}: {len(new_polymer)}")
        polymer = new_polymer
    
    elements = {c for pairs in rules for c in pairs}
    counts = {c: polymer.count(c) for c in elements}
    frequency = sorted(counts.values())
    print(''.join(polymer))
    print(f"#polymer={len(polymer)} {counts=} {frequency=}")

    return frequency[-1] - frequency[0]


def compute2(template, rules, steps) -> int:
    # Nope. See mapleoctopus21.py
    print("\ncompute2")
    pairs = {}
    polymer = template
    for i in range(0, len(template) - 1):
        pair = template[i] + template[i + 1]
        increment = +1 # if i % 2 == 0 else -1
        pairs[pair] = pairs.get(pair, 0) + increment
    logging.debug(f"step=0: {pairs=}")

    for step in range(1, steps+1):
        new_polymer = []
        for i in range(len(polymer) - 1):
            pair = polymer[i] + polymer[i+1]
            pair0, _ = rules[pair]
            new_polymer.append(pair0[0])
            new_polymer.append(pair0[1])
        new_polymer.append(polymer[-1])
        polymer = new_polymer

        # new_pairs = {}
        new_pairs = pairs.copy()
        for pair in pairs:
            pair0, pair1 = rules[pair]
            if pair0 != pair and pair1 != pair:
                new_pairs[pair] = max(new_pairs[pair] - 1, 0)
            t0 = new_pairs[pair0] = pairs.get(pair0, 0) + 1
            t1 = new_pairs[pair1] = pairs.get(pair1, 0) + 1
            print(f"{pair=} -> {pair0=} {t0=}, {pair1=} {t1=}")
        pairs = new_pairs
        logging.debug(f"{step=}: {''.join(polymer)} {pairs=}")

    counts = {template[-1]: 1}

    for pair, count in pairs.items():
        print(f"\t{pair[0]}{pair[1]}: {pairs[pair]}")
        counts[pair[0]] = counts.get(pair[0], 0) + count
        counts[pair[1]] = counts.get(pair[1], 0) + count
    print(sum(pairs.values()))
    frequency = sorted(counts.values())
    print(f"{counts=} {frequency=}")

    return frequency[-1] - frequency[0]


def main():
    namespace = parse_args()
    result1 = compute1(*load_data(namespace), namespace.steps)
    print(f"{result1=}")
    result2 = compute2(*load_data(namespace), namespace.steps)
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
