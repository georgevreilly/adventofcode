#!/usr/bin/env python3

from __future__ import annotations

DAY = 16
# https://adventofcode.com/2021/day/16

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

def to_bin(h):
    b = bin(int(h, 16))[2:]
    prefix = {0: "", 1: "000", 2: "00", 3: "0"}[len(b) % 4]
    return prefix + b


def parse_data(text_data: list[str]) -> list[list[int]]:
    return [(line, to_bin(line)) for line in text_data]


def load_data(namespace) -> list[list[int]]:
    if namespace.custom:
        text_data = ["-1"]
        data = parse_data(text_data)
    else:
        text_data = read_data(namespace.input_filename)
        logging.info("%s", namespace.input_filename)
        logging.debug("%s", text_data)
        data = parse_data(text_data)
    return data


def grid_to_str(grid: list[list[int]], prefix="") -> str:
    return prefix + ("\n" + prefix).join(
        "".join([str(n) for n in row]) for row in grid) + "\n"


def parse_number(tx, index):
    packet_type = int(tx[index:index+3], 2)
    if packet_type != 4:
        raise ValueError(f"Got {packet_type=} at {index=} in {tx=}")
    index += 3
    n = 0
    count = 2 if tx[index] == "1" else 1
    while count:
        nybble = tx[index+1:index+5]
        n = (n << 4) | int(nybble, 2)
        print(f"{index=} {nybble=} {n=}")
        index += 5
        if count == 1:
            break
        elif tx[index] == "0":
            count = 1
    return n, index


def decode_transmisssion(tx: int):
    payloads = []
    index = 0
    while index < len(tx):
        version = int(tx[index:index+3], 2)
        index += 3
        packet_type = int(tx[index:index+3], 2)
        print(f"{version=} {packet_type=}")
        if packet_type == 4:
            n, index = parse_number(tx, index)
            print(f"Got {n}, {index=}")
            payloads.append((4, n))
        elif packet_type == 6:
            index += 3
            length_type_id = tx[index]
            index += 1
            sub_packets = []
            if length_type_id == "0":
                r = total_length_in_bits = int(tx[index:index+15], 2)
                index += 15
                while r > 0:
                    n, index2 = parse_number(tx, index)
                    sub_packets.append(n)
                    r -= (index2 - index)
                    index = index2
                print(f"LTI:0 TLIB={total_length_in_bits}, {sub_packets=}")
            else:
                number_of_sub_packets = int(tx[index:index+11], 2)
                index += 11
                for _ in range(number_of_sub_packets):
                    n, index = parse_number(tx, index)
                    sub_packets.append(n)
                print(f"LTI:1 #packets={number_of_sub_packets}, {sub_packets=}")
        index = (index + 3) & ~3
    return payloads

# See https://github.com/pantaryl/adventofcode/blob/main/2021/src/day16.py

def compute1(transmissions: list[int]) -> int:
    for i, (hex, tx) in enumerate(transmissions):
        decode_transmisssion(tx)


def compute2(tile: list[list[int]]) -> int:
    return 0


def main():
    examples = parse_data([
#        "D2FE28",
        "38006F45291200",
        "EE00D40C823060",
        "8A004A801A8002F478",
        "620080001611562C8802118E34",
        "C0015000016115A2E0802F182340",
        "A0016C880162017C3686B18A3D4780",
    ])
    namespace = parse_args()
    result1 = compute1(examples)
    print(f"{result1=}")
    result2 = compute2(load_data(namespace))
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
