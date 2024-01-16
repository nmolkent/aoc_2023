# recursion makes this quite clean and simple enough to understand
# the stopping condition is when the sum of all numbers in the list is 0
# the recursion condition changes for each challenge
def diff_check(l: list):
    if sum(l) == 0:
        return 0
    # to get the next number take the last number of the list only and add the results of diff checker
    return l[-1] + diff_check([l[i+1] - l[i] for i in range(len(l)-1)])

def solve(filename):
    with open(filename) as file:
        result = sum([diff_check([int(s) for s in line.strip().split(" ")]) for line in file])
    return result

if __name__ == "__main__":
    solve("test1.txt")