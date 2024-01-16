from math import prod

def solve(filename):
    number_list = []
    gears = dict()
    # only interested in numbers touching gears, 
    # each gear wil be a tuple(int, int) key and list[int] values

    with open(filename) as file:
        arr = [line.strip() for line in file]
    max_idx = height, width = (len(arr), len(arr[0]))

    for i, row in enumerate(arr):
        number = []
        for j, char in enumerate(row):
            # if the last coordinate has a y value 1 less than the current y value it is subsequent and should be treated as part of the same number
            if char.isdigit() and (len(number) == 0 or number[-1][1] + 1 == j):
                number.append((i, j))
            # we should treat as a new number
            elif char.isdigit():
                number_list.append(number.copy())
                number = [(i, j)]
            # we are only interested in gear symbols, initialise the dict at this position with empty list
            elif char == "*":
                gears[(i, j)] = []
        # it's possible no numbers were found
        if len(number) > 0:
            number_list.append(number)

    # check if gear is neighbour and if so add the number to the gear list
    # assume numbers dont touch more than 1 gear
    for n in number_list:
        gear_factor = None
        for pos in n:
            for i in range(pos[0] - 1, pos[0] + 2):
                for j in range(pos[1] - 1, pos[1] + 2):
                    if (i, j) in gears:
                        gear_factor = (i, j)
                        break
        if gear_factor is not None:
            gears[gear_factor].append(int("".join([arr[i][j] for i, j in n])))

    # gears only multiply when they connect  more than 1 number
    sum_prod = 0
    for nums in gears.values():
        if len(nums) > 1:
            sum_prod += prod(nums)
    return sum_prod

if __name__ == "__main__":
    solve("test1.txt")

