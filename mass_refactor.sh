#!/bin/bash

for i in {2..16}
do
    mkdir data/day_$i
    mv solutions/day_$i/data.txt data/day_$i/data.txt
    mv solutions/day_$i/test1.txt data/day_$i/test1.txt
    mv solutions/day_$i/test2.txt data/day_$i/test2.txt
    touch data/day_$i/part1_solution.txt 
    touch data/day_$i/part2_solution.txt
done