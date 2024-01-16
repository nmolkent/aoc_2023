# initial thoughts, the problem can be reduced to a min max problem, 0 - min_time_to_win, winners_time - max time to win
import re

def wins(start_time, max_time, dist_gt):
    # assume zero condition is impossible
    # max_time condition might be possible
    time_remaining = max_time - start_time
    distance = start_time * time_remaining # speed * time_remaining
    if distance > dist_gt:
        return 1
    return 0

def solve(filename):
    race_map = {}
    with open(filename) as file:
        for line in file:
            key, vals = tuple(re.split(": ", line.strip()))
            race_map[key.strip()] = re.split("\\s+", vals.strip())
    prod = 1 
    for i, max_time in enumerate(race_map["Time"]):
        distance_to_beat = int(race_map["Distance"][i])
        prod *= sum([wins(j, int(max_time), distance_to_beat) for j in range(0, int(max_time))])
    return prod

if __name__ == "__main__":
    solve("test1.txt")