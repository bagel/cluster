web admin
========
api.dpool.cluster.sina.com.cn

##Config

#config file

* **update**

	curl 10.13.32.236/config/update -d @conf.json -H "Host: api.dpool.cluster.sina.com.cn"

conf.json

	{
	    "name": "php-fpm.ini",
	    "path": "/usr/local/sinadata/php-fpm/php-fpm.ini",
	    "owner": "root:root",
	    "perm": "0644",
	    "type": "file",
	    "module": "global",
	    "version": 1,
	    "author": "caoyu2",
	    "cmd0": "L2V0Yy9pbml0LmQvcGhwLWZwbSByZWxvYWQ=",
	    "cmd1": "L2V0Yy9pbml0LmQvcGhwLWZwbSByZWxvYWQ=",
	    "data": "dGVzdCBAQGludGlwQEAgd29ya1xuICAgIHRlc3Q="
	}

cmd0, cmd1 and data are base64 encode
