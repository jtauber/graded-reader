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
    if line.strip():
        target, item = line.strip().split()
        targets[target].add(item)


# step 1: optimize item list

known_items = set()
shown_targets = set()

processed_items = set()

learning_programme = []

for line in file(LEARNING_PROGRAMME_FILENAME):
    if not line.startswith("learn"):
        continue
    item = line.strip().split()[1]
    
    known_items.add(item)
    
    # for each target that can be known at this point but hasn't been shown...
    for target in targets:
        if known_items.issuperset(targets[target]) and target not in shown_targets:
            # for each item required by that target that hasn't been shown...
            for item in sorted(targets[target]): # sort merely for determinism
                if item not in processed_items:
                    # store the item
                    learning_programme.append(item)
                    processed_items.add(item)
            # remember that target has been processed
            shown_targets.add(target)


# step 2: optimize target list from that item list

# reset for re-use
known_items = set()
shown_targets = set()

score = 0

for item in learning_programme:
    print "learn", item
    known_items.add(item)
    
    for target in sorted(sorted(targets), key=lambda t: len(targets[t])):
        if known_items.issuperset(targets[target]) and target not in shown_targets:
            print "know", target
            shown_targets.add(target)
    
    score += float(len(shown_targets)) / len(targets)


print "score", score