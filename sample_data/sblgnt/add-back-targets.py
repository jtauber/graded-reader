#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict

TARGETS = defaultdict(list)

for line in open(sys.argv[1]):
    if line.strip():
        row = line.strip().split()
        TARGETS[row[0]].append(row[3])

for line in open(sys.argv[2]):
    if line.startswith("know"):
        print line.strip(),
        target_num = line.strip().split()[1]
        print " ".join(TARGETS[target_num])
    else:
        print line.strip()
