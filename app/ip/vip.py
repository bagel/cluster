#!/usr/bin/env python

import sys
import os
import redis


r = redis.StrictRedis("10.13.32.21")

vip = {
    "tc": {
        "dpool2_web": "123.126.42.251",
    },
    "yf": {
        "dpool2_web": "180.149.136.253",
        "dpool3_web": "180.149.153.146",
    },
    "xd": {
        "dpool2_web": "202.108.5.125",
    },
    "ja": {
        "dpool2_web": "219.142.78.157",
    },
    "bx": {
        "dpool2_web": "123.125.29.250",
        "dpool3_web": "123.125.29.243",
    },
    "sh": {
        "dpool2_web": "61.172.207.235",
    },
    "gd": {
        "dpool2_web": "58.63.237.237",
        "dpool3_web": "58.63.236.252",
    },
    "yhg": {
        "dpool2_web": "111.13.87.157",
        "dpool3_web": "111.13.88.233",
    },
    "sb": {
        "dpool2_web": "183.232.24.230",
        "dpool3_web": "183.232.24.242",
    },
    "edu": {
        "dpool2_web": "121.194.0.211",
        "dpool3_web": "58.205.212.115",
    }
}

r.set("vip", vip)

print vip
