#!/bin/bash

day=$1

mkdir solutions/day_$day
mkdir data/day_$day

touch data/day_$day/data.txt
touch data/day_$day/test1.txt
touch data/day_$day/test2.txt
touch data/day_$day/part1_solution.txt
touch data/day_$day/part2_solution.txt

cp templates/solution_template.py solutions/day_$day/part1.py
cp templates/solution_template.py solutions/day_$day/part2.py
touch solutions/day_$day/__init__.py

echo "created folder: day_$day"
echo "with files"
ls solutions/day_$day