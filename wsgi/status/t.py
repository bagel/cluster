import json

test =  open("config").read().strip()
print str(json.loads(test)["idc"]["xd"].encode("utf-8"))
