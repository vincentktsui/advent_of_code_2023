import math
from collections import defaultdict

file = open("day4.txt", "r")
lines = file.readlines()
cleaned = [line.strip().split(":")[1].strip() for line in lines]

points = []
cards = defaultdict(int)
for i, card in enumerate(cleaned):
    cards[i] += 1
    owned, winning = card.split("|")
    owned = owned.strip()
    winning = winning.strip()
    owned = owned.split()
    winning = winning.split()

    matching = [x for x in owned if x in winning]
    matches = len(matching)
    for x in range(i + 1, i + matches + 1):
        cards[x] += cards[i]
print(cards)
print(sum(cards.values()))


# points = []
# for card in cleaned:
#     owned, winning = card.split("|")
#     owned = owned.strip()
#     winning = winning.strip()
#     owned = owned.split()
#     winning = winning.split()

#     matching = [x for x in owned if x in winning]
#     matches = len(matching)
#     if matches == 0:
#         points.append(0)
#     else:
#         points.append(int(math.pow(2, matches - 1)))
# print(sum(points))
