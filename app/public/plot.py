#!/usr/bin/env python
#coding: utf-8

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import time
import hashlib
import json
import web


class Plot:
    def __init__(self, environ):
        self.environ = environ

    def plotPic(self):
        picdir = 'static/plot'
        picname = "%s.png" % hashlib.md5(str(time.time())).hexdigest()
        picfile = os.path.join(self.environ["DOCUMENT_ROOT"], picdir, picname)
        data = json.loads(self.environ['wsgi.input'].read(int(self.environ['CONTENT_LENGTH'])))

        plt.grid(True)
        x = data.get("x", None)
        if x:
            xlabel = x.get("label", "X")
            plt.xlabel(xlabel)
            xdata = x.get("data", None)
            if xdata:
                plt.xticks(range(len(xdata)), xdata)
        ydata = data.get("y", None)
        if not ydata:
            return "error: y data not found"
        for y in ydata:
            plt.plot(y.get("data"), label=y.get("label", "Y"))
        plt.legend(loc=0, shadow=True)
        plt.savefig(picfile)
        plt.close()
        return os.path.join("http://", self.environ['HTTP_HOST'], picdir, picname)

    @web.response
    def response(self):
        return ("text/html", self.plotPic())
