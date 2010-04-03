#!/usr/bin/env python

"""
Output a list of the top ten targets whose second least frequent item is
most frequent overall.
"""


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
    item_counts[item] +=1

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

# build a dict from target to second least frequent item target needs

last = dict([(target, targets[target][-2]) for target in targets])

for target in sorted(last, key=last.get)[:10]:
    print target, last[target], targets[target]
