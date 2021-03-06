#!/usr/bin/env python3

"""
Output a table showing what percentage of targets can be read assuming
a certain percentage coverage (columns) and number of items learnt in
frequency order (rows).

The input file should consist of lines of <target> <item> separated by
whitespace.

COVERAGE and ITEM_COUNTS below are configurable.
"""

import math


## configurable settings

# 0.001 is approximately "any"
ANY = 0.001

# list of coverage ratios we want to calculate for
COVERAGE = [ANY, 0.50, 0.75, 0.90, 0.95, 1.00]

# list of item counts we want to display for
ITEM_COUNTS = [100, 200, 500, 1000, 2000, 5000]


## load file

import sys
FILENAME = sys.argv[1]

# target_item_list: list of (target, item) tuples to save us loading the file
# twice

target_item_list = []
for line in open(FILENAME):
    target_item_list.append(line.strip().split())


## build item info

from collections import defaultdict

# item_counts - map of item to item count

item_counts = defaultdict(int)

for target, item in target_item_list:
    item_counts[item] += 1


# items: map of item to frequency order
items = {}
for i, x in enumerate(sorted(item_counts, key=item_counts.get, reverse=True)):
    items[x] = i + 1


## build target info

# targets - map of target to list of frequency order of items in that target

targets = defaultdict(list)
for target, item in target_item_list:
    targets[target].append(items[item])

# sort the list of item frequency orders

for target in targets:
    targets[target] = sorted(targets[target])

# so now if targets[X] = [5, 5, 20, 50],
# it means that target X consists of the 5th most frequent item (twice), the
# 20th most frequent and the 50th most frequent it also means if you want to
# read 50% of this target (i.e. 2/4) you need to know up to the 5th most
# frequent word and if you want to read 75% of this target (i.e. 3/4) you need
# to know up to the 20th most frequenct word


## calculate what's needed for each target

# needed - maps a given coverage ratio to a list which, for each target, gives
# the least frequent word necessary to reach that coverage ratio for that
# target
needed = {}

for coverage in COVERAGE:
    needed[coverage] = [
        targets[target][
            math.ceil(coverage * len(targets[target])) - 1
        ] for target in targets
    ]

# in other words if needed[0.50] = [16, 44, 182, 34, 21, 36, 8, 48, 21, 26],
# that means that to achieve 50% coverage, the first target needs up to the
# 16th most frequent word, the second target needs up to the 44th most
# frequent word, the third target needs up to the 182nd most frequent word,
# and so on...


## display table

# header
print("{:6s}".format(""), end=" ")
for coverage in COVERAGE:
    if coverage == ANY:
        print("{:>9s}".format("ANY"), end=" ")
    else:
        print("{:9.2%}".format(coverage), end=" ")
print()
print("-" * (6 + 10 * len(COVERAGE)))

for item_count in ITEM_COUNTS:
    print("{:6d}".format(item_count), end=" ")
    for coverage in COVERAGE:
        # how many targets require less than or equal to item_count to reach
        # the given coverage?
        num = len([freq for freq in needed[coverage] if freq <= item_count])
        print("{:9.2%}".format(num / len(targets)), end=" ")
    print()

# ALL row
print("{:>6s}".format("ALL"), end=" ")
for coverage in COVERAGE:
    num = len([freq for freq in needed[coverage] if freq <= len(items)])
    print("{:9.2%}".format(num / len(targets)), end=" ")
print()
