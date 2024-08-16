file = open("day5.txt", "r")
lines = file.read()


def split_list(list, size):
    temp = []
    for i in range(0, len(list), size):
        temp.append(list[i : i + size])
    return temp


split = lines.split(":")
seeds = split[1].strip().split()
seeds = [int(v) for v in seeds if v.isnumeric()]
seed_to_soil = split[2].strip().split()
seed_to_soil = [int(v) for v in seed_to_soil if v.isnumeric()]
seed_to_soil = split_list(seed_to_soil, 3)
soil_to_fertilizer = split[3].strip().split()
soil_to_fertilizer = [int(v) for v in soil_to_fertilizer if v.isnumeric()]
soil_to_fertilizer = split_list(soil_to_fertilizer, 3)
fertilizer_to_water = split[4].strip().split()
fertilizer_to_water = [int(v) for v in fertilizer_to_water if v.isnumeric()]
fertilizer_to_water = split_list(fertilizer_to_water, 3)
water_to_light = split[5].strip().split()
water_to_light = [int(v) for v in water_to_light if v.isnumeric()]
water_to_light = split_list(water_to_light, 3)
light_to_temperature = split[6].strip().split()
light_to_temperature = [int(v) for v in light_to_temperature if v.isnumeric()]
light_to_temperature = split_list(light_to_temperature, 3)
temperature_to_humidity = split[7].strip().split()
temperature_to_humidity = [int(v) for v in temperature_to_humidity if v.isnumeric()]
temperature_to_humidity = split_list(temperature_to_humidity, 3)
humidity_to_location = split[8].strip().split()
humidity_to_location = [int(v) for v in humidity_to_location if v.isnumeric()]
humidity_to_location = split_list(humidity_to_location, 3)

# print(seeds)
# print(seed_to_soil)
# print(soil_to_fertilizer)
# print(fertilizer_to_water)
# print(water_to_light)
# print(light_to_temperature)
# print(temperature_to_humidity)
# print(humidity_to_location)
# lines = lines.replace("\n", "")


def conversion(location, mappings: list[list[str]]):
    for m in mappings:
        start = m[1]
        range = m[2]
        end = start + range
        if location >= start and location < end:
            return location - start + m[0]
    return location


def conversion_list(loc: list[list[int]], mappings: list[list[int]]):
    ranges = loc.copy()
    transformed = []
    while ranges:
        r = ranges.pop()
        flag = False
        r_start = r[0]
        r_end = r[0] + r[1]
        r_range = r[1]
        for m in mappings:
            m_to = m[0]
            m_start = m[1]
            m_range = m[2]
            m_end = m_start + m_range
            if r_start >= m_start and r_end <= m_end:
                transformed.append([r_start - m_start + m_to, r_range])
                flag = True
                break
            elif r_start < m_start and r_end > m_start and r_end <= m_end:
                transformed.append([m_to, r_end - m_start])
                ranges.append([r_start, m_start - r_start])
                flag = True
                break
            elif r_start >= m_start and r_start < m_end and r_end > m_end:
                transformed.append([m_to + r_start - m_start, m_end - r_start])
                ranges.append([m_end, r_end - m_end])
                flag = True
                break
            elif r_start < m_start and r_end > m_end:
                ranges.append([r_start, m_start - r_start])
                transformed.append([m_to, m_range])
                ranges.append([m_end, r_end - m_end])
                flag = True
                break
        if not flag:
            transformed.append(r)
    return transformed


new_seed_ranges = split_list(seeds, 2)
# new_seeds = set()
# for start, length in new_seed_ranges:
#     generated = [*range(start, start + length)]
#     new_seeds.update(generated)
# soil = [conversion(l, seed_to_soil) for l in new_seeds]
# fertilizer = [conversion(l, soil_to_fertilizer) for l in soil]
# water = [conversion(l, fertilizer_to_water) for l in fertilizer]
# light = [conversion(l, water_to_light) for l in water]
# temperature = [conversion(l, light_to_temperature) for l in light]
# humidity = [conversion(l, temperature_to_humidity) for l in temperature]
# location = [conversion(l, humidity_to_location) for l in humidity]
# print(new_seeds)
# print(soil)
# print(fertilizer)
# print(water)
# print(light)
# print(temperature)
# print(humidity)
# print(location)


soil = conversion_list(new_seed_ranges, seed_to_soil)
fertilizer = conversion_list(soil, soil_to_fertilizer)
water = conversion_list(fertilizer, fertilizer_to_water)
light = conversion_list(water, water_to_light)
temperature = conversion_list(light, light_to_temperature)
humidity = conversion_list(temperature, temperature_to_humidity)
location = conversion_list(humidity, humidity_to_location)
starting_locations = [x[0] for x in location]
# print(new_seed_ranges)
# print(soil)
# print(fertilizer)
# for i in range(len(fertilizer)):
# i = 26
# print(fertilizer[i : i + 1])
# j = 0
# print(fertilizer_to_water[j : j + 1])
# print(conversion_list(fertilizer[i : i + 1], fertilizer_to_water[j : j + 1]))
# print(fertilizer_to_water)
# print(water)
# print(light)
# print(temperature)
# print(humidity)
print(location)
# print(starting_locations)
print(min(starting_locations))

# soil = [conversion(l, seed_to_soil) for l in seeds]
# fertilizer = [conversion(l, soil_to_fertilizer) for l in soil]
# water = [conversion(l, fertilizer_to_water) for l in fertilizer]
# light = [conversion(l, water_to_light) for l in water]
# temperature = [conversion(l, light_to_temperature) for l in light]
# humidity = [conversion(l, temperature_to_humidity) for l in temperature]
# location = [conversion(l, humidity_to_location) for l in humidity]

# # print(new_seeds)
# print(soil)
# # print(fertilizer)
# # print(water)
# # print(light)
# # print(temperature)
# # print(humidity)
# print(location)
# print(min(location))
