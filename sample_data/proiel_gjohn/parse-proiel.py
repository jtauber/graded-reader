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


class Segmented(ElementHandler):
    
    handlers = {
        "w": TextOnly,
        "s": TextOnly,
    }


class Milestone(ElementHandler):
    
    def start(self, name, attr):
        self.attr = attr
    
    def end(self, name):
        global book, chapter, verse
        attr = self.attr
        if isinstance(self.parent.parent, Sentence):
            sentence = self.parent.parent
        elif isinstance(self.parent.parent.parent, Sentence):
            sentence = self.parent.parent.parent
        else:
            raise Exception()
        if attr["unit"] == "book":
            book = attr["n"]
            sentence.add_book(book)
        if attr["unit"] == "chapter":
            chapter = attr["n"]
            sentence.add_chapter(chapter)
        if attr["unit"] == "verse":
            verse = attr["n"]
            sentence.add_verse(verse)


class W(ElementHandler):
    
    def end(self, name):
        # tell sentence it hit a w
        if isinstance(self.parent.parent, Sentence):
            sentence = self.parent.parent
        elif isinstance(self.parent.parent.parent, Sentence):
            sentence = self.parent.parent.parent
        else:
            raise Exception()
        sentence.got_w()

class Del(ElementHandler):
    
    handlers = {
        "w": W,
        "s": TextOnly,
        "pc": TextOnly,
        "milestone": Milestone,
    }


class Presentation(ElementHandler):
    
    handlers = {
        "milestone": Milestone,
        "w": W,
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
        self.attr = attr
    
    def end(self, name):
        attr = self.attr
        BCV = self.parent.BCV
        if include(BCV):
            assert BCV
            print format_bcv_set(BCV),
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
        self.book = None
        self.chapter = None
        self.verse = None
        self.BCV = set()
    
    def got_w(self):
        # we need to know this to see if BCV is carrying over from previous
        # sentence
        
        if not self.book:
            self.book = book
        if not self.chapter:
            self.chapter = chapter
        if not self.verse:
            self.verse = verse
        self.BCV.add((self.book, self.chapter, self.verse))
        
        
    def add_book(self, book):
        self.book = book
    
    def add_chapter(self, chapter):
        self.chapter = chapter
    
    def add_verse(self, verse):
        self.verse = verse
    
    def end(self, name):
        if include(self.BCV):
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


def include_book(book_name):
    def _(BCV):
        return book_name in (book for book, chapter, verse in BCV)
    return _


def include_chapter(book_name, chapter_num):
    def _(BCV):
        return (book_name, chapter_num) in ((book, chapter) for book, chapter, verse in BCV)
    return _


def format_bcv_set(BCV):
    books = set(book for book, chapter, verse in BCV)
    assert len(books) == 1
    book_string = books.pop()
    
    cv_string = ",".join(("%d.%d" % (c,v) for c,v in sorted((int(chapter), int(verse)) for book, chapter, verse in BCV)))
    return "%s %s" % (book_string, cv_string)

if len(sys.argv) == 3:
    include = include_book(sys.argv[2])
elif len(sys.argv) == 4:
    include = include_chapter(sys.argv[2], sys.argv[3])
else:
    print "usage: ./parse_proiel.py <xml file> <book name> [<chapter num>]"
    sys.exit(1)

Root(open(sys.argv[1]))
