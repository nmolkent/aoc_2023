from collections import defaultdict, deque
import operator
from typing import Callable

def parse_workflow(s: str):
    workflow_name, rules = tuple(s.strip()[:-1].split("{"))
    return workflow_name, rules

def parse_range(s: str, flipped=False):
    sn = s.split(":")[0][1]
    num = s.split(":")[0][2:]
    cmp = ">"
    if flipped:
        cmp = "<"
    if sn == cmp:
        return (int(num) + int(not flipped), 4000)
    else:
        return (1, int(num) - int(not flipped))


def solve(filename: str):
    workflows = {
        # name: rule 
    }
    xmas_ranges = {x: (1, 4000) for x in list("xmas")}
    parser = "workflows"
    result = 0
    with open(filename) as file:
        for line in file:
            if len(line.strip()) == 0:
                parser = "ratings"
            elif parser == "workflows":
                name, func = parse_workflow(line)
                workflows[name] = func

    workflow_inputs = deque([(["in"], [], [])])
    workflow_branches = []
    while len(workflow_inputs) > 0:
        path, doors, ranges= workflow_inputs.pop()
        last_node = path[-1]
        if path[-1] in ("A", "R"):
            if path[-1] == "R":
                workflow_branches.append((path, doors, ranges))
        else:
            options = workflows[last_node].split(",")
            collected_ranges = []
            collected_doors = []
            for o in options:
                if o.find(":") > 0:
                    collected_doors.append(o[0])
                    workflow_inputs.append((path + [o.split(":")[-1]], doors + collected_doors, ranges + collected_ranges + [parse_range(o)]))
                    collected_ranges.append(parse_range(o, flipped=True))
                else:
                    workflow_inputs.append((path + [o], doors + collected_doors, ranges + collected_ranges))
    
    total_combinations = 4000**4
    for b in workflow_branches:
        path, doors, ranges = b
        restricted_range = xmas_ranges.copy()
        for d, r in zip(doors, ranges):
            diff_range = restricted_range[d]
            restricted_range[d] = (max(r[0], diff_range[0]), min(r[1], diff_range[1]))
        prod = 1
        for x in restricted_range.values():
            prod *= x[1] - x[0] + 1
        total_combinations -= prod
    print(total_combinations)








if __name__ == "__main__":
    solve("test1.txt")
