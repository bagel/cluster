#!/usr/bine/env python

import sys
import os
import script
import augs
import time
import uwsgi


def test(environ, template):
    ctype = 'text/html'
    tdict = {'t': 'test'}
    response_body = script.response(os.path.join(template, 'test.html'), tdict)
    return (ctype, response_body)

def vhost(environ, template):
    ctype = 'text/html'
    #data = augs.Role().read(name="vipbook")['result']['data'][0]['configuration']['files'][0]['data']
    #tdict = {"ServerName": data['ServerName'], "ServerAlias": [ str(alias) for alias in data['ServerAlias'] ], "ServerAdmin": data['ServerAdmin']}
    tdict = {}
    response_body = script.response(os.path.join(template, 'vhost.html'), tdict)
    return (ctype, response_body)

def post(environ, template):
    length = int(environ['CONTENT_LENGTH'])
    data = environ['wsgi.input'].read(length)
    return ('text/plain', data)

def ws(environ, template):
    ws_scheme = 'ws'
    response_body = """
    <html>
      <head>
          <script language="Javascript">
            var s = new WebSocket("%s://%s/foobar/");
            s.onopen = function() {
              alert("connected !!!");
              s.send("ciao");
            };
            s.onmessage = function(e) {
        var bb = document.getElementById('blackboard')
        var html = bb.innerHTML;
        bb.innerHTML = html + '<br/>' + e.data;
            };
        
        s.onerror = function(e) {
            alert(e);
        }
    
    s.onclose = function(e) {
        alert("connection closed");
    }
            
            function invia() {
              var value = document.getElementById('testo').value;
              s.send(value);
            }
          </script>
     </head>
    <body>
        <h1>WebSocket</h1>
        <input type="text" id="testo"/>
        <input type="button" value="invia" onClick="invia();"/>
    <div id="blackboard" style="width:640px;height:480px;background-color:black;color:white;border: solid 2px red;overflow:auto">
    </div>
    </body>
    </html>
        """ % (ws_scheme, environ['HTTP_HOST'])
    return ("text/html", response_body)

def foobar(environ, template):
        uwsgi.websocket_handshake(environ['HTTP_SEC_WEBSOCKET_KEY'], environ.get('HTTP_ORIGIN', ''))
        print "websockets..."
        uwsgi.suspend()
        while True:
            msg = uwsgi.websocket_recv_nb()
            uwsgi.websocket_send("[%s] %s" % (int(time.time()), msg))
            time.sleep(1)
