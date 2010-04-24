#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

TARGETS = {}

for line in open(sys.argv[1]):
    target_num, verse, syncat, text = line.strip().split("|")
    TARGETS[target_num] = (verse, syncat, text)

for line in open(sys.argv[2]):
    if line.startswith("know"):
        print line.strip(),
        target_num = line.strip().split()[1]
        print " ".join(TARGETS[target_num])
    else:
        print line.strip()