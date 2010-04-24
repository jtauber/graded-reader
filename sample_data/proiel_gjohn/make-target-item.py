#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

target_classes = {}

for line in open(sys.argv[1]):
    target_num, verse, syncat, text = line.strip().split("|")
    target_class_num = target_classes.setdefault(text, len(target_classes) + 1)
    
    for word in text.split():
        print "%04d/%s" % (target_class_num, target_num), word
