#!/usr/bin/env python3

# https://adventofcode.com/2021/day/3#part1

from __future__ import annotations

import os


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

def read_data():
    with open(os.path.join(os.path.dirname(__file__), "day03input.txt")) as f:
        return [l.strip() for l in f]

real_data = read_data()


def my_filter(data, most: bool):
    for b in range(len(data[0])):
        off = on = 0
        for line in data:
            if line[b] == "1":
                on += 1
            else:
                off += 1
        if on >= off:
            value = "1" if most else "0"
        elif on < off:
            value = "0" if most else "1"
        data = [line for line in data if line[b] == value]
        #print(f"{b:2}, value={value}, data={data}")
        if len(data) <= 1:
            break
    return data[0], int(data[0], 2)

def life_support_rating(data):
    og = my_filter(data, most=True)
    print("OG", og)
    co2 = my_filter(data, most=False)
    print("CO2", co2)
    print(og[1] * co2[1])

life_support_rating(test_data)
life_support_rating(real_data)
