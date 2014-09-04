#coding: utf-8
import sys
import os
import redis
import yaml
import util2 as util
import json
import urllib2
import time
import alert


class NetworkMonitor(object):
    def __init__(self):
        self.config = "/etc/dAppCluster/confs/check_net.yaml"
        self.r = redis.StrictRedis(util.localenv("REDIS_ALERT_HOST"), int(util.localenv("REDIS_ALERT_PORT")))
        self.m = int(time.time()) / 60 * 60

    def monConfig(self):
        with open(self.config, "r") as fp:
            conf = yaml.load(fp.read())
        data = {}
        for idc, ip in conf["monitor_ip"].iteritems():
            for role in conf["check_role"]:
                for idc_dst in conf["check_idc"][idc]:
                    if not conf[role].has_key(idc_dst):
                        continue
                    for role_web, ips in conf[role][idc_dst].iteritems():
                        if isinstance(ips, str):
                            data["_".join([ip, ips])] = "-".join([idc, idc_dst, role_web, role])
                        elif isinstance(ips, list):
                            for ip_dst in ips:
                                data["_".join([ip, ip_dst])] = "-".join([idc, idc_dst, role_web, role])
        return data

    def sendGtalk(self, msg):
        data = {"to": ["freetgm@gmail.com"], "msg": msg}
        req = urllib2.Request(url="http://10.210.215.69/pybot/send")
        req.add_data(json.dumps(data))
        return urllib2.urlopen(req).read()

    def sendMail(self, msg, title, fail):
        am = alert.AutoMail()
        message = '''
<table style="border-top: 1px solid #ddd; border-left: 1px solid #ddd; border-spacing: 0;">
<thead>
    <tr style="font-size: 16px">
        <th style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">监控点</th>
        <th style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">目标地址</th>
        <th style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">目标角色</th>
        <th style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">%s</th>
        <th style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">最小时间</th>
        <th style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">平均时间</th>
        <th style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">最大时间</th>
    </tr>
</thead>
<tbody>
%s
</tbody>
</table>
<br>
收集时间: %s
''' % (fail, msg, time.strftime("%Y-%m-%d %H:%M", time.localtime(self.m)))
        am.mail("【动态平台自动监控】%s监控" % title, message, ["caoyu2@staff.sina.com.cn", "zhigang6@staff.sina.com.cn"])

    def monPort(self, ips):
        msg = ''
        try:
            portData = eval(self.r.hget("port%s" % self.m, ips))
        except:
            return msg
        if float(portData[0]) > 1 or float(portData[3]) > 1:
            return portData
        return msg

    def monPing(self, ips):
        msg = ''
        try:
            pingData = eval(self.r.hget("ping%s" % self.m, ips))
        except:
            return msg
        if float(pingData[0]) > 1 or float(pingData[3]) > 100:
            return pingData
        return msg

    def mon(self):
        mondata = self.monConfig()
        msg_temp = '''<tr>
<td style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">%s</td>
<td style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">%s</td>
<td style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">%s</td>
<td style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">%s</td>
<td style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">%s</td>
<td style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">%s</td>
<td style="border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 10px">%s</td>
</tr>'''
        msg_port = msg_ping = ''
        for ips, val in mondata.iteritems():
            dataPort = self.monPort(ips)
            if dataPort:
                msg_port += msg_temp % (ips.split('_')[0], ips.split('_')[1], val.split('-')[2], dataPort[0], dataPort[1]+'s', dataPort[2]+'s', dataPort[3]+'s')
            dataPing = self.monPing(ips)
            if dataPing:
                msg_ping += msg_temp % (ips.split('_')[0], ips.split('_')[1], val.split('-')[2], dataPing[0], dataPing[1]+'ms', dataPing[2]+'ms', dataPing[3]+'ms')
        if msg_port:
            self.sendMail(msg_port, "端口80", "超时1s")
        if msg_ping:
            self.sendMail(msg_ping, "网络ping", "丢包")
        #self.sendGtalk('\n'.join(msgs))
        print self.m

if __name__ == "__main__":
    nm = NetworkMonitor()
    nm.mon()
