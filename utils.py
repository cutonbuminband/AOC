from collections import deque, defaultdict
import queue
import numpy as np
from pathlib import Path
import re

datadir = Path("data")


def astar(
    start, end, neighbors, heuristic, weights=None, multiple_starts=False, **kwargs
):
    """Implementation of the A* path finding algorithm.

    parameters:
      - start: The initial node, or a list of starting nodes
      - end: The target node
      - neighbors: A function Node -> List[Node] which finds the valid neighbors of a node
      - heuristic: A heuristic function [Node, Node] -> Real which provides
        a lower bound on the distance between two nodes.
      - weights: A function [Node, Node] -> Real which gives the exact distance between
        two neighboring nodes
      - multiple_starts: are we starting from multiple nodes, or just one.
    returns:
      - The shortest path distance between start and end.
    """
    costs = defaultdict(lambda: np.inf)
    if not multiple_starts:
        start = [start]
    q = queue.PriorityQueue()
    for item in start:
        costs[item] = 0
        q.put((0, item))
    while q.qsize() > 0:
        _, state = q.get()
        if state == end:
            return costs[state]
        for neighbor in neighbors(state, **kwargs):
            current_cost = costs[state] + (
                1 if weights is None else weights(state, neighbor, **kwargs)
            )
            if current_cost < costs[neighbor]:
                costs[neighbor] = current_cost
                q.put((current_cost + heuristic(neighbor, end), neighbor))
    return costs[end]


def bfs(
    start, end, neighbors, initial_state=0, update=None, return_visited=False, **kwargs
):
    """Implementation of a BFS algorithm.

    parameters:
      - start: The initial node
      - end: Either a target node or a stopping condition. If the target is unreachable
        from start, or the stopping condition is always false, then all nodes reachable
        from start will be mapped out instead.
      - neighbors: A function Node -> List[Node] which finds the valid neighbors of a node,
        taking optional keyword arguments **kwargs
      - initial_state: What to return for bfs(start, start)
      - return_visited: (bool) if True, return visited nodes
    returns:
      - The result of calling update(update(...(initial_state))) when the end is
        reached, or when there are no more reachable nodes.
      - Or the nodes visited before the stopping condition is true.
    """
    if update is None:
        update = lambda steps, state, neighbor: steps + 1
    q = deque([(initial_state, start)])
    visited = set()
    if not callable(end):
        end_condition = lambda steps, state: state == end
    else:
        end_condition = end
    while q:
        steps, state = q.popleft()
        if end_condition(steps, state):
            break
        visited.add(state)
        for neighbor in neighbors(state, **kwargs):
            if neighbor in visited:
                continue
            q.append((update(steps, state, neighbor), neighbor))
    if return_visited:
        return visited
    return steps


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
    def load(day, output="lines", header=0, footer=None, **kwargs):
        filename = datadir / str(year) / f"{day}.txt"
        if output == "raw":
            return open(filename).read()
        lines = open(filename).readlines()[header:footer]
        if output == "lines":
            return lines
        if output == "int":
            regex = re.compile("-?\d+")
            integers = [[int(x) for x in re.findall(regex, line)] for line in lines]
            return [integer for integer in integers if integer]
        if output == "np":
            if "delimiter" not in kwargs:
                kwargs["delimiter"] = ","
            return np.loadtxt(filename, dtype=int, **kwargs)

    return load
