#!/usr/bin/env python

import sys
import os
import re
import cStringIO


def find(line, str):
    s_str = str
    e_str = str[1] + '}'
    start = line.find(s_str)
    end = line.find(e_str)
    return (start, end)

def value(line, val):
    start, end = find(line, '{$')
    key = line[start+2:end].strip()
    line_new = line.replace(line[start:end+2], str(val[key]))
    return line_new

def include(line, temp, f):
    s, e = find(line, '{#')
    base = os.path.join(os.path.dirname(temp), line[s+2:e].strip())
    fp = open(base, 'r')
    line = fp.readline()
    if re.match("{#.*#}", line):
        fp = include(line, temp, fp)
    else:
        fp.seek(0, 0)
    sec = {}
    fb = cStringIO.StringIO()
    line = f.readline()
    while line:
        if re.match('{%.*%}', line):
            s, e = find(line, '{%')
            if line[s+2:e].strip() != 'end':
                sec.update({line[s+2:e].strip(): f.tell()})
        line = f.readline()
    line = fp.readline()
    while line:
        if re.match('{\+.*\+}', line):
            s, e = find(line, '{+')
            k = line[s+2:e].strip()
            if sec.has_key(k):
                f.seek(sec[k], 0)
                line_f = f.readline()
                while line_f:
                    if re.match('{%\s*end\s*%}', line_f):
                        break
                    fb.write(line_f)
                    line_f = f.readline()
        else:
            fb.write(line)
        line = fp.readline()
    fb.seek(0, 0)
    return fb

def script(f, Tdict):
    fp = cStringIO.StringIO()
    f.seek(0)
    line = f.readline()
    indent = line.find(line.strip()[0])
    while line:
        if re.match('\s+$', line[:indent]):
            line = line[indent:]
        if line.strip().split(' ')[0] == 'echo':
            line = line.replace('echo', 'res +=')
        fp.write(line)
        line = f.readline()
    fp.seek(0)
    res = str()
    exec_str = fp.read()
    exec(exec_str)
    return res

def response(temp, val):
    response_body = str()
    fp = open(temp, 'r')
    line = fp.readline()
    if re.match('{#.*#}', line):
        fp = include(line, temp, fp)
        line = fp.readline()
    while line:
        if re.search('{\$.*\$}', line):
            line = value(line, val)
            continue
        if re.match('<script\s+type\s*=\s*"\s*text/python\s*"\s*>', line):
            fb = cStringIO.StringIO()
            line = fp.readline()
            while line:
                if re.match('</script>', line):
                    response_body += script(fb, val)
                    line = fp.readline()
                    break
                fb.write(line)
                line = fp.readline()
            continue
        response_body += line
        line = fp.readline()
    return response_body


if __name__ == '__main__':
    print response('../wsgi/mon/template/test2.html', {'t': "test", "ip": ["10.73.48.26", "10.73.48.28"]})
