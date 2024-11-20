from grid import Grid
import heapq

file = open("day17.txt", "r")
lines = file.readlines()

heat_map = Grid(lines)
print(heat_map)

def dijkstras(grid, min_steps, max_steps):
    # priority queue with (heat, x, y, dx dy)
    queue = [(0, 0, 0, 0, 0)]
    visited = {}
    while queue:
        current = heapq.heappop(queue)
        heat, x, y, dx, dy = current

        if (x, y, dx, dy) in visited and visited[(x, y, dx, dy)] <= heat:
            continue

        visited[(x, y, dx, dy)] = heat
         
        # only turn left or right. Don't go straight or reverse
        for dir in {(-1, 0), (1, 0), (0, -1), (0, 1)} - {(dx, dy), (-dx, -dy)}:
            current_heat = heat
            for i in range(1, max_steps + 1):
                new_coord = (x + i * dir[0], y + i*dir[1])
                new_x, new_y = new_coord
                if not 0 <= new_x < grid.rows or not 0 <= new_y < grid.cols:
                    # since we're only going in 1 direction, if we encounter grid edge then next one will be out of bounds too
                    break
                current_heat += int(grid[new_coord])
                if i < min_steps:
                    continue
                new_x, new_y = new_coord

                if ((new_x, new_y, dir[0], dir[1]) not in visited or visited[(new_x, new_y, dir[0], dir[1])] > current_heat):
                    heapq.heappush(queue, (current_heat, new_x, new_y, dir[0], dir[1]))
    return visited

results = dijkstras(heat_map, 1, 3)
possible_heat = []
for k,  v in results.items():
    if k[0] == heat_map.rows - 1 and k[1] == heat_map.cols - 1:
        print(k, v)
        possible_heat.append(v)
print(min(possible_heat))

results = dijkstras(heat_map, 4, 10)
print(results)
possible_heat = []
for k,  v in results.items():
    if k[0] == heat_map.rows - 1 and k[1] == heat_map.cols - 1:
        print(k, v)
        possible_heat.append(v)
print(min(possible_heat))

            


