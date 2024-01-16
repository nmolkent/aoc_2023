from collections import defaultdict

# clearly this is an optimisation problem, you're not meant to itterate over the ranges, instead just focus on the begining and end.
# a single range is transformed into a list of ranges because if a transformation partially intersects a range it will produce multiple ranges
# the apply_transformation function does this work

def apply_transformations(r: (int, int), transformation_list: list[(int, int, int)], location: str, debug=False):
    # this is recursive over the list of transformations
    # this is because some transformations leave 2 chunks of remaining range, recursion deals with this quite elegantly
    # allowing us to call the function again on each remaining chunk
    
    # given an original range and a list of transformations the output will be a list of ranges that have either been transformed
    # or the remainder of the original range that was not transformed

    # debugging this was a complete nightmare so I've left the debug statements in accessable by a default arg
    # comments provide some visual representation of the ranges with round brackets representing the original range 
    # debug statements print these comments with the ranges filled in
    # and square ones representing the transformation range
    # long form variables represent the original range, single letters the transformation range
    if len(transformation_list) == 0:
        #     (remained)   
        if debug:
            print(location, "was not transformed")
            print(location, f"   {r}    =>    {r}   ")
        return [r]
    else:
        start, end = r
        d, s, e = transformation_list[0]
        mv = d - s
        # (  ) = range to transform
        # [  ] = range of transformation
        if start < s and end > e:
            # (   [moved]   )
            stat1, move, stat2 = (start, s), (d, e + mv), (e, end)
            if debug:
                print(location, "s, e, mv:", s, e, mv)
                print(f"({stat1}[{(s, e)}]{stat2}) => (  )[{move}](  )")
            return apply_transformations(stat1, transformation_list[1:], location, debug) +  apply_transformations(stat2, transformation_list[1:], location, debug) + [move]
        elif start >= s and end <= e:
            # [ignored(moved)ignored]
            if debug:
                print(location, "s, e, mv:", s, e, mv, "exclusive transformation")
                print(f"[   ({(start, end)})   ] => (ignored)[{(start + mv, end + mv)}](ignored)")
            return [(start + mv, end + mv)]
        elif start < s and end > s and end <= e:
            # (remained[moved)ignored]
            static, move = (start, s), (d, end + mv)
            if debug:
                print(location, "s, e, mv:", s, e, mv)
                print(f"({static}[{(s, end)})  ] => ({static}))[{move}](ignored)")
            return apply_transformations(static, transformation_list[1:], location, debug) + [move]
        elif start >= s and start < e and end > e:
            # (ignored[moved)remained]
            move, static = (start + mv, e + mv), (e, end)
            if debug:
                print(location, "s, e, mv:", s, e, mv)
                print(f"[  ({(start, s)}]{static}) => (ignored)[{move}]({static})")
            return apply_transformations(static, transformation_list[1:], location, debug) + [move]
        else:
            #     (remained)    
            return apply_transformations((start, end), transformation_list[1:], location, debug)

def solve(filename):
    transformations = defaultdict(list)
    ranges = defaultdict(list)
    destinations = {}

    # read input data into the data structures above 
    # (note the only range initially is seeds, the other ranges are transformations)
    with open(filename) as file:
        for line in file:
            if len(line.strip()) == 0:
                pass
            elif line[0:len("seeds: ")] == "seeds: ":
                seed_values = [int(i) for i in line.strip()[len("seeds: "):].split(" ")]
                # (start, end) was much easier to work with than (start, length)
                ranges["seed"] = [(s, s + l) for s, l in zip(seed_values[0::2], seed_values[1::2])] 
            elif not line.strip()[0].isdigit():
                src_name, dest_name = tuple(line.split(" ")[0].split("-to-"))
                destinations[src_name] = dest_name
            else:
                d, s, l = tuple(map(int, line.strip().split(" ")))
                transformations[src_name].append((d, s, s+l))

    # itterate over the data structures to take each original range and apply transformations to that range
    # the new ranges created/left over will be added to the ranges data structure under the transformations name ie. soil
    for src_name, transform_list in transformations.items():
        for r in ranges[src_name]:
            new_range = apply_transformations(r, transform_list, src_name)
            ranges[destinations[src_name]] += new_range

    ans = min(ranges["location"], key=lambda x: x[0])[0]
    return ans
    

if __name__ == "__main__":
    solve("test1.txt")
    