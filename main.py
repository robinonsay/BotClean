#!/usr/bin/python
# Head ends here
from collections import namedtuple

State = namedtuple("State", [])


def heuristic(s1, s2):
    pass


def next_move(posr, posc, board):
    print("")


# Tail starts here

if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)