# coding=utf8

"""
    rux.parser
    ~~~~~~~~~~

    Parser from post source to html.
"""

from datetime import datetime
import os

from . import charset, src_ext
from .exceptions import *
import libparser

import houdini
import markdown as md
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

src_ext_len = len(src_ext)  # cache this, call only once

to_unicode = lambda string: string.decode(charset)


class Parser(object):
    """Usage::

        parser = Parser()
        parser.parse(str)   # return dict
        parser.markdown.render(markdown_str)  # render markdown to html

    """

    def __init__(self):
        """Initialize the parser, set markdown render handler as
        an attribute `markdown` of the parser"""
        render = RuxHtmlRenderer()  # initialize the color render
        self.extensions = [
            'markdown.extensions.footnotes',
            'markdown.extensions.smarty',
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
        ]

    def parse_markdown(self, markdown):
        return md.markdown(markdown, extensions=self.extensions)

    def parse(self, source):
        """Parse ascii post source, return dict"""

        rt, title, title_pic, markdown = libparser.parse(source)

        if rt == -1:
            raise SeparatorNotFound
        elif rt == -2:
            raise PostTitleNotFound

        # change to unicode
        title, title_pic, markdown = map(to_unicode, (title, title_pic,
                                                      markdown))

        # render to html
        html = md.markdown(markdown, extensions=self.extensions)
        summary = md.markdown(markdown[:200], extensions=self.extensions)

        return {
            'title': title,
            'markdown': markdown,
            'html': html,
            'summary': summary,
            'title_pic': title_pic
        }

    def parse_filename(self, filepath):
        """parse post source files name to datetime object"""
        name = os.path.basename(filepath)[:-src_ext_len]
        try:
            dt = datetime.strptime(name, "%Y-%m-%d-%H-%M")
        except ValueError:
            raise PostNameInvalid
        return {'name': name, 'datetime': dt, 'filepath': filepath}


parser = Parser()  # build a runtime parser
