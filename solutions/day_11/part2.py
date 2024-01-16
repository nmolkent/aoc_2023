from collections import defaultdict

# 

in_array = []

# untransformed col indexs: {base row: transformed row indexes}
columns = defaultdict(dict)
# in the base case the transformation factor should be 2 
# ie when doubling the space the transformation factor should be 2
# note for part 1 no multiplication performed 
# and if the expansion was 1 the transformation factor would be 0 (we want to add no space)

def solve(filename):
    transformation_factor = 1e6
    extra_rows = 0
    with open(filename) as file:
        for row_idx, line in enumerate(file):
            add_row = 1
            in_array.append(line)
            for col_idx, char in enumerate(line):
                if char == "#":
                    add_row = 0
                    columns[col_idx][row_idx] = row_idx + (extra_rows * (transformation_factor - 1))
            extra_rows += add_row
            

    galaxy_coordinates = set()
    extra_cols = 0
    for col_idx in range(len(in_array[0])):
        add_col = 1
        for row_idx in range(len(in_array)):
            if in_array[row_idx][col_idx] == "#":
                add_col = 0
                galaxy_coordinates.add((columns[col_idx][row_idx], col_idx + (extra_cols * (transformation_factor - 1))))
        extra_cols += add_col

    total = 0
    while len(galaxy_coordinates) > 0:
        i1, j1 = galaxy_coordinates.pop()
        for i2, j2 in galaxy_coordinates:
            total += (abs(i1 - i2) + abs(j1 - j2))
    return int(total)

if __name__ == "__main__":
    solve("test1.txt")

