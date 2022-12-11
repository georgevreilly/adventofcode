#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 11
# https://adventofcode.com/2022/day/11

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


def parse_record(record: str) -> dict:
    lines = record.strip().split("\n")
    assert lines[0].startswith("Monkey")
    monkey = int(lines[0].split()[1].strip(":"))
    assert lines[1].startswith("  Starting items")
    starting_items = [int(n) for n in lines[1].split(":")[1].split(",")]
    assert lines[2].startswith("  Operation: new = old ")
    operation = tuple(lines[2].split(" = ")[1].split()[1:])
    assert lines[3].startswith("  Test: divisible by ")
    div_by = int(lines[3].split("by")[1].strip())
    assert lines[4].startswith("    If true: throw to monkey")
    true_target = int(lines[4].split()[-1])
    assert lines[5].startswith("    If false: throw to monkey")
    false_target = int(lines[5].split()[-1])
    return dict(
            monkey=monkey,
            items=starting_items,
            operation=operation,
            div_by=div_by,
            targets=(false_target, true_target),
        )


def parse_data(text_data: str) -> list[dict]:
    return [parse_record(r) for r in text_data.split("\n\n")]


def make_operation(verb, value):
    if value == "old":
        if verb == "*":
            return lambda old: old * old
        elif verb == "+":
            return lambda old: old + old
        else:
            raise ValueError(f"Unknown {verb=}")
    else:
        value = int(value)
        if verb == "*":
            return lambda old: old * value
        elif verb == "+":
            return lambda old: old + value
        else:
            raise ValueError(f"Unknown {verb=}")


def compute1(records: list[dict]) -> int:
    monkey_items = [r["items"] for r in records]
    ops = [make_operation(*r["operation"]) for r in records]
    div_bys = [r["div_by"] for r in records]
    targets = [r["targets"] for r in records]
    count = len(records)
    activity = [0 for _ in range(count)]

    for round in range(1, 20+1):
        for m in range(count):
            items = monkey_items[m]
            monkey_items[m] = []
            logging.debug(f"{m=} {items=}")
            for item in items:
                activity[m] += 1
                worry_level = ops[m](item) // 3
                divisible = (worry_level % div_bys[m]) == 0
                target = targets[m][int(divisible)]
                logging.debug(f"{round=}: {m=} {worry_level=} {divisible=} {target=}")
                monkey_items[target].append(worry_level)
        logging.debug(f"Finished {round=}")
        for m, items in enumerate(monkey_items):
            logging.debug(f"{m=} {items=} activity={activity[m]}")

    return math.prod(sorted(activity, reverse=True)[:2])


def compute2(records: list[dict], rounds=10000) -> int:
    monkey_items = [r["items"] for r in records]
    ops = [make_operation(*r["operation"]) for r in records]
    div_bys = [r["div_by"] for r in records]
    modulo = functools.reduce(operator.mul, div_bys)
    print(f"{modulo=}")
    targets = [r["targets"] for r in records]
    count = len(records)
    activity = [0 for _ in range(count)]

    for round in range(1, rounds+1):
        for m in range(count):
            items = monkey_items[m]
            monkey_items[m] = []
            logging.debug(f"{m=} {items=}")
            for item in items:
                activity[m] += 1
                worry_level = ops[m](item)
                divisible = (worry_level % div_bys[m]) == 0
                target = targets[m][int(divisible)]
                logging.debug(f"{round=}: {m=} {worry_level=} {divisible=} {target=}")
                monkey_items[target].append(worry_level % modulo)
        if round in {1, 20} or round % 1000 == 0:
            logging.info(f"Finished {round=}")
            for m, items in enumerate(monkey_items):
                logging.info(f"{m=} {items=} activity={activity[m]}")

    return math.prod(sorted(activity, reverse=True)[:2])


def main():
    namespace = parse_args()
    payload = load_data(namespace)
    # logging.debug(json.dumps(payload, indent=4))
    result1 = compute1(payload)
    print(f"{result1=}")
    payload = load_data(namespace)
    result2 = compute2(payload, rounds=10_000)
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
