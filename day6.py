import math

file = open("day6.txt", "r")
lines = file.readlines()
cleaned = [line.strip().split(":")[1].strip() for line in lines]
# times = [int(x) for x in cleaned[0].split()]
# distances = [int(x) for x in cleaned[1].split()]

# results = []
# for j, time in enumerate(times):
#     possibilities = []
#     # for i in range(1, time):
#     #     possibilities.append((time - i) * i)
#     end = int(time / 2) + 1 if time % 2 == 0 else math.ceil(time / 2)
#     for i in range(1, end):
#         temp = (time - i) * i
#         possibilities.append(temp)
#         if not i == time / 2 - 1:
#             possibilities.append(temp)
#     to_beat = distances[j]
#     winning = list(filter(lambda x: x >= to_beat, possibilities))
#     results.append(len(winning))
# print(results)
# print(math.prod(results))

time = int("".join(cleaned[0].split()))
distance = int("".join(cleaned[1].split()))

end = int(time / 2) + 1 if time % 2 == 0 else math.ceil(time / 2)


def binary_search(left, right):
    while left < right:
        print(left, right)
        middle = math.floor((left + right) / 2)
        if (middle * (time - middle)) < distance:
            if left == middle:
                left = middle + 1
            else:
                left = middle
        else:
            right = middle
    return left


lowest_over = binary_search(1, end)

if time % 2 == 0:
    print((end - lowest_over - 1) * 2 + 1)
else:
    print((end - lowest_over) * 2)
