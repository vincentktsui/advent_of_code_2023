from grid import Grid
from collections import deque
import sys
sys.setrecursionlimit(5000)

file = open("day16.txt", "r")
lines = file.readlines()

grid = Grid(lines)
print(grid)



direction_coords = {
    "N": (-1, 0),
    "S": (1, 0),
    "W": (0, -1),
    "E": (0, 1)
}


def resulting_directions(direction, obstacle)->list:
    if obstacle == ".":
        return [direction]
    elif obstacle == "|":
        if direction in ["N", "S"]:
            return [direction]
        elif direction in ["E", "W"]:
            return ["N", "S"]
    elif obstacle == "-":
        if direction in ["E", "W"]:
            return [direction]
        elif direction in ["N", "S"]:
            return ["W", "E"]
    elif obstacle == "/":
        if direction == "N":
            return ["E"]
        elif direction == "S":
            return ["W"]
        elif direction == "W":
            return ["S"]
        elif direction == "E":
            return ["N"]
    elif obstacle == "\\":
        if direction == "N":
            return ["W"]
        elif direction == "S":
            return ["E"]
        elif direction == "W":
            return ["N"]
        elif direction == "E":
            return ["S"]



def sol(initial_coord, initial_direction):
    beams = deque()
    beams.append((*initial_coord, initial_direction))
    energized = {}
    cache = {}

    while len(beams):
        beam = beams.popleft()
        coordinate, direction = beam[0: 2], beam[2]
        x, y = coordinate
        if not 0 <= x < grid.rows or not 0 <= y < grid.cols:
            continue
        if beam in cache:
            continue
        cache[beam] = True
        energized[coordinate] = True
        obstacle = grid[coordinate]
        res_dir = resulting_directions(direction, obstacle)
        for dir in res_dir:
            xd, yd = direction_coords[dir]
            new_coordinate = (x + xd, y + yd)
            beams.append((*new_coordinate, dir))
    return energized



def dfs(beam, memo: dict[tuple, set], visited: set) -> set:
    if beam in memo:
        return memo[beam]
           
    coordinate, direction = beam[0: 2], beam[2]
    x, y = coordinate
    if not 0 <= x < grid.rows or not 0 <= y < grid.cols:
        return set()
    
    memo[beam] = set([beam])

    obstacle = grid[coordinate]
    res_dir = resulting_directions(direction, obstacle)

    for dir in res_dir:
        xd, yd = direction_coords[dir]
        new_coordinate = (x + xd, y + yd)
        new_beam = (*new_coordinate, dir)

        if new_beam not in memo:
            resulting_beams = dfs(new_beam, memo, visited)
        else:
            resulting_beams = memo.get(new_beam, set())
            visited.add(new_beam)
        memo[beam].update(resulting_beams)
    
    # when returning, reverse propagate
    if beam in visited:
        for key, reachables in memo.items():
            if beam in reachables:
                memo[key].update(memo[beam])
        visited.remove(beam)

    return memo[beam]

# memo = {}
# temp = dfs((0,0, "E"), memo, set())
# print("memo")
# for key, value in memo.items():
#     print(key, ":", sorted(list(value)))
# print(temp)
# print(len(set([beam[0:2] for beam in temp])))


max_energized = 0
memo = {}
for i in range(grid.rows):
    temp = dfs((i, 0, "E"), memo, set())
    energized = len(set([beam[0:2] for beam in temp]))
    print(i, 0, energized, len(sol((i, 0), "E").keys()))
    max_energized = max(max_energized, energized)
    temp = dfs((i, grid.cols - 1, "W"), memo, set())
    energized = len(set([beam[0:2] for beam in temp]))
    print(i, grid.cols - 1, energized, len(sol((i, grid.cols - 1), "W").keys()))
    max_energized = max(max_energized, energized)
for j in range(grid.cols):
    temp = dfs((0, j, "S"), memo, set())
    energized = len(set([beam[0:2] for beam in temp]))
    print(0, j, energized, len(sol((0, j), "S").keys()))
    max_energized = max(max_energized, energized)
    temp = dfs((grid.rows - 1, j, "N"), memo, set())
    energized = len(set([beam[0:2] for beam in temp]))
    print(grid.rows - 1, j, energized, len(sol((grid.rows - 1, j), "N").keys()))
    max_energized = max(max_energized, energized)
print(max_energized)

# temp = (dfs((0, 3, "S"), {}))
# energized = set([beam[0:2] for beam in temp])
# print(len(energized))
# max_energized = 0
# for i in range(grid.rows):
#     max_energized = max(max_energized, len(sol((i, 0), "E").keys()))
#     max_energized = max(max_energized, len(sol((i, grid.cols - 1), "W").keys()))
# for j in range(grid.cols):
#     max_energized = max(max_energized, len(sol((0, j), "S").keys()))
#     max_energized = max(max_energized, len(sol((grid.rows - 1, j), "N").keys()))
# print(max_energized)