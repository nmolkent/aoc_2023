from collections import defaultdict

def solve(filename):
    # reading into defaultdict simplifies the process of appending to lists we don't have to initialise
    arrs = defaultdict(list)
    i = 0
    with open(filename) as file:
        for line in file:
            if len(line.strip()) == 0:
                i += 1
            else:
                arrs[i].append(list(line.strip()))
    total = 0
    for a in arrs.values():
        total += find_reflection(a)
    return total

def mirror(arr, i, j, allowed_diffs=0, diffs=0):
    # using diffs as an accumulator we can both return early when diffs > than the allowed limit (see section 2)
    # and return diffs when the end condition is met (ie the indexed are about to go out of bounds)
    if i < 0 or j >= len(arr) or diffs > allowed_diffs:
        return diffs
    else:
        return mirror(arr, i - 1, j + 1, allowed_diffs,
            diffs + sum([int(x != y) for x, y in zip(arr[i], arr[j])])
        )
def find_reflection(arr, allowed_diffs=0):
    # 2 searches h = horizontal
    for i in range(len(arr) - 1):
        h_reflect = mirror(arr, i, i+1, allowed_diffs)
        if h_reflect == allowed_diffs:
            return (i+1)*100
    # v = vertical note the array is simply transposed so we can use the same mirror function for both
    for i in range(len(arr[0]) - 1):
        v_reflect = mirror(list(zip(*arr)), i, i+1, allowed_diffs)
        if v_reflect == allowed_diffs:
            return i+1

if __name__ == "__main__":
    solve("test1.txt")