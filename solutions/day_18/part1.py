from utils.pathfinder import Pos, Compass


compass_dirction = {
    "R": Compass.East,
    "U": Compass.North,
    "L": Compass.West,
    "D": Compass.South
}

def parse_line(direction: str, intensity: str, colour: str):
    return (compass_dirction[direction], int(intensity), colour[1:-1])

def show(limits, visited):
    for i in range(limits.row):
        for j in range(limits.col):
            if Pos(i, j) in visited:
                print("#", end="")
            else:
                print(".", end="")
        print()
            

def get_area(limits: Pos, visited: dict[Pos, tuple[tuple[Compass, int], tuple[Compass, int]]]):
    # find corner
    top_left = min(visited.keys(), key=lambda x: x.col + x.row*(5**16))
    print(limits)
    print(top_left)


    travelling = Compass.South
    orientation = Compass.South

    this_pos = top_left
    first_pair = visited[this_pos]
    forward_idx = 0 if first_pair[0][0] == travelling else 1
    total = 0

    while True:
        forward_dir, forward_intensity = visited[this_pos][forward_idx]
        reverse_dir, reverse_intensity = visited[this_pos][int(not forward_idx)]

        next_pos = forward_dir.of_pos(this_pos, forward_intensity)

        # anti clovckwise
        if forward_dir == Compass.South and reverse_dir == Compass.East:
            total -= this_pos.col * (forward_intensity + 1)
        elif forward_dir == Compass.East and reverse_dir == Compass.North:
            total += 0
        elif forward_dir == Compass.North and reverse_dir == Compass.West:
            total += (this_pos.col + 1) * (forward_intensity + 1)
        elif forward_dir == Compass.West and reverse_dir == Compass.South:
            total += 0
        # clockwise
        elif forward_dir == Compass.South and reverse_dir == Compass.West:
            total -= (this_pos.col) * (forward_intensity)
        elif forward_dir == Compass.East and reverse_dir == Compass.South:
            total -= (this_pos.col + 1)
        elif forward_dir == Compass.North and reverse_dir == Compass.East:
            total += (this_pos.col + 1) * (forward_intensity)
        elif forward_dir == Compass.West and reverse_dir == Compass.North:
            total += this_pos.col
        else:
            raise Exception(f"move: {forward_dir}, {reverse_dir} should be illegal")
        
        
        print(reverse_dir, forward_dir, this_pos, forward_intensity, total)

        if next_pos == top_left:
            return total
        this_pos = next_pos

def solve(filename: str):
    lead_pos = Pos(0, 0)
    visited: dict[Pos, tuple[Compass, int]] = {}
    reversed: dict[Pos, tuple[Compass, int]] = {}
    with open(filename) as file:
        for line in file:
            direction, intensity, colour = parse_line(*line.strip().split(" "))
            visited[lead_pos] = (direction, intensity)
            lead_pos = direction.of_pos(lead_pos, intensity)       
            reversed[lead_pos] = (direction.flip(), intensity)
    reversed[Pos(0, 0)] = (direction.flip(), intensity)
    paired = {}
    # realign positions to zero
    shift_pos = Pos(
        -min(visited.keys(), key=lambda x: x.row).row,
        -min(visited.keys(), key=lambda x: x.col).col
    )
    limit_pos = Pos(
        shift_pos.row + max(visited.keys(), key=lambda x: x.row).row + 1,
        shift_pos.col + max(visited.keys(), key=lambda x: x.col).col + 1
    )

    for k, v in reversed.items():
        paired[k.move(shift_pos)] = (v, visited[k])

    # show(limit_pos, set(paired.keys()))
    result = get_area(limit_pos, paired)
    return result

if __name__ == "__main__":
    solve("test1.txt")
