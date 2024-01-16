
def solve(filename):
    number_list = []
    symbols = set()  
    # use set because we will check for neighbors identity in symbols
    with open(filename) as file:
        arr = [line.strip() for line in file]
    # read into array and we can index strings as though this was a 2d array
    # this way we can efficiently index the array at a constant time

    # first loop to set up data structures
    for i, row in enumerate(arr):
        number_xys = []
        for j, char in enumerate(row):
            # if the last coordinate has a y value 1 less than the current y value it is subsequent and should be treated as part of the same number
            if char.isdigit() and (len(number_xys) == 0 or number_xys[-1][1] + 1 == j):
                number_xys.append((i, j))
            # we should treat as a new number
            elif char.isdigit():
                number_list.append(number_xys.copy())
                number_xys = [(i, j)]
            # rather than list the symbls we assume anything other than a . or digit is a symbol
            elif char != ".":
                symbols.add((i, j))
        # it's possible no numbers were found
        if len(number_xys) > 0:
            number_list.append(number_xys)

    total = 0
    # sum of only numbers adjacent to symbols/parts
    # second loop to use data structures to calculate appropriate sum
    for n in number_list:
        for pos in n:
            part_adjacent = False
            for i in range(pos[0] - 1, pos[0] + 2):
                for j in range(pos[1] - 1, pos[1] + 2):
                    if (i, j) in symbols:
                        part_adjacent = True
            if part_adjacent:
                total += int("".join([arr[i][j] for i, j in n]))
                break
    return total

if __name__ == "__main__":
    solve("test1.txt")
