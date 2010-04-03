#!/usr/bin/env python

"""
Orders the learning of items based on, at each step, assigning a score to each
unknown item and learning the highest scoring item next before recalculating
the scores all over again with the remaining items.

The score is currently the sum of 1 / 2 ** number_of_items_missing_from_target
for each target in which the item is missing.

Therefore, at each step, it favours a next item that is the only missing item
(or one of only a few missing items) from lots of targets.

The input file should consist of lines of <target> <item> separated by
whitespace.

The output will consist of "learn <item>" and "know <target>" lines.
"""

import sys
FILENAME = sys.argv[1]

from collections import defaultdict

# a dictionary mapping targets to a set of items that are needed
# (and initially missing)
MISSING_IN_TARGET = defaultdict(set)

# a dictionary mapping items to a set of targets the items are needed for
# (and initially missing from)
TARGETS_MISSING = defaultdict(set)

for line in file(FILENAME):
    target, item = line.strip().split()
    MISSING_IN_TARGET[target].add(item)
    TARGETS_MISSING[item].add(target)

while True:
    
    # for each item, a score of how bad it is that it is missing
    MISSING_ITEMS = defaultdict(int)
    
    for missing in MISSING_IN_TARGET.values():
        for item in missing:
            # if item is only missing item for a target, add 1/2 to its score
            # if item is 1 of 2 missing items for a target, add 1/4
            # if item is 1 of 3 missing items for a target, add 1/8
            # and so on...
            MISSING_ITEMS[item] += 1. / (2 ** len(missing))
    
    # stop if there are no missing items
    if not MISSING_ITEMS:
        break
        
    # otherwise the next item to learn is the one with the highest score
    next_item = sorted(MISSING_ITEMS, key=MISSING_ITEMS.get)[-1]
    
    print "learn", next_item
    
    # for each target missing that item, remove the item
    for target in TARGETS_MISSING[next_item]:
        MISSING_IN_TARGET[target].remove(next_item)
        
        # if the target is now missing no items...
        if len(MISSING_IN_TARGET[target]) == 0:
            
            # it is known
            print "know", target
            del MISSING_IN_TARGET[target]
    
    del TARGETS_MISSING[next_item]


print len(MISSING_IN_TARGET), "targets unread"
