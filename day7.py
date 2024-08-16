import math
from collections import defaultdict

file = open("day7.txt", "r")
lines = file.readlines()
cleaned = [line.strip() for line in lines]
print(cleaned)
hands = {}
for x in cleaned:
    temp = x.split()
    hands[temp[0]] = temp[1]


# def find_hand(hand):
#     counts = defaultdict(int)
#     for card in hand:
#         counts[card] += 1
#     a = counts.values()
#     if 5 in a:
#         return 1
#     if 4 in a:
#         return 2
#     if 3 in a:
#         if 2 in a:
#             return 3
#         else:
#             return 4
#     if 2 in a:
#         if len(a) == 3:
#             return 5
#         else:
#             return 6
#     return 7


# mapping = {
#     "A": 1,
#     "K": 2,
#     "Q": 3,
#     "J": 4,
#     "T": 5,
#     "9": 6,
#     "8": 7,
#     "7": 8,
#     "6": 9,
#     "5": 10,
#     "4": 11,
#     "3": 12,
#     "2": 13,
# }

# 1 -> 5 of a kind
# 2 -> 4 of a kind
# 3 -> full house
# 4 -> 3 of a kind
# 5 -> 2 pair
# 6 -> pair
# 7 single


def find_hand(hand):
    counts = defaultdict(int)
    for card in hand:
        counts[card] += 1
    sorted_hand = dict(
        sorted(counts.items(), key=lambda item: (-item[1], mapping[item[0]]))
    )
    if "J" in sorted_hand.keys() and len(sorted_hand.keys()) > 1:
        temp = sorted_hand.pop("J")
        sorted_hand[next(iter(sorted_hand))] += temp
    a = sorted_hand.values()
    if 5 in a:
        return 1
    if 4 in a:
        return 2
    if 3 in a:
        if 2 in a:
            return 3
        else:
            return 4
    if 2 in a:
        if len(a) == 3:
            return 5
        else:
            return 6
    return 7


mapping = {
    "A": 1,
    "K": 2,
    "Q": 3,
    "T": 5,
    "9": 6,
    "8": 7,
    "7": 8,
    "6": 9,
    "5": 10,
    "4": 11,
    "3": 12,
    "2": 13,
    "J": 14,
}

for hand in hands.keys():
    print(find_hand(hand))

sorted_hands = sorted(
    hands.keys(),
    key=lambda x: (
        find_hand(x),
        mapping[x[0]],
        mapping[x[1]],
        mapping[x[2]],
        mapping[x[3]],
        mapping[x[4]],
    ),
)[::-1]

print(sorted_hands)
total = 0
for i, hand in enumerate(sorted_hands):
    total += (i + 1) * int(hands[hand])
print(total)
