#!/usr/bin/env python
# coding: utf-8

import glob
import sys
import unicodedata

from parsexml import parse, ElementHandler


def n(x):
    return unicodedata.normalize("NFKC", x)


class Node(ElementHandler):
    
    def start(self, name, attr):
        self.items = []
        self.node_id = attr["nodeId"]
        if attr["nodeId"].endswith("0010"):  # leaf nodes
            for key in attr.keys():
                if key not in [
                    "Start", "End",
                    "nodeId", "morphId",
                    "Cat",
                    "Case", "Number", "Gender",
                    "Relative", "Personal", "Demonstrative", "Interrogative",
                    "Tense", "Voice", "Mood",
                    "Person",
                    "Degree",
                    "Unicode", "UnicodeLemma",
                ]:
                    raise Exception, key
            
            self.analysis = None
            self.parent.add_item(attr["Unicode"].strip(u".,·").encode("utf-8"))
        else:
            if "Rule" in attr:
                if "ClType" in attr:
                    self.analysis = attr["Cat"] + "{" + attr["Rule"] + "/" + attr["ClType"] + "}"
                else:
                    self.analysis = attr["Cat"] + "{" + attr["Rule"] + "}"
            else:
                self.analysis = attr["Cat"]
            self.parent.add_item(self.analysis)
    
    def add_item(self, item):
        self.items.append(item)
        self.parent.add_item(item)
    
    def end(self, name):
        if self.analysis and self.analysis.startswith("CL"):
            print self.node_id, self.analysis
            for item in self.items:
                print self.node_id, item


Node.handlers = dict(Node=Node)


class Tree(ElementHandler):
    
    handlers = dict(Node=Node)
    
    def start(self, name, attr):
        self.node_id = None
    
    def add_item(self, item):
        pass


class Trees(ElementHandler):
    
    handlers = dict(Tree=Tree)
    


class Sentence(ElementHandler):
    
    handlers = dict(Trees=Trees)
    
    def start(self, name, attr):
        pass # print attr["ID"]


class Sentences(ElementHandler):
    
    handlers = dict(Sentence=Sentence)


if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        parse(f, {"Sentences": Sentences})
else:
    for filename in glob.glob("syntax-trees/*.xml"):
        with open(filename) as f:
            parse(f, {"Sentences": Sentences})
