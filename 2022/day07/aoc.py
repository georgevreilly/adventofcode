#!/usr/bin/env python3

from __future__ import annotations

YEAR = 2022
DAY = 7
# https://adventofcode.com/2022/day/7

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
        "--verbose", "-v", action="store_true",
        help="More verbose logging")
    namespace = parser.parse_args()

    namespace.input_filename = REAL_DATA if namespace.real else TEST_DATA
    log_level = logging.DEBUG if namespace.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    return namespace


def grid_to_str(grid: list[list[int]], prefix="") -> str:
    return prefix + ("\n" + prefix).join(
        "".join([str(n) for n in row]) for row in grid) + "\n"


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


def parse_data(text_data: str) -> list[str]:
    return [s.strip() for s in text_data.split('\n')]


def dir_size(tree: dict) -> tuple[dict, int]:
    size_map = {}

    def inner(tree: dict, path: str) -> tuple[dict, int]:
        size = 0
        for k, v in tree.items():
            if isinstance(v, dict):
                sub_path, sub_size = inner(v, os.path.join(path, k))
                size += sub_size
            else:
                size += v
        logging.debug(f"{path=}: {size=}")
        size_map[path] = size
        return (path, size)

    inner(tree, "/")
    return size_map


def parse_ops(lines: list[str]) -> int:
    path = "/"
    cwd = tree = {}
    listing = False
    for i, line in enumerate(lines, 1):
        parts = line.split()
        logging.debug(f"{i}: {parts=}: {path=} {tree=} {cwd=}")
        if not parts:
            break
        if parts[0] == "$":
            listing = False
            if parts[1] == "cd":
                if parts[2] == "/":
                    path = "/"
                    cwd = tree
                elif parts[2] == "..":
                    path = os.path.abspath(os.path.join(path, ".."))
                    cwd = tree
                    try:
                        for d in path.split("/"):
                            if d:
                                cwd = cwd[d]
                    except:
                        print(path)
                        print(json.dumps(tree, indent=4))
                        raise
                else:
                    path = os.path.join(path, parts[2])
                    cwd = cwd[parts[2]]
            elif parts[1] == "ls":
                listing = True
        elif listing:
            if parts[0] == "dir":
                cwd[parts[1]] = {}
            else:
                cwd[parts[1]] = int(parts[0])
    return tree


def compute1(lines: list[str]) -> int:
    tree = parse_ops(lines)
    print(json.dumps(tree, indent=4))
    size_map = dir_size(tree)
    print(json.dumps(size_map, indent=4))

    return sum(v if v <= 100_000 else 0 for k, v in size_map.items())


TOTAL_DISK_SPACE = 70_000_000
NEED = 30_000_000


def compute2(lines: list[str]) -> int:
    tree = parse_ops(lines)
    size_map = dir_size(tree)
    available = TOTAL_DISK_SPACE - size_map["/"]
    sizes = sorted([(s, d) for d, s in size_map.items()])
    print(sizes)
    for s, d in sizes:
        if s + available >= NEED:
            print(s, d)
            return s


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
