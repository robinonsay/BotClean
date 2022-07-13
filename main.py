#!/usr/bin/python
# Head ends here
# Sample Input
"""
0 0
b---d
-d--d
--dd-
--d--
----d
"""

import math
from collections import namedtuple

Position = namedtuple("Position", ["i", "j"])
State = namedtuple("State", ["pos", "num_dirt"])
ACTIONS = ("UP", "DOWN", "LEFT", "RIGHT", "CLEAN")
BOARD_SIZE = 5


def getDirtLocs(grid):
    dirt_locs = set()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if 'd' == grid[i][j]:
                dirt_locs.add(Position(i, j))
    return dirt_locs


def heuristic(s1, s2):
    dist = math.sqrt((s1.pos.i - s2.pos.i)**2 + (s1.pos.j - s2.pos.j)**2)
    dirt_size = abs(s1.num_dirt - s2.num_dirt)
    return dist + dirt_size


def getSuccessors(state, dirt_locs):
    cornerActions = {Position(0, 0): ["DOWN", "RIGHT"],
                     Position(0, BOARD_SIZE-1): ["DOWN", "LEFT"],
                     Position(BOARD_SIZE-1, 0): ["UP", "RIGHT"],
                     Position(BOARD_SIZE-1, BOARD_SIZE-1): ["UP", "LEFT"]}
    normalActions = {"UP", "DOWN", "LEFT", "RIGHT"}
    actions = set()
    successors = set()
    pos = state.pos
    if state.pos in dirt_locs:
        actions.add("CLEAN")
    if state.pos in cornerActions:
        for action in cornerActions[state.pos]:
            actions.add(action)
    else:
        actions += normalActions
    for action in actions:
        successor = None
        if action == "CLEAN":
            successor = (State(state.pos, state.num_dirt - 1), action, 1)
        elif action == "UP":
            successor = (State(Position(pos.i - 1, pos.j), state.num_dirt), action, 1)
        elif action == "DOWN":
            successor = (State(Position(pos.i + 1, pos.j), state.num_dirt), action, 1)
        elif action == "LEFT":
            successor = (State(Position(pos.i, pos.j - 1), state.num_dirt), action, 1)
        elif action == "RIGHT":
            successor = (State(Position(pos.i, pos.j + 1), state.num_dirt), action, 1)
        successors.add(successor)
    return successors


def next_move(posr, posc, grid):
    pq = []
    dirt_locs = getDirtLocs(grid)
    state = State(Position(posr, posc), len(dirt_locs))
    goalStates = set([State(dirt, 0) for dirt in dirt_locs])
    avg_i = 0
    avg_j = 0
    for dirt in dirt_locs:
        avg_i += dirt.i
        avg_j += dirt.j
    avg_i = avg_i / len(dirt_locs)
    avg_j = avg_j / len(dirt_locs)
    cod = Position(avg_i, avg_j)
    print(f"state: {state}")
    print(f"goalStates: {goalStates}")
    print(f"CoD: {cod}")
    print(f"successors: {getSuccessors(state, dirt_locs)}")

# Tail starts here


if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)