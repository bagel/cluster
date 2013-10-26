web admin
========
api.dpool.cluster.sina.com.cn

#Nginx

config with nginx + uwsgi

##nginx

	server {
	        listen       80 ;
	        root /data1/www/htdocs/api.dpool.cluster.sina.com.cn;
	        server_name api.dpool.cluster.sina.com.cn;
	
	        access_log  /data1/www/logs/api.dpool.cluster.sina.com.cn-access_log  main;
	        access_log  /data1/www/logs/all_items_http_log  main;
	        error_log   /data1/www/logs/api.dpool.cluster.sina.com.cn-error_log;
	
	        location ~ /static/(.*) {
	                alias /data1/www/htdocs/api.dpool.cluster.sina.com.cn/static/$1;
	                expires 1d;
	        }
	
	        location / {
	                uwsgi_pass 127.0.0.1:9002;
	                expires -1;
	        }
	}


##uwsgi

	[uwsgi]
	chdir = %(document_root)
	cpu-affinity = 1
	daemonize = %(sinasrv)/var/logs/uwsgi/%n.log
	document_root = /data1/www/htdocs/%n
	gid = www
	master = true
	pidfile = %(sinasrv)/var/run/uwsgi/%n.pid
	plugins = /usr/local/sinasrv2/lib/uwsgi/python_plugin.so
	sinasrv = /usr/local/sinasrv2
	socket = 127.0.0.1:9002
	stats = 127.0.0.1:7002
	uid = www
	workers = 8
	wsgi-file = wsgi
	env = SINASRV_APPLOGS_DIR=/data1/www/applogs/%n
	env = SINASRV_DB_HOST=10.73.48.210
	env = SINASRV_DB_PORT=3306
	env = SINASRV_MEMCACHED_SERVERS=10.13.32.22:7601


#Apache

config with apache

##apache
