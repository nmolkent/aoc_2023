# Advent of Code 2023

Like any half decent nerd I enjoy a good coding challenge. I don't expect my solutions to be the best but it is good practice.

With this repo I aim to doccument my AOC 2023 progress and practice a few new skills.

# Usage
to run from the root of the project use the command below.
without the optional arguement the script will look for the data/day/data.txt file which should always remain private in your repoository (see .gitnore), all relevant inputs should be stored in the data/day_*/ directory.

```bash
python main -m [day] [part] --filename file-to-use-as-test-input
```

Given AOC have requested no sharing publicly of any of the data inputs, in order to run tests locally files need to be created with the inputs as .txt files. see the .gitnore file for clear directory structure. if the files follow that directory structure you will be able to run tests on all inputs in data/day_*/data.txt path format using the command below. 

tests
```bash
python -m unittest
```

### About my AOC experience so far
Last year I completed the AOC challenge with my colleagues following upskilling on a datascience course. I completed 34 challenges of a total 50 and completed all the code in python in jupyter notebooks... A whole year later and I realise it might be worthwhile implementing some of the better coding practices that I've picked up practicing in a data engineering capacity and perhaps trying to learn some new skills.

## Goals for 2023
- Have fun. This is still something I'll be doing for fun, as such i'm not looking for perfection. 
- My number 1 priority will be to practice using deployment tools and automated testing. As mentioned last year I used jupyter noteboks which are great for scripting and prototyping. My primary aim for development then is to move towards deployment tools and automated testing. As such I'm doing a bit of preparation this year to create a template file structure and a place for utilities inside a package like structure.
- Improve my completion percentage. Last year I got stumped on a few challenges towards the end as the difficulty increased. The holiday season also comes with other activities especially when the challenge ramps up to its highest so, while I don't expect to reach 100% completion. There are some areas in particular that last year I wanted to improve upon which became obvious once the solutions began requiring optimisations for memory and thoughtful simplification of state. I suspect the best way to do this will be reflection and to compare my solutions with more optimised ones.

## Retrospective
Looking back, I improved my completion by a litle in the time. 37 rather than 34 is an incremental improvement but I think I can solve more of these given time. I'd like to continue through the year to create solutions for all the days.

The primary thing I learnt this year was state management. In many of the puzzles keeping track of state was crucial to be able to optimise a solution that runs in less than 10 seconds on my laptop. To this end heapq is the newest python standard library tool I've now grown familiar with. In addition the power of dataclasses is amazing. Never been a huge fan of object oriented python because it can feel quite verbose in comparison to (for example) Scala. Dataclasses resolve this but also add great customisation options.

Don't share your input data! I nuked my repo in order to delete the commit history which included data that was used in my automated tests. I think for a free resource it's common decency to respect Eric's wishes so just sorry i didn't realise sooner. Aside from that I think practice with manipulating files using shell scripts has been useful. I didn't really get to a point where deployment tools were that useful but I suspect would I want to clone this repo into another environement it would first be worth developing a script to fetch the inputs and cache them in a private cloud based storage somewhere. I'm deffinitely intrigued to try and implement this ready for next year and this'll encourage me to look into security good practices too.

The competition from my peers was great this year, very motivating. Seeing someone else had made it on the leaderboard each day made me determined to find a solution when things got more challenging. The community is deffinitely something I want to contribute more to in coming years. Fun was had!