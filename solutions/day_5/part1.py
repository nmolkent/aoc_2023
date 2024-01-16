# the trees dictionary stores transformation name: [initial seeds]
# the first line gives an initial list which we copy into the next
# the coppied lst is mutable and has the relevant transformations applied
def solve(filename):
    trees = {}
    src_name, dest_name = None, None
    initial_seed_no = 0

    with open(filename) as file:
        for line in file:
            if len(line.strip()) == 0:
                pass
            elif line[0:len("seeds: ")] == "seeds: ":
                trees["seed"] = [int(i) for i in line[len("seeds: "):].split(" ")]
                initial_seed_no = len(trees["seed"])
            elif not line[0].isdigit():
                src_name, dest_name = tuple(line.split(" ")[0].split("-to-"))
                trees[dest_name] = trees[src_name].copy()
            else:
                dest, start, length = tuple(map(int, line.split(" ")))
                for i in range(initial_seed_no):
                    if trees[src_name][i] >= start and trees[src_name][i] < start + length:
                        trees[dest_name][i] = dest + (trees[src_name][i] - start)
    return min(trees["location"])

    if __name__ == "__main__":
        solve("test1.txt")
