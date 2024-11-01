import functools

file = open("day12.txt", "r")
lines = file.readlines()
records = [line.split()[0] for line in lines]
configs = [tuple([int(num) for num in line.split()[1].split(',')]) for line in lines]

new_records = ["?".join([record]*5)for record in records]
new_configs = [config * 5 for config in configs]

@functools.cache
def alternative(record, remaining):
    if not remaining:
        if "#" in record:
            return 0
        else:
            return 1
    if not len(record):
        return 0
    current_chain = remaining[0]
    last_chain = len(remaining) == 1
    if len(record) < current_chain:
        return 0
    current_fountain = record[0]

    @functools.cache
    def dot(r, c):
        return alternative(r[1:], c)
    
    @functools.cache
    def pound(r, c, last, length):
        if "." in r[:length]:
            return 0
        elif last:
            return alternative(r[length:], c[1:])
        elif len(r) > length and r[length] != "#":
            return alternative(r[length + 1:], c[1:])
        else:
            return 0
        
    if current_fountain == ".":
        return dot(record, remaining)
    elif current_fountain == "#":
        return pound(record, remaining, last_chain, current_chain)
    else:
        dots = dot(record, remaining)
        pounds = pound(record, remaining, last_chain, current_chain)
        return dots + pounds


@functools.cache
def solver(record, remaining, connected):
    if not record:
        if len(remaining) > 1 or (len(remaining) and remaining[0] > 0):
            return []
        return [""]
    current_fountain = record[0]

    if not len(remaining):
        if current_fountain == "#":
            return []
        remaining = solver(record[1:], remaining, False)
        return [f".{f}" for f in remaining]
    
    current_chain = remaining[0]
    remaining_chains = remaining[1:]

    if connected:
        # must be broken to break chain
        if current_chain == 0:
            if current_fountain == "#":
                return []
            return [f".{f}" for f in solver(record[1:], remaining_chains, False)]

        # must be working to continue the chain
        else:
            if current_fountain == ".":
                return []
            return [f"#{f}" for f in solver(record[1:], tuple([current_chain - 1, *remaining_chains]), True)]
        
    else:
        # if not connected, current_chain can't be 0
        current_working = [f"#{f}" for f in solver(record[1:], tuple([current_chain - 1, *remaining_chains]), True)]
        current_broken = [f".{f}" for f in solver(record[1:], tuple([current_chain, *remaining_chains]), False)]
        if current_fountain == "#":
            return current_working
        elif current_fountain == ".":
            return current_broken
        else:
            return current_working + current_broken
        
@functools.cache
def solver_num_only(record, remaining, connected):
    if not record:
        if len(remaining) > 1 or (len(remaining) and remaining[0] > 0):
            return 0
        return 1
    current_fountain = record[0]

    if not len(remaining):
        if current_fountain == "#":
            return 0
        return solver_num_only(record[1:], remaining, False)
        
    
    current_chain = remaining[0]
    remaining_chains = remaining[1:]

    if connected:
        # must be broken to break chain
        if current_chain == 0:
            if current_fountain == "#":
                return 0
            return solver_num_only(record[1:], remaining_chains, False)

        # must be working to continue the chain
        else:
            if current_fountain == ".":
                return 0
            return solver_num_only(record[1:], tuple([current_chain - 1, *remaining_chains]), True)
        
    else:
        # if not connected, current_chain can't be 0
        current_working = solver_num_only(record[1:], tuple([current_chain - 1, *remaining_chains]), True)
        current_broken = solver_num_only(record[1:], tuple([current_chain, *remaining_chains]), False)
        if current_fountain == "#":
            return current_working
        elif current_fountain == ".":
            return current_broken
        else:
            return current_working + current_broken

for i in range(len(records)):
    calc_valid = solver_num_only(records[i], configs[i], False)
    new_calc_valid = alternative(records[i], configs[i])
    # print(calc_valid, new_calc_valid)
    if calc_valid != new_calc_valid:
        print("ahhhhh")

# sum = 0
# for i in range(len(records)):
#     num_valid = len(solver(records[i], configs[i], False))
#     calc_valid = solver_num_only(records[i], configs[i], False)
#     print(solver(records[i], configs[i], False))

# new_sum = 0
# for i in range(len(new_records)):
#     calc_valid = solver_num_only(new_records[i], new_configs[i], False)
#     new_sum += calc_valid
# print(new_sum)

