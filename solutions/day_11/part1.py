
def solve(filename):
    in_array = []
    with open(filename) as file:
        for line in file:
            in_array.append(line)
            if "#" not in line:
                in_array.append(line)

    galaxy_coordinates = set()

    extra_rows = 0
    for j in range(len(in_array[0])):
        add_row = 1
        for i in range(len(in_array)):
            if in_array[i][j] == "#":
                add_row = 0
                galaxy_coordinates.add((i, j + extra_rows))
        extra_rows += add_row

    total = 0
    while len(galaxy_coordinates) > 0:
        i1, j1 = galaxy_coordinates.pop()
        for i2, j2 in galaxy_coordinates:
            total += abs(i1 - i2) + abs(j1 - j2)
    return total

if __name__ == "__main__":
    solve("test1.txt")
