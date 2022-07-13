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
import heapq
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


def heuristic(state, dirt_locs):
    dirt_dists = []
    for dirt_loc in dirt_locs:
        dirt_dists.append(abs(state.pos.i - dirt_loc.i) + abs(state.pos.j - dirt_loc.j))
    dirt_dists.sort()
    alpha = 0.5
    weight = 1/alpha
    cost = 0
    for dist in dirt_dists:
        weight *= alpha
        cost += dist * weight
    return cost + state.num_dirt


def getSuccessors(state, dirt_locs):
    actions = set()
    successors = set()
    pos = state.pos
    if pos in dirt_locs:
        actions.add("CLEAN")
    if pos.i - 1 >= 0:
        actions.add("UP")
    if pos.i + 1 < 5:
        actions.add("DOWN")
    if pos.j - 1 >= 0:
        actions.add("LEFT")
    if pos.j + 1 < 5:
        actions.add("RIGHT")
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
    avg_i = avg_i // len(dirt_locs)
    avg_j = avg_j // len(dirt_locs)
    cod = Position(avg_i, avg_j)
    if state in goalStates:
        return None
    for nextState, action, stepCost in getSuccessors(state, dirt_locs):
        priority = heuristic(nextState, dirt_locs)
        heapq.heappush(pq, (priority, action))
    priority, action = heapq.heappop(pq)
    print(action)
    return action
# Tail starts here


if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)