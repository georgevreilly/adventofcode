#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 13
# https://adventofcode.com/2022/day/13

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
    result = []
    for stanza in text_data.split("\n\n"):
        result.append(tuple(eval(l) for l in stanza.strip().split("\n")))
    return result


def compare(l1, l2, level=0) -> int:
    indent = " " * 4 * level
    logging.debug(f"{indent}compare({l1=!r} (len={len(l1)}), "
                  f"{l2=!r} (len={len(l2)}), {level=})")
    indent += " " * 4
    level += 1

    for l, r in zip(l1, l2):
        logging.debug(f"{indent}> {l=!r} {r=!r}")
        if isinstance(l, int):
            if isinstance(r, int):
                if (cmp := l - r) != 0:
                    logging.debug(f"{indent} {l=!r} <> {r=!r} {cmp=}")
                    return cmp
            elif isinstance(r, list):
                if (cmp := compare([l], r, level)) != 0:
                    logging.debug(f"{indent} abort {l=!r} {r=!r} {cmp=}")
                    return cmp
            else:
                assert False, f"{l=!r} {r=!r}"
        elif isinstance(r, int):
            if isinstance(l, int):
                if (cmp := l - r) != 0:
                    logging.debug(f"{indent} {l=!r} <> {r=!r} {cmp=}")
                    return cmp
            elif isinstance(l, list):
                if (cmp := compare(l, [r], level)) != 0:
                    logging.debug(f"{indent} abort {l=!r} {r=!r} {cmp=}")
                    return cmp
            else:
                assert False, f"{l=!r} {r=!r}"
        else:
            assert isinstance(l, list) and isinstance(r, list)
            if (cmp := compare(l, r, level)) != 0:
                logging.debug(f"{indent} abort {l=!r} {r=!r}")
                return cmp
    cmp = len(l1) - len(l2)
    logging.debug(f"{indent} len(l1)={len(l1)} len(l2)={len(l2)} {cmp=}")
    return cmp


def compute1(packet_pairs: tuple[list]) -> int:
    total = 0
    for i, (l, r) in enumerate(packet_pairs, 1):
        ordered = compare(l, r, 0) < 0
        logging.info(f"{i=} {l=!r} {r=!r} {ordered=}\n")
        total += i if ordered else 0
    return total


def compute2(packet_pairs: tuple[list]) -> int:
    DIV2 = [[2]]
    DIV6 = [[6]]
    packets = [p for pair in packet_pairs for p in pair]
    packets.extend([DIV2, DIV6])
    packets = sorted(packets, key=functools.cmp_to_key(compare))
    index2 = packets.index(DIV2) + 1
    index6 = packets.index(DIV6) + 1
    logging.debug(f"{packets=}")
    logging.info(f"{index2=}, {index6=}")
    return index2 * index6
    


def main():
    namespace = parse_args()
    payload = load_data(namespace)
    # logging.debug(json.dumps(payload, indent=4))
    result1 = compute1(payload)
    print(f"{result1=}")
    payload = load_data(namespace)
    result2 = compute2(payload)
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
