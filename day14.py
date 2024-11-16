from grid import Grid

file = open("day14.txt", "r")
lines = file.readlines()

grid = Grid(lines)
# print(grid)

def tilt(old_seq: list):
    seq = old_seq.copy()
    walls = [-1]
    for i in range(len(seq)):
        if seq[i] == "#":
            walls.append(i)
    walls.append(len(seq))

    for wall_idx in range(len(walls) - 1):
        start = walls[wall_idx] + 1
        end = walls[wall_idx+1] - 1

        while start <= end:
            if seq[start] == ".":
                start += 1
                continue
            if seq[start] == "O":
                if seq[end] == ".":
                    seq[end] = "O"
                    seq[start] = "."
                    end -= 1
                    start += 1
                    continue
                elif seq[end] == "O":
                    end -= 1
                    continue
    return seq

def tilt_direction(board: Grid, direction):
    rows = board.get_rows()
    columns = board.get_columns()
    if direction == "N":
        return Grid([tilt(column[::-1])[::-1] for column in columns], vertical=True)
    elif direction == "S":
        return Grid([tilt(column) for column in columns], vertical=True)
    elif direction == "E":
        return Grid([tilt(row) for row in rows])
    elif direction == "W":
        return Grid([tilt(row[::-1])[::-1] for row in rows])
    
def count_weight(board:Grid):
    weight = 0
    length = board.rows
    for i in range(length):
        row = board[i]
        weight += row.count("O") * (length - i)
    return weight


print(count_weight(tilt_direction(grid, "N")))

def cycle(board: Grid):
    n = tilt_direction(board, "N")
    w = tilt_direction(n, "W")
    s = tilt_direction(w, "S")
    e = tilt_direction(s, "E")
    return e

# print(cycle(grid))

def cycles(board: Grid, cycles: int):
    sequences = []
    sequences.append(board)
    temp = board
    cycle_size = 0
    cycle_start = 0
    for i in range(cycles):
        temp = cycle(temp)
        if temp in sequences:
            previous_idx = sequences.index(temp)
            cycle_size = (i + 1) - previous_idx
            cycle_start = previous_idx
            break
        else:
            sequences.append(temp)
    idx = (cycles - cycle_start) % cycle_size
    print(cycle_start, cycle_size, idx)
    return sequences[cycle_start + idx]
        
new_grid = cycles(grid, 1000000000)
print(new_grid)
print(count_weight(new_grid))




# def solver(pattern):
#     total_weight = 0
#     for column in pattern:
#         walls = [-1]
#         for i in range(len(column)):
#             if column[i] == "#":
#                 walls.append(i)

#         length = len(column) - 1
#         weight = 0

#         for wall_idx in range(len(walls)):
#             end = walls[wall_idx] + 1
#             start = walls[wall_idx+1] - 1 if wall_idx < len(walls)-1 else length

#             while end <= start:
#                 if column[start] == ".":
#                     start -= 1
#                     continue
#                 if column[start] == "O":
#                     if column[end] == ".":
#                         weight += (length + 1 - end)
#                         end += 1
#                         start -= 1
#                         continue
#                     elif column[end] == "O":
#                         weight += (length + 1 - end)
#                         end += 1
#                         continue
#         total_weight += weight
#     return total_weight

# print(solver(vertical_pattern))

