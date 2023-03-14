import numpy as np
from pathlib import Path

import re

datadir = Path("data")


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
        lines = open(filename).readlines()
        if output == "lines":
            return lines
        if output == "integers":
            regex = re.compile("-?\d+")
            return [[int(x) for x in re.findall(regex, line)] for line in lines]
        if output == "np":
            return np.loadtxt(filename, dtype=int, delimiter=",")

    return load
