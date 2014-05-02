import sys
import os
import urlparse
import web
import json
import subprocess
import hashlib
import time
import random
import re

@web.response
def convert(environ):
    ctype = "application/json"
    document_root = environ['DOCUMENT_ROOT']
    query_string = environ["QUERY_STRING"]
    if not query_string or not re.match("url=", query_string):
        return (ctype, json.dumps({"errmsg": "url not found"}))
    url = re.sub(r'url=(.*)', r'\1', query_string)
    applog_dir = os.path.join(web.getenv("APPLOGS_DIR"), 'ghostdriver.log')
    chartjs_dir = os.path.join(document_root, web.getenv("CHARTJS_DIR"), "chart.js")
    chart_file = hashlib.md5(url + str(time.time()) + str(random.randint(0, 100000))).hexdigest()
    chart_svg = os.path.join('/tmp', chart_file + '.svg')
    phantomjs = "/usr/local/sinasrv2/bin/phantomjs --webdriver-logfile=%s %s %s %s" % (applog_dir, chartjs_dir, url, chart_svg)
    p = subprocess.Popen(phantomjs, shell=True, stdout=subprocess.PIPE)
    p.wait()
    chart_png = os.path.join(document_root, web.getenv("IMAGE_DIR"), chart_file + '.png')
    os.environ['LANG'] = 'zh_CN.UTF-8'
    cairosvg = '/usr/bin/cairosvg %s -o %s' % (chart_svg, chart_png)
    p1 = subprocess.Popen(cairosvg, shell=True, stdout=subprocess.PIPE)
    p1.wait()
    os.remove(chart_svg)
    url = 'http://' + os.path.join(environ["HTTP_HOST"], web.getenv("IMAGE_DIR"), chart_file + '.png')
    return (ctype, json.dumps({"url": url}))


if __name__ == "__main__":
    convert(environ)
