import queue
import numpy as np
from pathlib import Path

import re

datadir = Path("data")


def astar(start, end, neighbors, distance_function, multiple_starts=False):
    """Implementation of the A* path finding algorithm.

    parameters:
      - start: The initial node, or a list of starting nodes
      - end: The target node
      - neighbors: A function Node -> List[Node] which finds the valid neighbors of a node
      - distance function: A heuristic function [Node, Node] -> Real which provides
        a lower bound on the distance between two nodes.
      - multiple_starts: are we starting from multiple nodes, or just one.
    returns:
      - The shortest path distance between start and end.
    """
    costs = defaultdict(lambda: np.inf)
    if not multiple_starts:
        start = [start]
    q = queue.PriorityQueue()
    for item in start:
        q.put((0, item))
    while q:
        _, state = q.get()
        if state == end:
            return costs[state]
        for neighbor in neighbors(state):
            current_cost = costs[state] + 1
            if current_cost < costs[neighbor]:
                costs[neighbor] = current_cost
                q.put((current_cost + distance_function(neighbor, end), neighbor))
    return costs[end]


def bezout(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_s, old_t


def crt(congruences):
    """
    Given a list of pairs of numbers [(n1, a1), (n2, a2), ldots] find the
    smallest positive number x such that

    x ≡ a1 (mod n1)
    x ≡ a2 (mod n2)
    \vdots
    """

    N = np.product([pair[0] for pair in congruences])
    total = 0
    for n, a in congruences:
        m, M = bezout(n, N // n)
        total += a * M * (N // n)
    return total % N


def year_load(year):
    def load(day, output="lines"):
        filename = datadir / str(year) / f"{day}.txt"
        if output == "raw":
            return open(filename).read()
        lines = open(filename).readlines()
        if output == "lines":
            return lines
        if output == "int":
            regex = re.compile("-?\d+")
            return [[int(x) for x in re.findall(regex, line)] for line in lines]
        if output == "np":
            return np.loadtxt(filename, dtype=int, delimiter=",")

    return load
