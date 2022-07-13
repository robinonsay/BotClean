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
Item = namedtuple("Item", ["state", "path", "cost"])
PQItem = namedtuple("PQItem", ["priority", "item"])
ACTIONS = ("UP", "DOWN", "LEFT", "RIGHT", "CLEAN")
BOARD_SIZE = 5


def getDirtLocs(grid):
    dirt_locs = set()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if 'd' == grid[i][j]:
                dirt_locs.add(Position(i, j))
    return dirt_locs


def getDist(pos1, pos2):
    return math.sqrt((pos1.i - pos2.i)**2 + (pos1.j - pos2.j)**2)


def heuristic(state, dirt_locs):
    dirt_list = list(dirt_locs)
    estimate = 0
    pos = state.pos
    while len(dirt_list) > 0:
        dirt_list.sort(key=lambda dirt: getDist(dirt, pos))
        estimate += getDist(dirt_list[0], pos)
        pos = dirt_list.pop(0)
    return estimate


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
            successor = (State(Position(pos.i - 1, pos.j), state.num_dirt), action, 2)
        elif action == "DOWN":
            successor = (State(Position(pos.i + 1, pos.j), state.num_dirt), action, 2)
        elif action == "LEFT":
            successor = (State(Position(pos.i, pos.j - 1), state.num_dirt), action, 2)
        elif action == "RIGHT":
            successor = (State(Position(pos.i, pos.j + 1), state.num_dirt), action, 2)
        successors.add(successor)
    return successors


def next_move(posr, posc, grid):
    pq = []
    explored = set()
    dirt_locs = getDirtLocs(grid)
    startState = State(Position(posr, posc), len(dirt_locs))
    goalStates = set([State(dirt, 0) for dirt in dirt_locs])
    priority = heuristic(startState, dirt_locs) + 0
    heapq.heappush(pq, PQItem(priority, Item(startState, None, 0)))
    while len(pq) != 0:
        _, item = heapq.heappop(pq)
        state, path, cost = item
        if state in explored:
            continue
        if state in goalStates:
            print(path[0])
            return path[0]
        explored.add(state)
        dirt_locs -= explored
        for nextState, action, stepCost in getSuccessors(state, dirt_locs):
            newCost = cost + stepCost
            newPath = []
            if path is not None:
                newPath = path.copy()
            newPath.append(action)
            priority = heuristic(nextState, dirt_locs) + newCost
            item = Item(nextState, newPath, newCost)
            heapq.heappush(pq, PQItem(priority, item))
# Tail starts here


if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)