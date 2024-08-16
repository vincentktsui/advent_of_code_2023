import math
from collections import defaultdict

file = open("day11.txt", "r")
lines = file.readlines()
galaxy = [[*line.strip()] for line in lines]
empty_rows = []
empty_columns = []

for i in range(0, len(galaxy)):
    if all(x == "." for x in galaxy[i]):
        empty_rows.append(i)
for j in range(0, len(galaxy[0])):
    column = [galaxy[i][j] for i in range(0, len(galaxy))]
    if all(x == "." for x in column):
        empty_columns.append(j)

# for i in range(len(galaxy) - 1, -1, -1):
#     if all(x == "." for x in galaxy[i]):
#         galaxy.insert(i, ["."] * len(galaxy[0]))
# for j in range(len(galaxy[0]) - 1, -1, -1):
#     column = [galaxy[i][j] for i in range(0, len(galaxy))]
#     if all(x == "." for x in column):
#         for i in range(0, len(galaxy)):
#             galaxy[i].insert(j, ".")

galaxies = []

for i in range(0, len(galaxy)):
    for j in range(0, len(galaxy[0])):
        if galaxy[i][j] == "#":
            galaxies.append([i, j])


def min_distance(g1, g2):
    lower_row, higher_row = 0, 0
    lower_column, higher_column = 0, 0
    if g1[0] < g2[0]:
        lower_row, higher_row = g1[0], g2[0]
    else:
        lower_row, higher_row = g2[0], g1[0]
    if g1[1] < g2[1]:
        lower_column, higher_column = g1[1], g2[1]
    else:
        lower_column, higher_column = g2[1], g1[1]
    rows = [x for x in empty_rows if lower_row < x and x < higher_row]
    columns = [x for x in empty_columns if lower_column < x and x < higher_column]
    return (
        higher_row
        - lower_row
        - len(rows)
        + len(rows) * 1000000
        + higher_column
        - lower_column
        - len(columns)
        + len(columns) * 1000000
    )


# def min_distance(g1, g2):
#     return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])

print(galaxies, empty_rows, empty_columns)

distances = []
for i in range(0, len(galaxies) - 1):
    for j in range(i + 1, len(galaxies)):
        distances.append(min_distance(galaxies[i], galaxies[j]))
print(distances)
print(sum(distances))
