#!/usr/bin/env python

"""
Optimizes the ordering of items by delaying any that are not yet needed.

The first argument is the name of the file that lists the items to be
learnt in pre-optimized order. The lines should be of the form "learn <item>".
Any line not beginning with "learn" is ignored.

The second argument is the name of the file that lists the target-item pairs.
Each line should be of the form <target> <item> separated by whitespace.
"""


import sys
LEARNING_PROGRAMME_FILENAME = sys.argv[1]
TARGET_ITEM_FILENAME = sys.argv[2]


## build target-item prerequisites

from collections import defaultdict

# targets: map of target to set of prerequisite items

targets = defaultdict(set)

for line in open(TARGET_ITEM_FILENAME):
    target, item = line.strip().split()
    targets[target].add(item)


## go through existing learning programme, only outputing items when a target needs them

# known_items: set of items known at a given point but not necessarily shown yet
known_items = set()

# shown_items: set of items shown on output
shown_items = set()

# shown_targets: set of targets shown on output
shown_targets = set()

# score
score = 0

for line in file(LEARNING_PROGRAMME_FILENAME):
    if not line.startswith("learn"):
        continue
    item = line.strip().split()[1]
    
    known_items.add(item)
    
    # for each target that can be known at this point but hasn't been shown...
    for target in targets:
        if known_items.issuperset(targets[target]) and target not in shown_targets:
            # for each item required by that target that hasn't been shown...
            for item in sorted(targets[target]): # we sort merely for determinism
                if item not in shown_items:
                    # print the item and remember that it has been shown
                    print "learn", item
                    shown_items.add(item)
            # now print the target that is known and remember that it has been shown
            print "know", target
            shown_targets.add(target)
    
    score += float(len(shown_targets)) / len(targets)
    

print "score", score