file = open("day20.txt", "r")
lines = file.readlines()

from collections import defaultdict, deque

import math

class FlipFlop:
    def __init__(self, name, destinations):
        self.state = False
        self.name = name
        self.destinations = destinations

    def process(self, source, pulse):
        output = []
        if pulse:
            return output
        
        if self.state:
            self.state = False
            for d in self.destinations:
                output.append((self.name, False, d))
        else:
            self.state = True
            for d in self.destinations:
                output.append((self.name, True, d))
        return output
    
class Conjunction:
    def __init__(self, name, destinations = []):
        self.sources = {}
        self.name = name
        self.destinations = destinations

    def add_destination(self, destination):
        if destination not in self.destinations:
            self.destinations.append(destination)

    def add_source(self, source):
        if source not in self.sources:
            self.sources[source] = False

    def process(self, source, pulse):
        self.sources[source] = pulse
        output_pulse = not all(self.sources.values())
        return [(self.name, output_pulse, d) for d in self.destinations]

class Broadcast:
    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations

    def process(self, source, pulse):
        return [(self.name, pulse, d) for d in self.destinations]
    
def initialize_converters(instructions, parts):
    for i in instructions:
        o, ds = i.split("->")
        origin = o.strip()
        destinations = ds.strip()

        if origin[0] != '&':
            continue

        destinations_cleaned = []
        for d in destinations.split(","):
            destinations_cleaned.append(d.strip())
        parts[origin[1:]] = Conjunction(origin[1:], destinations_cleaned)
    return parts

def initialize_others(instructions, parts):
    for i in instructions:
        o, ds = i.split("->")
        origin = o.strip()
        destinations = ds.strip()

        destinations_cleaned = []
        for d in destinations.split(","):
            destinations_cleaned.append(d.strip())
        for d in destinations_cleaned:
            if d in parts and isinstance(parts[d], Conjunction):
                parts[d].add_source(origin if origin[0] not in ['%', "&"] else origin[1:])
        if origin[0] == "%":
            parts[origin[1:]] = FlipFlop(origin[1:], destinations_cleaned)
        if origin == "broadcaster":
            parts[origin] = Broadcast(origin, destinations_cleaned)
    return parts    


def bfs(q: deque, parts):
    pulses = []
    while q:
        source, pulse, destination = q.popleft()
        pulses.append((source, pulse, destination))
        if destination not in parts:
            continue
        element = parts[destination]
        results = element.process(source, pulse)
        q.extend(results)
    return tuple(pulses)


def count_pulses(pulses):
    signals = [p[1] for p in pulses]
    return (signals.count(False), signals.count(True))


def repeat(q, parts, times = 1000):    
    total_lows = 0
    total_highs = 0
    for i in range(times):
        q.append(("button", False, "broadcaster"))
        pulses = bfs(q, parts)
        a, b = count_pulses(pulses)
        total_lows += a
        total_highs += b
    return total_lows * total_highs


def part1():
    parts = {}
    parts = initialize_converters(lines, parts)
    parts = initialize_others(lines, parts)
    queue = deque()
    return repeat(queue, parts)
    
print(part1())



def find_period(q, parts, source, destination):
    occurences = []
    for i in range(1, 100000):
        q.append(("button", False, "broadcaster"))
        pulses = bfs(q, parts)
        if (source, True, destination) in pulses:
            occurences.append(i)
        if len(occurences) >= 2:
            print(occurences)
            break
    return (occurences[0], occurences[1] - occurences[0])
        



def helper(source, destination):
    parts = {}
    parts = initialize_converters(lines, parts)
    parts = initialize_others(lines, parts)
    queue = deque()
    return find_period(queue, parts, source, destination)

def part2():

    a = helper("fm", "vr")
    b = helper("dk", "vr")
    c = helper("fg", "vr")
    d = helper("pq", "vr")
    print(a, b, c, d)
    sol = math.lcm(a[1], b[1], c[1], d[1])
    for e in [a, b, c, d]:
        t = sol - e[0]
        print(t)
        print(t % e[1])
    return sol
print(part2())



