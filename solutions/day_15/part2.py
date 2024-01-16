from collections import defaultdict
from solutions.day_15.part1 import lens_hash

hash_store = defaultdict(list)
def hash_map(s: str):
    if "=" in s:
        add(*s.split("="))
    elif "-" in s:
        rm(s.split("-")[0])

def add(lable, focal_length):
    global hash_store
    i = 0
    found = False
    for l, f in hash_store[lens_hash(lable)]:
        if l == lable:
            hash_store[lens_hash(lable)][i] = (lable, focal_length)
            found = True
            break
        i += 1
    if not found:
        hash_store[lens_hash(lable)].append((lable, focal_length))
    
def rm(lable):
    global hash_store
    for l, f in hash_store[lens_hash(lable)]:
        if l == lable:
            hash_store[lens_hash(lable)].remove((lable, f))
            break

def solve(filename: str):
    global hash_store
    total = 0
    with open(filename) as file:
        for line in file:
            for s in line.strip().split(","):
                hash_map(s)
    total = 0
    for box, pairs in hash_store.items():
        for i, p in enumerate(pairs, start=1):
            total += (box+1) * i * int(p[1])
    return total


if __name__ == "__main__":
    solve("test1.txt")
