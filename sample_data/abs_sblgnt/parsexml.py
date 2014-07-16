import xml.parsers.expat


class ElementHandler(object):

    def __init__(self, p, parent, name, attr):
        self.p = p
        self.parent = parent
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data
        self.start(name, attr)

    def start_element(self, name, attr):
        cls = self.handlers.get(name)
        if cls:
            state = self.p.StartElementHandler, self.p.EndElementHandler, self.p.CharacterDataHandler
            handler = cls(self.p, self, name, attr)
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

    handlers = {}


def parse(f, root_handlers):

    class Root(ElementHandler):
        def __init__(self, f):
            self.p = p = xml.parsers.expat.ParserCreate()
            p.StartElementHandler = self.start_element
            p.EndElementHandler = self.end_element
            p.CharacterDataHandler = self.char_data
            p.Parse(f.read())

        handlers = root_handlers

    Root(f)
