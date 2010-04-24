#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

for line in open(sys.argv[1]):
    clause_num, verse, syncat, text = line.strip().split("|")
    
    for word in text.split():
        print clause_num, word
