from itertools import combinations
from functools import cache

def solve(filename: str):
    total = 0
    with open(filename) as file:
        for line in file:
            springs, broken_str = tuple(line.split(" "))
            broken = tuple(map(int, broken_str.split(",")))
            total += recursive_combinations(broken, springs)
    return total

@cache
def recursive_combinations(lengths, springs):
    if len(lengths) == 0:
        if "#" in springs:
            # used all options but things left to fix
            return 0
        else:
            # this is a valid option
            return 1
    elif len(springs) == lengths[0]:
        if "." not in springs and len(lengths) == 1:
            # this is a valid final option 
            return 1
        else:
            return 0
    elif (len(springs) < sum(lengths)):
        # terminate early as unable to use all options beffore end
        return 0       
    elif springs[:lengths[0]].startswith("#"):
        if "." in springs[:lengths[0]]:
            # terminate early as damaged spring and fixed spring intefere with consecuitivity condition
            return 0
        elif len(springs) >= sum(lengths) + 1 and springs[lengths[0]] == "#":
            # terminate early as damaged spring and fixed spring intefere with consecuitivity condition
            return 0
        else:
            # this must only be a match and not a skip
            return recursive_combinations(
                lengths[1:], springs[lengths[0]+1:]
            )
    elif "." not in springs[:lengths[0]]:
        # all options at the start are ? and consecutively ? or # and we don't break the consecuitivy condition
        if len(springs) >= sum(lengths) + 1 and springs[lengths[0]] == "#":
            # we should skip because the consecuitivity condition
            return recursive_combinations(
                lengths, springs[1:]
            ) 
        else:
            # we must skip and add simultaneously
            return recursive_combinations(
                lengths, springs[1:]
            ) + recursive_combinations(
                lengths[1:], springs[lengths[0]+1:]
            )
    else:
        # skip as unable to meet consecuitivity condition
        return recursive_combinations(
            lengths, springs[1:]
        )
    
def recursive_combinations_debug(lengths, springs, acc=""):
    if len(lengths) == 0:
        if "#" in springs:
            # used all options but things left to fix
            return []
        else:
            # this is a valid option
            return [acc + springs]
    elif len(springs) == lengths[0]:
        if "." not in springs and len(lengths) == 1:
            # this is a valid final option 
            return [acc + springs]
        else:
            return []
    elif (len(springs) < sum(lengths)):
        # terminate early as unable to use all options beffore end
        return []      
    elif springs[:lengths[0]].startswith("#"):
        if "." in springs[:lengths[0]]:
            # terminate early as damaged spring and fixed spring intefere with consecuitivity condition
            return []
        elif len(springs) >= sum(lengths) + 1 and springs[lengths[0]] == "#":
            # terminate early as damaged spring and fixed spring intefere with consecuitivity condition
            return []
        else:
            # this must only be a match and not a skip
            return recursive_combinations(
                lengths[1:], springs[lengths[0]+1:], acc + "#"*lengths[0] + "."
            )
    elif "." not in springs[:lengths[0]]:
        # all options at the start are ? and consecutively ? or # and we don't break the consecuitivy condition
        if len(springs) >= sum(lengths) + 1 and springs[lengths[0]] == "#":
            # we should skip because the consecuitivity condition
            return recursive_combinations(
                lengths, springs[1:], acc + "."
            ) 
        else:
            # we must skip and add simultaneously
            return recursive_combinations(
                lengths, springs[1:], acc + "."
            ) + recursive_combinations(
                lengths[1:], springs[lengths[0]+1:], acc + "#"*lengths[0] + ".", debug=debug
            )
    else:
        # skip as unable to meet consecuitivity condition
        return recursive_combinations(
            lengths, springs[1:], acc + ".",
        )


def in_index_ranges(idx: int, indicies: list[(int, int)])->bool:
    return any([idx >= start and idx < end for start, end in indicies])

def is_valid(indicies:list[(int, int)], springs: str):
    for spring_idx, c in enumerate(springs):
        if c == "." and in_index_ranges(spring_idx, indicies):
            return False
        if c == "#" and not in_index_ranges(spring_idx, indicies):
            return False
    return True

def to_string(indicies: list[(int, int)], springs: str):
    return "".join(["#" if in_index_ranges(i, indicies) else "." for i in range(len(springs))])

def new_positions(lengths: list[int], idx_adjustments: list[int]):
    # taking a list of lengths and the adjustments return tuple ranges (start, excludes[end])
    blocked = 0
    for l, adjustment in zip(lengths, idx_adjustments):
        yield (blocked+adjustment, blocked + l + adjustment)
        blocked += l

def get_combinations(springs, broken):
    # range increments is the min to max possible values that would be accepted by
    # new_positions idx adjustments
    range_increments = list(range(len(springs) + 1 - sum(broken)))
    for c in combinations(range_increments, len(broken)):
        # each combination created represents the index adjustments required to transform the 
        # intervals of broken pipes into solutions that can be checked
        nw = tuple(new_positions(broken, c))
        if is_valid(nw, springs):
            yield to_string(nw, springs)

if __name__ == "__main__":
    solve("test1.txt")