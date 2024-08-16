import math

file = open("day3.txt", "r")
lines = file.readlines()
cleaned = [line.strip() for line in lines]
height = len(cleaned)
width = len(cleaned[0])


def search_adjacent(i, j):
    coordinates = [
        [i - 1, j - 1],
        [i - 1, j],
        [i - 1, j + 1],
        [i, j - 1],
        [i, j + 1],
        [i + 1, j - 1],
        [i + 1, j],
        [i + 1, j + 1],
    ]
    number_coordinates = []
    for x, y in coordinates:
        if x < 0 or y < 0 or x >= height or y >= width:
            continue
        if cleaned[x][y].isdigit():
            number_coordinates.append([x, y])
    return number_coordinates


def construct_number(i, j):
    left = j
    right = j
    while left >= -1 and right < width + 1:
        # print([i, left], [i, right], cleaned[i][left + 1 : right])
        if left >= 0 and cleaned[i][left].isdigit():
            left -= 1
            continue
        elif right < width and cleaned[i][right].isdigit():
            right += 1
            continue
        break
    # print(left, right)
    return ((i, left + 1), cleaned[i][left + 1 : right])


saved = {}

for i in range(height):
    for j in range(width):
        if cleaned[i][j] == ".":
            continue
        if cleaned[i][j] == "*":
            adj_number_coords = search_adjacent(i, j)
            adj_numbers = {}
            for x, y in adj_number_coords:
                starting_coord, number = construct_number(x, y)
                adj_numbers[starting_coord] = number
            if len(adj_numbers) >= 2:
                saved[(i, j)] = math.prod([int(x) for x in adj_numbers.values()])
print(saved)
print(sum(saved.values()))
# saved = {}

# for i in range(height):
#     for j in range(width):
#         if cleaned[i][j] == ".":
#             continue
#         if not cleaned[i][j].isdigit():
#             adj_number_coords = search_adjacent(i, j)
#             for x, y in adj_number_coords:
#                 starting_coord, number = construct_number(x, y)
#                 saved[starting_coord] = number

# numbers = [int(num) for num in saved.values()]
# print(sum(numbers))
