from solutions.day_14.part1 import Direction
from solutions.day_16.part1 import Mirror, find_energised_tiles, show

def iterate_configs(arr_size, mirrors):
    largest = set()
    for d in Direction:
        for i in range(arr_size[d.pos_index()]):
            initial_pos = d.rebuild(i, d.flip().limit(arr_size[d.weight_index()]))
            new_result = find_energised_tiles(initial_pos, d, mirrors, arr_size)
            if len(new_result) > len(largest):
                largest = new_result
    return largest

def solve(filename: str):
    mirrors: dict[tuple[int, int], Mirror] = {}
    with open(filename) as file:
        for i, line in enumerate(file):
            for j, char in enumerate(line.strip()):
                if char != ".":
                    mirrors[(i, j)] = Mirror(char, (i, j))
    arr_size: tuple[int, int] = (i+1, j+1)
    x = iterate_configs(arr_size, mirrors)
    return len(x)

if __name__ == "__main__":
    solve("test1.txt")
