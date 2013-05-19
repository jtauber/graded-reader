#!/usr/bin/env python

with open("sblgnt.txt") as f:
    for line in f:
        row = line.strip().split()
        # print("{} lexeme:{}".format(row[0], row[6]))
        # print("{} tag:{}{}".format(row[0], row[1], row[2]))
        print("{} form:{}/{}/{}{}".format(row[0], row[5], row[6], row[1], row[2]))
