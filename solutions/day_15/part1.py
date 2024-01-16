
def lens_hash(s: str):
    current_hash = 0
    for c in s.strip():
        current_hash += ord(c)
        current_hash *= 17
        current_hash %= 256
    return current_hash

def solve(filename: str):
    global hash_store
    total = 0
    with open(filename) as file:
        for line in file:
            for s in line.split(","):
                total += lens_hash(s)            
    return total

if __name__ == "__main__":
    solve("test1.txt")
