##### NEED TO REVISIT


file = open("day18.txt", "r")
lines = file.readlines()
from collections import defaultdict
from grid import Grid

direction_coords = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}

map_to_pipe = {
    ("U", "U"): "|",
    ("D", "D"): "|",
    ("L", "L"): "-",
    ("R", "R"): "-",
    ("U", "L"): "7",
    ("U", "R"): "F",
    ("D", "L"): "J",
    ("D", "R"): "L",
    ("L", "U"): "L",
    ("L", "D"): "F",
    ("R", "U"): "J",
    ("R", "D"): "7",
    
}

def process_instructions(instructions: list) -> list:
    current = (0, 0)
    marked = []
    last_direction = None
    for instruction in instructions:
        direction, steps, *_ = instruction.strip().split(" ")
        for i in range(0, int(steps)):
            x, y = current
            dx, dy = direction_coords[direction]
            new_x, new_y = x + dx, y + dy
            if last_direction:
                last_pipe = map_to_pipe[(last_direction, direction)]
                marked[-1] = (*marked[-1][0: 3], last_pipe)
            marked.append((new_x, new_y, direction, None))
            current = (new_x, new_y)
            last_direction = direction

    # assign last pipe
    last = marked[-1]
    marked[-1] = (*last[0:3], map_to_pipe[(last[2],marked[0][2])])
    return marked

def form_grid(c: list)->Grid:
    min_x = min([tile[0] for tile in c])
    max_x = max([tile[0] for tile in c])
    min_y = min([tile[1] for tile in c])
    max_y = max([tile[1] for tile in c])

    rows = max_x - min_x + 1
    columns = max_y - min_y + 1

    empty_grid = [[''] * columns for _ in range(rows)]
    plan = Grid(empty_grid)

    for tile in c:
        plan[(tile[0] - min_x, tile[1]-min_y)] = tile[2: 4]
    return plan

def fill_inside(grid: Grid)->None:
    for i in range(grid.rows):
        walls = 0
        for j in range(grid.cols):
            if grid[(i, j)] and grid[(i, j)][1] in ["|", "L", "J"]:
                walls += 1
            else:
                if walls % 2:
                    grid[(i, j)] = "x"

def part1():
    coordinates = process_instructions(lines)
    plan = form_grid(coordinates)
    fill_inside(plan)

    count = 0
    for row in plan._grid:
        for e in row:
            if e:
                count += 1
    return count

print(part1())

map_direction = {
    0: "R",
    1: "D",
    2: "L",
    3: "U"
}

def convert_instructions(instructions):
    new_instructions = []
    for instruction in instructions:
        _, _, code = instruction.split()
        cleaned = code.replace("(", "").replace(")", "").replace("#", "")
        steps = int(cleaned[0:-1], 16)
        direction = map_direction[int(cleaned[-1])]
        new_instructions.append(f"{direction} {steps}")
    return new_instructions

def process_instructionsv2(instructions: list):
    left, right, up, down = 0, 0, 0, 0
    ix, iy = 0, 0
    for instruction in instructions:
        direction, steps, *_ = instruction.strip().split(" ")
        dx, dy = direction_coords[direction]
        ix += int(steps) * dx
        iy += int(steps) * dy
        up = min(ix, up)
        left = min(iy, left)
        down = max(ix, down)
        right = max(iy, right)

    current = (0, 0)
    horizontal, vertical = defaultdict(list), defaultdict(list)
    corners = defaultdict(list)
    last_direction = None
    for i in range(len(instructions)):
        instruction = instructions[i]
        direction, steps, *_ = instruction.strip().split(" ")
        x1, y1 = current
        dx, dy = direction_coords[direction]
        x2, y2 = x1 + int(steps) * dx, y1 + int(steps) * dy
        current = (x2, y2)
        if direction in ["U", "D"]:
            vertical[y1].append([min(x1, x2) + 1, max(x1, x2) - 1])
        elif direction in ["L", "R"]:
            horizontal[x1].append([min(y1, y2) + 1, max(y1, y2) - 1])
        if last_direction:
            corner = map_to_pipe[(last_direction,direction)]
            corners[x1].append((y1, corner))
        last_direction = direction
        if i == len(instructions) - 1:
            corner = map_to_pipe[(last_direction, instructions[0][0])]
            corners[x2].append((y2, corner))
            
    return left, right, up, down, horizontal, vertical, corners


def check_overlap(current, ranges):
    c0, c1 = current
    area = c1 - c0 + 1
    for r in ranges:
        r0, r1 = r
        if r1 < c0: continue
        if r0 > c1: continue
        if r0 <= c0 and r1 >= c1:
            return 0
        if r0 >= c0 and r1 <= c1:
            area -= (r1 - r0 + 1)
            continue
        if c0 <= r1 <= c1:
            area -= (r1 - c0 + 1)
            continue
        if c0 <= r0 <= c1:
            area -= (c1 - r0 + 1)
            continue
    return area


def count_area(left, right, up, down, hor, vert, corners):
    # print(left, right, up, down)
    # print(hor)
    # print(vert)
    # print(corners)
    area = 0
    for i in range(up, down + 1):
        hor_wall_ranges = []
        hor_wall_area = 0
        if hor[i]:
            hor_wall_ranges = hor[i]
            for hor_wall in hor_wall_ranges:
                hor_wall_area += (hor_wall[1] - hor_wall[0] + 1)
        area += hor_wall_area

        to_check = {}
        if corners[i]:
            for corner in corners[i]:
                to_check[corner[0]] = corner[1]
        for y, x_ranges in vert.items():
            for x_range in x_ranges:
                if x_range[0] <= i <= x_range[1] and y not in to_check:
                    to_check[y] = "|"
        wall = 0
        last_y = None
        corner_and_wall_area = 0
        corner_and_wall_ranges = [[k, k] for k in to_check.keys()]
        for y, obstacle in sorted(to_check.items()):
            corner_and_wall_area += 1
            if obstacle in ["L", "|", "J"]:
                wall += 1
                if not wall % 2 and last_y is not None:
                    ranges_to_check = [*hor_wall_ranges, *corner_and_wall_ranges]
                    temp = check_overlap([last_y + 1, y - 1], ranges_to_check)
                    # print("row", i, "last_y", last_y + 1, "current_y", y - 1, ranges_to_check, "new_area", temp)
                    area += temp
                last_y = y
        area += corner_and_wall_area
    return area



def part2():
    new_instructions = convert_instructions(lines)
    # new_instructions = lines
    count_area(*process_instructionsv2(new_instructions))


print(part2())