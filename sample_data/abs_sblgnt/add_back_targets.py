#!/usr/bin/env python

import sys

book = [
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians",
    "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter",
    "1 John", "2 John", "3 John", "Jude", "Revelation"
]

TARGETS = {}

for line in open(sys.argv[1]):
    target_num, text = line.strip().split(" ", 1)
    TARGETS[target_num] = text

for line in open(sys.argv[2]):
    if line.startswith("know"):
        target_num = line.strip().split()[1]
        bcv = book[int(target_num[:2]) - 40], int(target_num[2:5]), int(target_num[5:8])
    
        print "know", "{} {}.{}".format(*bcv),
        print TARGETS[target_num]
    else:
        print line.strip()
