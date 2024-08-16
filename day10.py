import math
from collections import defaultdict

file = open("day10.txt", "r")
lines = file.readlines()
grid = [[*line.strip()] for line in lines]
h = len(grid)
w = len(grid[0])

pipe = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(0, -1), (1, 0)],
    "F": [(0, 1), (1, 0)],
    ".": [],
}


def search_connected(i, j, starting: bool = False):
    adjacent = [
        (-1, 0),
        (0, -1),
        (0, 1),
        (1, 0),
    ]
    connected_from = []
    for dir_x, dir_y in adjacent:
        x = i + dir_x
        y = j + dir_y
        if x < 0 or y < 0 or x >= h or y >= w:
            continue
        for dir in pipe[grid[x][y]]:
            if i == x + dir[0] and j == y + dir[1]:
                connected_from.append((dir_x, dir_y))
    if starting:
        return connected_from
    return pipe[grid[i][j]]


def find_starting():
    for i in range(0, h):
        for j in range(0, w):
            if grid[i][j] == "S":
                return (i, j)
    return (-1, -1)


def find_pipe(adjacents):
    for k, v in pipe.items():
        if all(dir if dir in v else 0 for dir in adjacents):
            return k
    return "."


starting_coord = find_starting()
# print(starting_coord)
starting_adjacents = search_connected(starting_coord[0], starting_coord[1], True)
starting_pipe = find_pipe(starting_adjacents)
grid[starting_coord[0]][starting_coord[1]] = starting_pipe


def bfs(starting):
    queue = [[starting]]
    visited = defaultdict(bool)
    while queue:
        elements = queue.pop(0)
        current_iter = []
        for e in elements:
            visited[e] = True
            i = e[0]
            j = e[1]
            dirs = search_connected(i, j)
            for d in dirs:
                adj = (i + d[0], j + d[1])
                if not visited[adj]:
                    current_iter.append(adj)
            if not current_iter:
                return visited
        queue.append(current_iter)
    return visited


main_loop = bfs(starting_coord)
# print(main_loop)

# mark all non-loop pipes as .
for i in range(0, h):
    for j in range(0, w):
        if not main_loop[(i, j)]:
            grid[i][j] = "."

for i in range(0, h):
    print("".join(grid[i]))


for i in range(0, h):
    pipes_encountered = 0
    for j in range(0, w):
        if main_loop[(i, j)]:
            if grid[i][j] in ["|", "L", "J"]:
                pipes_encountered += 1
            continue
        if grid[i][j] == "." and pipes_encountered % 2 == 0:
            grid[i][j] = "O"


area = 0
for i in range(0, h):
    for j in range(0, w):
        if grid[i][j] == ".":
            area += 1

print()
for i in range(0, h):
    print("".join(grid[i]))

print(area)

# def bfs(starting):
#     queue = [[starting]]
#     distance = 0
#     visited = defaultdict(bool)
#     while queue:
#         print(queue)
#         elements = queue.pop(0)
#         current_iter = []
#         for e in elements:
#             visited[e] = True
#             i = e[0]
#             j = e[1]
#             dirs = search_connected(i, j)
#             for d in dirs:
#                 adj = (i + d[0], j + d[1])
#                 if not visited[adj]:
#                     current_iter.append(adj)
#             if not current_iter:
#                 return distance
#         queue.append(current_iter)
#         distance += 1
#     return distance


# distance = bfs(starting_coord)
# print(distance)
