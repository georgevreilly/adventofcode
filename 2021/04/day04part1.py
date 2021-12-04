#!/usr/bin/env python3

# https://adventofcode.com/2021/day/4#part1

from __future__ import annotations

import os

def read_data(suffix: str):
    with open(os.path.join(os.path.dirname(__file__), f"day04{suffix}.txt")) as f:
        return [l.strip() for l in f]

def parse_data(lines: list[str]):
    numbers = [int(n.strip()) for n in lines[0].split(",")]
    boards = []
    for i in range(1, len(lines), 6):
        board = []
        for j in range(i+1, i+6):
            row = [int(n.strip()) for n in lines[j].split()]
            board.append(row)
        boards.append(board)
    return numbers, boards

def bingo(board) -> bool:
    for i in range(5):
        col = [row[i] for row in board]
        row = board[i]
        if all(n >= 100 for n in row):
            return f"row{i+1}", row
        if all(n >= 100 for n in col):
            return f"col{i+1}", col
    return "", []

def unmarked_sum(board) -> int:
    return sum(
        n for row in board
            for n in row
                if n < 100
    )


def winning_board_score(numbers, boards, ignore):
    for n in numbers:
        # print("Calling", n)
        for b, board in enumerate(boards):
            if ignore[b]:
                continue
            for r, row in enumerate(board):
                for c in range(5):
                    if row[c] == n:
                        boards[b][r][c] = 100 + n
                        break
            reason, vector = bingo(board)
            if reason:
                sum = unmarked_sum(board)
                score = n * sum
                print(f"Bingo! Board {b+1}: {reason} {vector} n={n} sum={sum} score={score}")
                ignore[b] = True
                return n, sum, score, b

def last_loser(numbers, boards):
    count = len(boards)
    ignore = [False] * count
    for _ in range(count):
        n, sum, score, b = winning_board_score(numbers, boards, ignore)
        winner = boards[b]
    print(score, winner)
    return score

numbers, boards = parse_data(read_data("test_input"))
last_loser(numbers, boards)

numbers, boards = parse_data(read_data("input"))
last_loser(numbers, boards)

