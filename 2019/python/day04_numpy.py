"""Numpy is 14x faster than python (0.15s for numpy vs 2.13s for python)"""
import numpy as np


lower = 134564
upper = 585159


nums = np.arange(lower, upper + 1)
d = np.arange(6).reshape(-1, 1)
digits = (nums // (10 ** d)) % 10

#  N x 6 array representing each number as a vector
digits = digits[::-1].T

adjacent = (digits[:, :-1] == digits[:, 1:]).any(axis=1)
increasing = (digits[:, :-1] <= digits[:, 1:]).all(axis=1)

print("Part 1:")
print((adjacent & increasing).sum())

mask = digits[:, :-1] == digits[:, 1:]
bad = ~mask
bad[:, 1:] += mask[:, :-1]
bad[:, :-1] += mask[:, 1:]
run_of_two = ~(bad.all(axis=1))

print("Part 2:")
print((run_of_two & increasing).sum())
