import operator
from typing import Callable

def workflow_combinator(rules: str):
    if len(rules) == 0:
        raise Exception("rules is an empty str")
    elif rules.find(",") == -1:
        return lambda x, y: rules if rules in ["A", "R"] else y[rules](x, y)
    else:
        this, that = rules[:rules.find(",")], rules[rules.find(",")+1:]
        question, response = this.split(":")
        xmas_category = question[0]
        op = operator.lt if question[1] == "<" else operator.gt
        number = int(question[2:])
        return lambda x, y: response if response in ["A", "R"] and op(x[xmas_category], number) else y[response](x, y) if op(x[xmas_category], number) else workflow_combinator(that)(x, y)


def parse_workflow(s: str)->tuple[str, Callable]:
    workflow_name, rules = tuple(s.strip()[:-1].split("{"))
    return workflow_name, workflow_combinator(rules)

def parse_xmas_rating(s: str):
    rating = {}
    for kv in s.strip()[1:-1].split(","):
        k, v = tuple(kv.split("="))
        rating[k] = int(v)
    return rating


def solve(filename: str):
    workflows = {
        # name: rule func
    }
    parser = "workflows"
    result = 0
    with open(filename) as file:
        for line in file:
            if len(line.strip()) == 0:
                parser = "ratings"
            elif parser == "workflows":
                name, func = parse_workflow(line)
                workflows[name] = func
            else:
                xmas_rating = parse_xmas_rating(line)
                workflow_result = workflows["in"](xmas_rating, workflows)
                if workflow_result == "A":
                    result += sum(xmas_rating.values())
    return result

if __name__ == "__main__":
    solve("test1.txt")
