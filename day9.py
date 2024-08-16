import math
from collections import defaultdict

file = open("day9.txt", "r")
lines = file.readlines()
sequences = [[int(x) for x in line.strip().split()] for line in lines]


def diff_seq(seq):
    diff = []
    for i in range(len(seq) - 1, 0, -1):
        diff.append(seq[i] - seq[i - 1])
    return diff[::-1]


def generate_seq(seq):
    sequences = []
    current = seq
    while not all([x == 0 for x in current]):
        sequences.append(current)
        current = diff_seq(current)
    return sequences


def solve(sequences):
    sum = 0
    for seq in sequences[::-1]:
        # sum += seq[-1]
        sum = seq[0] - sum
    return sum


sol = [solve(generate_seq(x)) for x in sequences]
print(sol)
print(sum(sol))
