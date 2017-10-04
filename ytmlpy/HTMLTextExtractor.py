from html.parser import HTMLParser
from html.entities import html5

class HTMLTextExtractor(HTMLParser):
    """ Adaption of http://stackoverflow.com/a/7778368/196732 """
    def __init__(self):
        super().__init__()
        self.result = []

    def handle_data(self, d):
        self.result.append(d)

    def handle_charref(self, number):
        codepoint = int(number[1:], 16) if number[0] in (u'x', u'X') else int(number)
        self.result.append(chr(codepoint))

    def handle_entityref(self, name):
        if name in html5:
            # self.result.append(chr(html5[name]))
            self.result.append(html5[name])

    def get_text(self):
        return u''.join(self.result)

def html_to_text(html):
    s = HTMLTextExtractor()
    s.feed(html)
    return s.get_text()
