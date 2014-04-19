import sys
import os
import script


class Util:
    def __init__(self, environ, template):
        self.environ = environ
        self.template = template

    def response(self):
        return ("text/html", script.response(os.path.join(self.template, "util.html"), {"user": self.environ["USER"]}))
