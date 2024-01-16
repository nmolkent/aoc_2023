# we can reduce the problem space by using gradient descent , im sure theres a precise maths way to do this but
# I'm not gunna teach myself differential math on a work day
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
   
        for i, line in enumerate(file):
            key, vals = tuple(re.split(": ", line.strip()))
            race_map[key.strip()] = int("".join([char for char in vals if char != " "]))

    # here we do gradient descent
    start_pos, end_pos = 1, race_map["Distance"]

    first_win, last_win = None, None

    # step size should
    step_size = end_pos // 10**(len(str(end_pos))-1)

    for i in range(1000): # 1000 iterations should be more than enough
        # look for the first win
        while start_pos < end_pos and not wins(start_pos, race_map["Time"], race_map["Distance"]):
            start_pos += step_size
        # reverse after win or reach limit and reduce step size
        start_pos -= step_size
        step_size//=2
        if step_size == 1:
            while not wins(start_pos, race_map["Time"], race_map["Distance"]):
                start_pos += step_size
            first_win = start_pos
            break
        if start_pos > race_map["Time"]:
            raise Exception("first win not found!")

    # reset step size, it's now at most as big as the distance less the first win
    step_size = end_pos - first_win

    for i in range(1000):
        # look for the last win
        while wins(start_pos, race_map["Time"], race_map["Distance"]):
            start_pos += step_size
        start_pos -= step_size
        step_size//=2
        if step_size == 1:
            while wins(start_pos, race_map["Time"], race_map["Distance"]):
                start_pos += step_size
            last_win = start_pos
            break
        if start_pos > race_map["Time"]:
            print("warn, end not found")
            end_pos = race_map["Distance"]
    return last_win-first_win
    

if __name__ == "__main__":
    solve("test1.txt")  
