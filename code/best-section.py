#!/usr/bin/env python

"""
Given a file allocating items to sections, works out which sections have
the best coverage of the whole for their size.

The input file should consist of lines of <section> <item> separated by
whitespace.
"""


from collections import defaultdict


# how many times a given item appears overall
item_count = defaultdict(int)

# how many times a given section has a given item
section_item_count = defaultdict(int)

# size of each section
section_count = defaultdict(int)


## load file

import sys
FILENAME = sys.argv[1]

for line in open(FILENAME):
    section, item = line.strip().split()
    item_count[item] += 1
    section_count[section] += 1
    section_item_count[section, item] += 1


## calculate section score

section_score = {}

for section in section_count:
    contribution = 0
    for item, overall_count in item_count.items():
        if section_item_count[section, item] > 0:
            contribution += overall_count - section_item_count[section, item]

    section_score[section] = 1. * contribution / section_count[section]


## display results

for section in sorted(section_score, key=section_score.get, reverse=True):
    print("{} {:.2f}".format(section, section_score[section]))
