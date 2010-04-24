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


## calculate contribution

section_contribution = {}

for section in section_count:
    contribution = 0
    for item, count in item_count.items():
        if section_item_count[section, item] > 0:
            contribution += count - section_item_count[section, item]
    
    section_contribution[section] = 1. * contribution / section_count[section]


## display results

for section in sorted(section_contribution, key=section_contribution.get, reverse=True):
    print "%05s %.2f" % (section, section_contribution[section])
