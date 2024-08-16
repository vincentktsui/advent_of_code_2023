import math

file = open("day2.txt", "r")
lines = file.readlines()
cleaned = [line.strip() for line in lines]
reference = {"red": 12, "green": 13, "blue": 14}
games = []
for line in cleaned:
    game = line.split(":")[1].strip()
    all_records = [record.strip() for record in game.split(";")]
    temp = {}
    for record in all_records:
        counts = [color.strip() for color in record.split(",")]
        for count in counts:
            amount, color = count.split(" ")
            temp[color] = max(temp.get(color, 0), int(amount))
    games.append(temp)
powers = []
for game in games:
    power = math.prod(game.values())
    powers.append(power)
print(sum(powers))
# sum = 0
# viable_games = {}
# for i, game in enumerate(games):
#     valid = all([amount <= reference[color] for color, amount in game.items()])
#     if valid:
#         sum += i + 1
#         viable_games[i + 1] = game
# print(viable_games)
# print(viable_games.keys())
# print(sum)
