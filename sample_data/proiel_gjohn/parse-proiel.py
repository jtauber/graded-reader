#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import xml.parsers.expat
import collections


class ElementHandler(object):
    
    def __init__(self, p, name, attr):
        self.p = p
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data
        self.start(name, attr)
    
    def start_element(self, name, attr):
        cls = self.handlers.get(name)
        if cls:
            state = self.p.StartElementHandler, self.p.EndElementHandler, self.p.CharacterDataHandler
            handler = cls(self.p, name, attr)
            handler.parent = self
            handler.return_state = state
        else:
            raise Exception("%s got unknown element %s" % (self.__class__.__name__, name))
    
    def end_element(self, name):
        self.end(name)
        self.p.StartElementHandler, self.p.EndElementHandler, self.p.CharacterDataHandler = self.return_state
        self.p.StartElementHandler = self.parent.start_element
        self.p.EndElementHandler = self.parent.end_element
        self.p.CharacterDataHandler = self.parent.char_data
    
    def char_data(self, data):
        pass
    
    def start(self, name, attr):
        pass
    
    def end(self, name):
        pass


class TextOnly(ElementHandler):
    pass


book = None


class Segmented(ElementHandler):
    
    handlers = {
        "w": TextOnly,
        "s": TextOnly,
    }


class Milestone(ElementHandler):
    
    def start(self, name, attr):
        global book, chapter, verse
        if attr["unit"] == "book":
            book = attr["n"]
        if attr["unit"] == "chapter":
            chapter = attr["n"]
        if attr["unit"] == "verse":
            verse = attr["n"]


class Del(ElementHandler):
    
    handlers = {
        "w": TextOnly,
        "s": TextOnly,
        "pc": TextOnly,
        "milestone": Milestone,
    }


class Presentation(ElementHandler):
    
    handlers = {
        "milestone": Milestone,
        "w": TextOnly,
        "s": TextOnly,
        "pc": TextOnly,
        "segmented": Segmented,
        "del": Del,
    }


class Slashes(ElementHandler):
    
    handlers = {
        "slash": TextOnly,
    }


class Token(ElementHandler):
    
    handlers = {
        "slashes": Slashes,
    }
    
    def start(self, name, attr):
        if include(book):
            print book, chapter, verse,
            print attr["id"],
            if "form" in attr:
                print attr["form"].replace(" ", "+").encode("utf-8"),
                print attr["morph-features"].replace(" ", "+").encode("utf-8"),
            else:
                print attr["empty-token-sort"],
                print "-",
            print attr["relation"],
            if "head-id" in attr:
                print attr["head-id"]
            else:
                print "-"

class Sentence(ElementHandler):
    
    handlers = {
        "presentation": Presentation,
        "token": Token,
    }
    
    def start(self, name, attr):
        if include(book):
            print


class TEIHeader(ElementHandler):
    
    handlers = {
        "teiHeader": TextOnly,
    }


class Div(ElementHandler):
    
    handlers = {
        "title": TextOnly,
        "abbreviation": TextOnly,
        "sentence": Sentence,
    }


class Source(ElementHandler):
    
    handlers = {
        "title": TextOnly,
        "abbreviation": TextOnly,
        "tracked-references": TextOnly,
        "tei-header": TEIHeader,
        "div": Div,
    }

class Root(ElementHandler):
    def __init__(self, f):
        self.p = p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data
        p.Parse(f.read())
    
    handlers = {
        "source": Source,
    }


def include(book):
    return book == "JOHN"


Root(open(sys.argv[1]))
