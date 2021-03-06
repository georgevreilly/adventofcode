#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict

DAY = 12
# https://adventofcode.com/2021/day/12

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
        custom=0,
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
        "--custom", "-C", type=int,
            help="Use custom data")
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="More verbose logging")
    namespace = parser.parse_args()

    if namespace.custom:
        namespace.input_filename = f"day{DAY:02}test_input{namespace.custom}.txt"
    else:
        namespace.input_filename = REAL_DATA if namespace.real else TEST_DATA
    log_level = logging.DEBUG if namespace.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    return namespace


def read_data(input_filename: str):
    with open(os.path.join(os.path.dirname(__file__), input_filename)) as f:
        return f.readlines()


def parse_data(text_data: list[str]) -> dict[str, list[str]]:
    pairs = defaultdict(list)
    for line in text_data:
        src, dst = line.strip().split("-")
        pairs[src].append(dst)
        pairs[dst].append(src)
    return pairs


def load_data(namespace) -> list[list[int]]:
    text_data = read_data(namespace.input_filename)
    logging.info("%s", namespace.input_filename)
    logging.debug("%s", text_data)
    data = parse_data(text_data)
    return data


def explore1(node: str, pairs: dict[str, list[str]], seen: set[str], path: list[str]):
    logging.debug(f"explore1: {path=} {node=} {seen=} caves={pairs[node]}")
    if node == "end":
        logging.debug(f"\tPath: {path}")
        yield path
    else:
        for cave in pairs[node]:
            if cave in seen and cave.islower():
                continue
            yield from explore1(cave, pairs, seen | {node}, path + [cave])


def compute1(pairs: dict[str, list[str]]) -> int:
    paths = [path for path in explore1("start", pairs, set(), ["start"])]
    for path in paths:
        logging.debug(f'{",".join(path)}')
    return len(paths)


def explore2(node: str, pairs: dict[str, list[str]], seen: dict[str, int], path: list[str]):
    if node == "end":
        logging.debug(f"\tPath: {path}")
        yield path
    else:
        seen = seen.copy()
        if node.islower():
            seen[node] += 1
        logging.debug(f"explore2: path={','.join(path)} {node=} {seen=} caves={pairs[node]}")
        for cave in set(pairs[node]) - {"start"}:
            prev = seen[cave]
            if prev == 2 or (prev == 1 and any(v == 2 for v in seen.values())):
                continue
            yield from explore2(cave, pairs, seen, path + [cave])


def compute2(pairs: dict[str, list[str]]) -> int:
    paths = [path for path in explore2("start", pairs, defaultdict(int), ["start"])]
    for path in paths:
        logging.debug(f'{",".join(path)}')
    return len(paths)


def main():
    namespace = parse_args()
    result1 = compute1(load_data(namespace))
    print(f"{result1=}")
    result2 = compute2(load_data(namespace))
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
