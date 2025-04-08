file = open("day19.txt", "r")
lines = file.readlines()

from collections import defaultdict

workflows = []
parts = []

part2 = False
for line in lines:
    if line.strip() == "":
        part2 = True
        continue
    if part2:
        parts.append(line.strip())
    else:
        workflows.append(line.strip())


def parse_workflows(workflows):
    workflow_rules = {}
    for workflow in workflows:
        name, rule_seq = workflow.split("{")
        rules = rule_seq.replace("}", "").split(",")
        workflow_rules[name] = rules
    return workflow_rules

def parse_parts(parts):
    parsed_parts = []
    for part in parts:
        ratings = part.replace("{","").replace("}","").split(",")
        part_ratings = {}
        for rating in ratings:
            rating_name, score = rating.split("=")
            part_ratings[rating_name] = int(score)
        parsed_parts.append(part_ratings)
    return parsed_parts


def process_rule_block(part: dict[str, int], block: str):
    if ":" not in block:
        return block
    condition, result = block.split(":")
    if "<" in condition:
        part_name, score = condition.split("<")
        if part[part_name] < int(score):
            return result
        else:
            return None
    if ">" in condition:
        part_name, score = condition.split(">")
        if part[part_name] > int(score):
            return result
        else:
            return None
        
def process_rule_sequence(part: dict[str, int], seq: list[str]):
    for block in seq:
        result = process_rule_block(part, block)
        if result:
            return result

def process_part(part, rules):
    current_rule = "in"
    rule_sequences = [current_rule]
    while current_rule:
        rule = rules[current_rule]
        current_rule = process_rule_sequence(part, rule)
        rule_sequences.append(current_rule)
        if current_rule in ["A", "R"]:
            return rule_sequences



def part1(parts, workflows):
    rules = parse_workflows(workflows)
    parsed_parts = parse_parts(parts)
    results = []
    accepted_parts = []
    for part in parsed_parts:
        result = process_part(part, rules)
        results.append(result)
        if "A" in result:
            accepted_parts.append(part)
    rating = 0
    for part in accepted_parts:
        for score in part.values():
            rating += score
    return rating
print(part1(parts, workflows))

def build_graph(workflows):
    graph = defaultdict(list)
    for node, edges in workflows.items():
        negation = []
        for edge in edges:
            if ":" not in edge:
                graph[node].append((edge,[*negation]))
                break
            else:
                condition, result = edge.split(":")
                graph[node].append((result, [*negation, condition]))
                if "<" in condition:
                    part_name, score = condition.split("<")
                    negation.append(f"{part_name}>{int(score)-1}")
                elif ">" in condition:
                    part_name, score = condition.split(">")
                    negation.append(f"{part_name}<{int(score)+1}")
    return graph



def dfs(graph, start, end, path = []):
    path.append(start)
    if start[0] == end:
        yield path
    else:
        for neighbor, condition in graph.get(start[0], []):
            if not any(neighbor == edge[0] for edge in path):
                yield from dfs(graph, (neighbor, condition), end, path.copy())
    path.pop()

def build_set(path):
    rule_set = []
    for step in path:
        conditions = step[1]
        for c in conditions:
            rule_set.append(c)
    return rule_set

def intersect_intervals(intervals):
    """
    This function takes a list of intervals (each represented as a tuple of (start, end))
    and returns the intersection of all the intervals, or an empty list if there is no common intersection.
    """
    # Start with the first interval as the initial "intersection"
    if not intervals:
        return []

    # Initialize the intersection range with the first interval
    intersection_start, intersection_end = intervals[0]

    # Iterate over the remaining intervals and find the intersection
    for interval in intervals[1:]:
        start, end = interval

        # Update the intersection range
        intersection_start = max(intersection_start, start)
        intersection_end = min(intersection_end, end)

        # If there's no intersection, return an empty list
        if intersection_start > intersection_end:
            return []

    # Return the final intersection interval
    return [(intersection_start, intersection_end)]


def get_intervals_for_rule_set(rule_set):
    """Convert a rule set into a list of intervals for s, a, x, m."""
    s_intervals = []
    a_intervals = []
    x_intervals = []
    m_intervals = []

    for rule in rule_set:
        variable = rule[0]
        operator = rule[1]
        value = int(rule[2:])

        s_intervals.append((1, 4000))
        a_intervals.append((1, 4000))
        x_intervals.append((1, 4000))
        m_intervals.append((1, 4000))

        if variable == 's':
            if operator == '<':
                s_intervals.append((1, value - 1))  # s < value
            elif operator == '>':
                s_intervals.append((value + 1, 4000))  # s > value
        elif variable == 'a':
            if operator == '<':
                a_intervals.append((1, value - 1))  # a < value
            elif operator == '>':
                a_intervals.append((value + 1, 4000))  # a > value
        elif variable == 'x':
            if operator == '<':
                x_intervals.append((1, value - 1))  # x < value
            elif operator == '>':
                x_intervals.append((value + 1, 4000))  # x > value
        elif variable == 'm':
            if operator == '<':
                m_intervals.append((1, value - 1))  # m < value
            elif operator == '>':
                m_intervals.append((value + 1, 4000))  # m > value

    # Merge intervals for each variable
    s_intervals = intersect_intervals(s_intervals)
    a_intervals = intersect_intervals(a_intervals)
    x_intervals = intersect_intervals(x_intervals)
    m_intervals = intersect_intervals(m_intervals)

    return s_intervals, a_intervals, x_intervals, m_intervals


def calculate_combinations(interval):
    total = 1
    for var in interval:
        c = 0
        for r in var:
            c += r[1] - r[0] + 1
        total *= c
    return total

    
def part2(workflows):
    rules = parse_workflows(workflows)
    graph = build_graph(rules)
    paths = dfs(graph, ("in", []), "A")
    total = 0
    for path in paths:
        rule_set = build_set(path)
        t = get_intervals_for_rule_set(rule_set)
        total += calculate_combinations(t)
    return total
print(part2(workflows))