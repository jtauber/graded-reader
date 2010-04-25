#!/usr/bin/env python

from collections import defaultdict

ENGLISH_VERSES = {}

for line in open("translation.txt"):
    if line.startswith("#"):
        continue
    if line.strip() == "":
        continue
    
    s = line.split()
    cv = s[0]
    
    T = []
    C = None
    stack = []
    
    for token in s[1:]:
        if token.startswith("["):
            clause = token[1:]
            if C != None:
                stack.append(C)
            C = [clause, []]
        elif token == "]":
            if stack:
                stack[-1][1].append(C)
            else:
                T.append(C)
            if stack:
                C = stack.pop()
            else:
                C = None
        else:
            assert "[" not in token, token
            assert "]" not in token, token
            if C == None:
                if T == []:
                    T = [token]
                elif type(T[-1]) == str:
                    T[-1] += " " + token
                else:
                    T.append(token)
            else:
                if C[1] == []:
                    C[1] = [token]
                elif type(C[1][-1]) == str:
                    C[1][-1] += " " + token
                else:
                    C[1].append(token)
    
    ENGLISH_VERSES[cv] = T


def walk_nodes(nodes, known):
    for node in nodes:
        if type(node) == str:
            yield False, None, node
        else: # tuple
            ref, children = node
            if ref in known:
                yield True, ref, None
            else:
                for result in walk_nodes(children, known):
                    yield result


def walk_verse(verse, known):
    nodes = ENGLISH_VERSES.get(verse, [])
    for result in walk_nodes(nodes, known):
        yield result


KNOWN_CLAUSE_REFS = {}


first = True
for line in open("programme"):
    line = line.strip()
    
    if line.startswith("learn"):
        if first:
            print
            first = False
        print line
    elif line.startswith("know"):
        first = True
        print
        print line
        action, r, cvs, syncat, text = line.split(" ", 4)
        target_class, target = r.split("/")
        
        KNOWN_CLAUSE_REFS[target] = text
        
        for cv in cvs.split(","):
            if cv in ENGLISH_VERSES:
                print
                print "John %s" % cv
                for known, ref, alt in walk_verse(cv, KNOWN_CLAUSE_REFS):
                    if known:
                        if ref == target:
                            print "__%s__" % KNOWN_CLAUSE_REFS[ref], # bold
                        else:
                            print KNOWN_CLAUSE_REFS[ref],
                    else: 
                        print alt,
                print
            else:
                print "@@@ John %s not annotated yet." % cv
