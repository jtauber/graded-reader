#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

CLAUSES = {}

for line in open(sys.argv[1]):
    clause_num, verse, syncat, text = line.strip().split("|")
    CLAUSES[clause_num] = (verse, syncat, text)

for line in open(sys.argv[2]):
    if line.startswith("know"):
        print line.strip(),
        clause_num = line.strip().split()[1]
        print " ".join(CLAUSES[clause_num])
    else:
        print line.strip()