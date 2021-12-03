#!/usr/bin/env python3

# https://adventofcode.com/2021/day/3#part1

from __future__ import annotations

import os



def read_data():
    with open(os.path.join(os.path.dirname(__file__), "day03input.txt")) as f:
        return [l.strip() for l in f]


def parse_data(text):
    return [int(l, 2) for l in text]


def to_bin(n, bit_count):
    return f"{n:0{bit_count}b}"


def compute_epsilon_gamma(data):
    bit_count = len(data[0])
    bit_data = [int(l, 2) for l in data]
    gamma = 0
    epsilon = 0
    for b in range(bit_count):
        zero = one = 0
        mask = 1 << b
        for i, line in enumerate(bit_data):
            if line & mask:
                one += 1
            else:
                zero += 1
            # print(f"{line:02d}: {to_bin(line, bit_count)}, {data[i]}")

        if one > zero:
            gamma |= mask
            r = "g"
        elif one < zero:
            epsilon |= mask
            r = "e"
        else:
            print("even")
        print(f"{b:2}, {to_bin(mask, bit_count)}, 0={zero}, 1={one}, r={r}")
    return to_bin(gamma, bit_count), to_bin(epsilon, bit_count), gamma * epsilon

test_data = [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010",
]

print(compute_epsilon_gamma(test_data))

real_data = read_data()
print(compute_epsilon_gamma(real_data))
