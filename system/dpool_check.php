<?php
/************************************************
 * Dynamic architecture monitor
 * Apri. 21th, 2006
 * Maintainer: WangLijun (lijun3@staff.sina.com.cn)
 **********************************************/

header('Content-Type: text/xml; charset=utf-8');
error_reporting(E_ALL & (!E_NOTICE));
ini_set('display_errors', true);
ini_set('html_errors', false);
ini_set('mysql.connect_timeout', 2);
set_time_limit(0);

$errno = 0; // for each resource
$info = ""; // for each resource
$xmlret = "<?xml version='1.0' encoding='utf-8'?><xml>";

$g_env_dir = array();
$g_env_dbr = array();
$g_env_dbw = array();
$g_env_sinasrv = array();

$g_dbr = array();
$g_dbw = array();
$g_func = array();
$g_mc = array();
$g_mcl = array();

// basic env variables to be checked
$env_dir_check = array('SINASRV_DATA_DIR', 'SINASRV_CACHE_DIR',
        'SINASRV_PRIVDATA_DIR',    'SINASRV_APPLOGS_DIR');
$env_dbw_check = array('SINASRV_DB_HOST', 'SINASRV_DB_PORT',
        'SINASRV_DB_NAME', 'SINASRV_DB_USER',
        'SINASRV_DB_PASS');
$env_dbr_check = array('SINASRV_DB_HOST_R', 'SINASRV_DB_PORT_R',
        'SINASRV_DB_NAME_R', 'SINASRV_DB_USER_R',
        'SINASRV_DB_PASS_R');

// special variales in SINASRV_CONFIG but no need exist in httpd.conf
$special_var = array('SINASRV_SERVER_NAME', 'SINASRV_DOCUMENT_ROOT',
                    'DOCUMENT_ROOT', 'SINASRV_SERVER_PORT');

//////////////////////////////////////////////
// functions

function read_sinasrv_config($file)
{
    global $g_env_sinasrv;
    global $env_info;
    global $special_var;

    if(!$handle = fopen($file, 'r')) {
        $env_info = "cannot open file $file";
        return false;
    }
    while(!feof($handle)) {
        $line = fgets($handle);
        if(preg_match('/^\s*$/', $line)) continue;
        list($k, $v) = split("=", $line, 2);
        $k = preg_replace('/^(\w+) */', "\${1}", $k);
        foreach ($special_var as $s_k => $s_v) {
            if($k == $s_v) continue 2;
        }
        $v = preg_replace('/^ *"?(.+?)"?\n/', "\${1}", $v);
        $g_env_sinasrv["$k"] = $v;
    }
    fclose($handle);

    return true;
}

//function
function test_env_match()
{
    global $g_env_sinasrv;
    global $env_info;
    $ret = true;
    $special_db = array('SINASRV_DB_HOST', 'SINASRV_DB_NAME');

    foreach ($_SERVER as $k => $v) {
        if(!preg_match('/^SINASRV_.+/', $k)) continue;
        if(array_key_exists($k, $g_env_sinasrv)) {
            if($g_env_sinasrv["$k"] != $v) {
                $env_info .= "env $k not match between SINASRV_CONFIG and httpd.conf\n";
                $ret = false;
            }
        } else {
            if($k == 'SINASRV_DB_HOST' &&
            !array_key_exists('SINASRV_DB_NAME', $_SERVER)) continue;
            if($k == 'SINASRV_DB_HOST_R' &&
            !array_key_exists('SINASRV_DB_NAME_R', $_SERVER)) continue;

            $env_info .= "env $k not exists in file SINASRV_CONFIG\n";
            $ret = false;
        }
    }

    foreach ($g_env_sinasrv as $k => $v) {
        if(!array_key_exists($k, $_SERVER)) {
            $env_info .= "env $k not exists in httpd.conf\n";
            $ret = false;
        }
    }

    return $ret;
}

function get_env_variables()
{
    global $g_env_dir;
    global $g_env_dbr;
    global $g_env_dbw;
    global $env_dir_check;
    global $env_dbw_check;
    global $env_dbr_check;

    foreach($_SERVER as $k => $v) {
	if(preg_match('/^SINASRV_NDATA_DIR$/', $k)) {
	    continue;
        } else if(preg_match('/^SINASRV_NCACHE_DIR$/', $k)) {
            continue;
        } else if(preg_match('/^SINASRV_.*_DIR$/', $k)) {
            if($k == "SINASRV_CGIBIN_DIR") continue;
            $g_env_dir["$k"]['dir'] = $v;
        } else if(preg_match('/^SINASRV_DB(\d*)_.*_R$/', $k, $match)) {
            if(empty($match[1])) { $match[1] = 0; }
            $g_env_dbr[$match[1]]["$k"] = $v;
        } else if(preg_match('/^SINASRV_DB(\d*)_.*$/', $k, $match)) {
            if(empty($match[1])) { $match[1] = 0; }
            $g_env_dbw[$match[1]]["$k"] = $v;
        }
    }

    // assure basic env varibles be exist
/*
    foreach($env_dir_check as $k => $v) {
        $g_env_dir["$v"]['dir'] = $_SERVER["$v"];
    }
    foreach($env_dbw_check as $k => $v) {
        $g_env_dbw[0]["$v"] = $_SERVER["$v"];
    }
    foreach($env_dbr_check as $k => $v) {
        $g_env_dbr[0]["$v"] = $_SERVER["$v"];
    }
*/
}

function read_pipe($cmd)
{
    $fp = @popen($cmd, "r");
    if (!$fp)
    {
        return "unexecutable";
    }

    while(!feof($fp))
    {
        $res .= fgets($fp);
    }

    @pclose($fp);
    return $res;
}

function test_db_w($key, &$db, &$db_res) {
    if($key == 0) $key = "";
    if(!empty($db["SINASRV_DB${key}_HOST"]) &&
       empty($db["SINASRV_DB${key}_NAME"])) {
        return true;
    }
    if(empty($db["SINASRV_DB${key}_HOST"]) ||
       empty($db["SINASRV_DB${key}_NAME"])) {
        $db_res['connect_info'] = "NO";
        return false;
    }
    $db_res['connect_info'] = "OK";
    if(!preg_match("/\d+\.\d+\.\d+\.\d+/", $db["SINASRV_DB${key}_HOST"])) {
        $db_res['wdomain'] = $db["SINASRV_DB${key}_HOST"];
	if(stripos($db_res['wdomain'],'m4392') !== false) return true; //Special auth DB.Exclude from common mon. By shangbin
        $db_res['wip'] = gethostbyname($db_res['wdomain']);
        if($db_res['wdomain'] == $db_res['wip']) {
            $db_res['wip'] = "NO";
            return false;
        }
    } else {
        $db_res['wip'] = $db["SINASRV_DB${key}_HOST"];
    }
    $db_res['dbname'] = $db["SINASRV_DB${key}_NAME"];
    // connect to mysql
    $link = @mysql_connect($db_res['wip'].":".$db["SINASRV_DB${key}_PORT"],
        $db["SINASRV_DB${key}_USER"], $db["SINASRV_DB${key}_PASS"]);
    if (!$link) {
        $db_res['connect'] = 'ErrNo: ' . mysql_errno() . ', ' . mysql_error();
        return false;
    } else {
	if(!@mysql_select_db($db["SINASRV_DB${key}_NAME"])) {
		$db_res['connect'] = 'ErrNo: ' . mysql_errno() . ', ' . mysql_error();
		return false;
	} else {
	        $db_res['connect'] = "OK";
	}
    }
/*
    // use dbname;
    if (!@mysql_select_db($db["SINASRV_DB${key}_NAME"])) {
        $db_res['usedb'] = 'ErrNo: ' . mysql_errno() . ', ' . mysql_error();
        @mysql_close($link);
        return false;
    } else {
        $db_res['usedb'] = "OK";
    }
    // create table
    $sql = "CREATE TABLE IF NOT EXISTS dpool_check_db (
        id INT(10)  UNSIGNED NOT NULL AUTO_INCREMENT,
        name        CHAR(20) NOT NULL,
        time        int     NOT NULL,
        PRIMARY KEY(id)
        )";
    $res = @mysql_query($sql, $link);
    if (!$res) {
        $db_res['create_table'] = 'ErrNo: ' . mysql_errno() . ', ' . mysql_error();
        @mysql_close($link);
        return false;
    } else {
        $db_res['create_table'] = "OK";
    }
    // delete record from table
    $sql = "DELETE FROM dpool_check_db";
    $res = @mysql_query($sql, $link);
    if (!$res) {
        $db_res['delete_record'] = 'ErrNo: ' . mysql_errno() . ', ' . mysql_error();
        @mysql_close($link);
        return false;
    } else {
        $db_res['delete_record'] = "OK";
    }
    // insert record into table
    $sql = "INSERT INTO dpool_check_db(name, time) values('tongjian', " . time() . ")";
    $res = @mysql_query($sql, $link);
    if (!$res) {
        $db_res['insert_record'] = 'ErrNo: ' . mysql_errno() . ', ' . mysql_error();
        @mysql_close($link);
        return false;
    } else {
        $db_res['insert_record'] = "OK";
    }
*/
    @mysql_close($link);
    return true;
}

function test_db_r($key, &$db, &$db_res) {
    if($key == 0) $key = "";

    if(!empty($db["SINASRV_DB${key}_HOST_R"]) &&
        empty($db["SINASRV_DB${key}_NAME_R"])) {
        return true;
    }

    if(empty($db["SINASRV_DB${key}_HOST_R"]) ||
       empty($db["SINASRV_DB${key}_NAME_R"])) {
        $db_res['connect_info'] = "NO";
        return false;
    }
    $db_res['connect_info'] = "OK";
    if(!preg_match("/\d+\.\d+\.\d+\.\d+/", $db["SINASRV_DB${key}_HOST_R"])) {
        $db_res['rdomain'] = $db["SINASRV_DB${key}_HOST_R"];
	if(stripos($db_res['rdomain'],'s4392') !== false) return true; //Special auth DB.Exclude from common mon. By shangbin
        $db_res['rip'] = gethostbyname($db_res['rdomain']);
        if($db_res['rdomain'] == $db_res['rip']) {
            $db_res['rip'] = "NO";
            return false;
        }
    } else {
        $db_res['rip'] = $db["SINASRV_DB${key}_HOST_R"];
    }
    $db_res['dbname'] = $db["SINASRV_DB${key}_NAME_R"];
    // connect to mysql
    $link = @mysql_connect($db_res['rip'].":".$db["SINASRV_DB${key}_PORT_R"],
        $db["SINASRV_DB${key}_USER_R"], $db["SINASRV_DB${key}_PASS_R"]);
    if (!$link) {
        $db_res['connect'] = 'ErrNo: ' . mysql_errno() . ', ' . mysql_error();
        return false;
    } else {
	if(!@mysql_select_db($db["SINASRV_DB${key}_NAME_R"])) {
		$db_res['connect'] = 'ErrNo: ' . mysql_errno() . ', ' . mysql_error();
		return false;
	} else {
	        $db_res['connect'] = "OK";
	}
    }
/*
    // use dbname;
    if (!@mysql_select_db($db["SINASRV_DB${key}_NAME_R"])) {
        $db_res['usedb'] = 'ErrNo: ' . mysql_errno() . ', ' . mysql_error();
        @mysql_close($link);
        return false;
    } else {
        $db_res['usedb'] = "OK";
    }
    // select records from table
    $sql = "SELECT time FROM dpool_check_db limit 1";
    $res = @mysql_query($sql, $link);
    if (!$res) {
        $db_res['select_record'] = 'ErrNo: ' . mysql_errno() . ', ' . mysql_error();
        return false;
    } else {
        $num_rows = @mysql_num_rows($res);
        if($num_rows == NULL) {
            $db_res['select_record'] = "NULL";
            return false;
        } else {
            $db_res['time'] = @mysql_result($res, 0);
            $difftime = time() - $db_res['time'];
            if ($difftime > 60) {
                $db_res['select_record'] = "DB replication delayed";
                return false;
            }
            $db_res['select_record'] = "OK";
        }
    }

*/
    @mysql_close($link);
    return true;
}

function test_dir($path)
{
    global $info;
    $info = "";

    if (@is_dir($path))
    {
        $type = "d";
    }
    else if (@is_file($path))
    {
        $type = "f";
    }
    else
    {
        $info = "$path has problem";
        return false;
    }
/*
    $res = @stat($path);
    if ($res === false)
    {
        return "unstatable";
    }

    return sprintf("mode:%s0%o uid:0x%04x gid:0x%04x time:%s", $type, $res[2],
        $res[4], $res[5], date("YmdHis", $res[9]));
*/
    if($type == "d") {
        $last = substr($path, -1, 1);
        $testfile = $last == "/" ?
                    $path . "dpool_check_" . randstr(10) :
                    $path . "/dpool_check_" . randstr(10);
    } else if($type == "f") {
        $testfile = $path;
    } else {
        $testfile = "";
    }
    $testcontent = "test file rw";
    $length = strlen($testcontent);
    if(!$handle = fopen($testfile, 'w+')) {
        $info = "cannot open file in $path.";
        return false;
    }
    if(fwrite($handle, $testcontent) == false) {
        unlink($testfile);
        fclose($handle);
        $info .= "cannot write file $testfile.";
        return false;
    }
    fseek($handle, 0);
    $contents = fread($handle, $length);
    if($contents != $testcontent) {
        unlink($testfile);
        fclose($handle);
        $info .= "cannot read file $testfile.";
        return false;
    }
    fclose($handle);
    if(!unlink($testfile)) {
        $info .= "cannot delete file $testfile";
        return false;
    }

    $info .= "$path can be read and written,";

    return true;
}

function get_cgi_var($key, &$value, $default = NULL)
{
    if (!empty($_GET[$key]))
    {
        $value = $_GET[$key];
    }
    else if (!empty($_POST[$key]))
    {
        $value = $_POST[$key];
    }
    else if (!empty($_COOKIE[$key]))
    {
        $value = $_COOKIE[$key];
    }
    else
    {
        if (!is_null($default)) $value = $default;
        return false;
    }

    return true;
}

function test_session($act = "")
{
    $session_key = "session_testkey";
    $session_value = "session_testvalue";

    $session_name = session_name();
    @session_start();
    $session_id = @session_id();

    if ($act == "get_session")
    {
        $res = $_SESSION[$session_key];
        echo $res;
        return;
    }

    $_SESSION[$session_key] = $session_value;
    session_write_close();

/*
    $url = "http://".$_SERVER['SERVER_NAME'].$_SERVER['PHP_SELF'];
    $url .= "?" . $session_name . "=" . $session_id;
    $url .= "&act=get_session";
    $res = @file_get_contents($url);
*/

    /// Try another way
    $head = "GET ".$_SERVER['SCRIPT_NAME']."?act=get_session HTTP/1.1\r\n";
    $head .= "Host: ".$_SERVER['SERVER_NAME']."\r\n";
    $head .= "Cookie: ".$session_name."=".$session_id."\r\n";
    $head .= "\r\n";

    $res = http_request($head);

    if ($res == "FAIL")
    {
        return false;
    }
    else if (eregi($session_value, $res))
    {
        return true;
    }
    else
    {
        return false;
    }
}

function http_request($body)
{
    $fp = @fsockopen("127.0.0.1", "80", $errno, $errstr);
    if (!$fp)
    {
        return "FAIL";
    }

    $size = strlen($body);
    $blocksize = 1024;
    $pos = 0;
    while($pos < $size)
    {
        $written = @fwrite($fp, substr($body, $pos, $blocksize));
        if ($written === false) break;
        $pos += $written;
    }

    if ($written === false)
    {
        return "FAIL";
    }

    $body = "";
    $eat = false;
    while(!feof($fp))
    {
        $line = fgets($fp);
        if (!$eat && ereg("^\r?\n$", $line))
        {
            $eat = true;
            continue;
        }

        if ($eat) $body .= $line;
    }

    fclose($fp);
    return $body;
}

function test_upload($act = "")
{
    $file_key = "file_testkey";
    $file_name = "hello.txt";
    $file_content = "OK";

    if ($act == "get_file")
    {
        $get_file = $_FILES[$file_key]['tmp_name'];
        $get_size = $_FILES[$file_key]['size'];
        $get_name = $_FILES[$file_key]['name'];

        if ($get_name == $file_name && $get_size > 0 && is_readable($get_file))
        {
            echo "OK";
        }
        else
        {
            echo "NO";
        }

        return;
    }

    $boundary = 'UPLOADTEST_' . md5(uniqid('request') . microtime());
    ///////////////////////////////////////////
    $head = "POST ".$_SERVER['PHP_SELF']."?act=get_file HTTP/1.1\r\n";
    $head .= "Content-Type: multipart/form-data; boundary={$boundary}\r\n";
    $head .= "User-Agent: SinaTestAgent\r\n";
    $head .= "Host: ".$_SERVER['SERVER_NAME']."\r\n";
    $head .= "Connection: close\r\n";
    //////////////////////////////////////////
    $postdata = "--{$boundary}\r\n";
    $postdata .= "Content-Disposition: form-data; name=\"{$file_key}\"; filename=\"{$file_name}\"\r\n";
    $postdata .= "Content-Type: application/octet-stream\r\n\r\n";
    $postdata .= $file_content."\r\n";
    $postdata .= "--{$boundary}\r\n";
    ////////////////////////////////////////
    $head .= "Content-Length: ".strlen($postdata)."\r\n\r\n";
    $body = $head.$postdata;

    //echo $body;exit;
    $res = http_request($body);
    if ($res == "FAIL")
    {
        return false;
    }
    else if (eregi("OK", $res))
    {
        return true;
    }
    else
    {
        return false;
    }
}

function dispatch_act($act)
{
    if ($act == "get_file")
    {
        test_upload($act);
        exit(0);
    }
    else if ($act == "get_session")
    {
        test_session($act);
        exit(0);
    } 
}

function test_vfs($act, $from)
{
    global $g_func;
    require_once 'VFS/VFS/dpool_storage.php';
    $dStorage = new VFS_dpool_storage();

    if ($act == "write_vfs")
    {
        $ret = $dStorage->writeData("/dpoolcheck", "vfs-$from", time());
        if(is_a($ret, 'PEAR_Error'))
        {
            $g_func['vfs'] = "Error when write VFS!";
            return false;
        }
    } else if ($act == "read_vfs")
    {
        $ret = $dStorage->read("/dpoolcheck", "vfs-$from");
        if(is_a($ret, 'PEAR_Error'))
        {
            #ob_start();
            #print_r($ret);
            $g_func['vfs'] = "Error when read VFS!";
            #ob_end_clean();
            return false;
        } else if (time() - $ret > 500)
        {
            $g_func['vfs'] = "vfs sync delayed too long!";
            return false;
        }
    }
    else
    {
        $g_func['vfs'] = "Not Supported Actions:$act, vfs check supports only actions such as 'write_vfs' or 'read_vfs'!";
        return false;
    }

    $g_func['vfs'] = 'OK';
    return true;
}

function get_intip() {
	$shellfp = popen("/sbin/ip addr show | awk '/inet / {print $2}' |grep -v 127.0.0.1 |cut -d'/' -f1",'r');
	$ips = current(split("\n", fread($shellfp,4096)));
	pclose($shellfp);
        $ipsconf = "/etc/dAppCluster/dpoolips.conf";
        $confarray = parse_ini_file($ipsconf);
        if(!is_array($confarray)) die();
        $iipb = explode(" ",rtrim($confarray["INTIP_B"]));
        $iipc = explode(" ",rtrim($confarray["INTIP_C"]));
        foreach ($ips as $ip) {
                $splitip = explode(".",$ip);
                $ip_b = $splitip[0].".".$splitip[1];
                $ip_c = $splitip[0].".".$splitip[1].".".$splitip[2];
                if(in_array($ip_b,$iipb) || in_array($ip_c,$iipc))
                        return $ip;
        }
}

function test_vfs_rw()
{
    global $g_vfsrw;
    require_once 'VFS/VFS/dpool_storage.php';
    $dStorage = new VFS_dpool_storage();
    $myip = get_intip();
    $error = 0;
    $content = time();
    $ret = $dStorage->writeData("/dpoolcheck", "vfs-rwtest-${myip}", $content);
    if($ret === 'Not found module') {
        $g_vfsrw['vfsrw'] = "OK";
	return true;
    }
    if($ret != 1)
    {
        $g_vfsrw['vfswrite'] = "Error when writing VFS!";
	$error = 1;
    }
    $ret = $dStorage->read("/dpoolcheck", "vfs-rwtest-${myip}");
    if(!($ret))
    {
        $g_vfsrw['vfsread'] = "Error when reading VFS!";
	$error = 1;
    } 
    if($error == 0) {
	    $g_vfsrw['vfscheck'] = 'OK';
	    return true;
    } else {
	    $g_vfsrw['vfscheck'] = 'NO';
	    return false;
    }
}


function test_memcache()
{
    global $g_mc;
    if(!array_key_exists('SINASRV_MEMCACHED_SERVERS', $_SERVER)) {
        $g_mc['connect info'] = 'NO';
        return false;
    } else {
        $g_mc['connect info'] = $_SERVER['SINASRV_MEMCACHED_SERVERS'];
    }
    $memcached_servers = split(' ', $_SERVER['SINASRV_MEMCACHED_SERVERS']);
    $memcached_key_prefix = $_SERVER['SINASRV_MEMCACHED_KEY_PREFIX'];

    $memcache = new Memcache;
    foreach ($memcached_servers as $memcached) {
        list($server, $port) = split(':', $memcached);
        $memcache->addServer($server, $port, FALSE);
    }

    $key = $memcached_key_prefix . rand();
    $content = $key;

    for($i=0;$i<3;$i++) {
        $ret=$memcache->set($key, $content, MEMCACHE_COMPRESSED, 20);
        if(!$ret) {
            $g_mcl['set'] = 'NO';
            sleep(1);
            continue;
        } else {
            $g_mcl['set'] = 'OK';
            break;
        }
    }

    if ($g_mcl['set'] == 'OK') {
        for($i=0;$i<3;$i++) {
            $cont = $memcache->get($key);
            if ($cont === false) { $g_mcl['get'] = 'NO'; sleep(1);continue; }
            else if ($cont == $content) { $g_mcl['get'] = 'OK'; break; }
            else { $g_mcl['get'] = 'Content Not Match'; sleep(1);continue; }
        }
    } else {
        return false;
    }

    if($g_mcl['get'] != "OK") {
        return false;
    } else {
        return true;
    }

    return true;
}

function test_memcache_localhost()
{
    global $g_mcl;
    if(!array_key_exists('SINASRV_MEMCACHED_HOST', $_SERVER) || !array_key_exists('SINASRV_MEMCACHED_PORT', $_SERVER)) {
        $g_mcl['connect info'] = 'NO';
        return false;
    } else {
        $g_mcl['connect info'] = $_SERVER['SINASRV_MEMCACHED_HOST'] . ":" . $_SERVER['SINASRV_MEMCACHED_PORT'];
    }

    $memcache = new Memcache;
    $memcache->addServer($_SERVER['SINASRV_MEMCACHED_HOST'], $_SERVER['SINASRV_MEMCACHED_PORT'], FALSE);

    $key = $memcached_key_prefix . rand();
    $content = $key;

    if ($memcache->set($key, $content, MEMCACHE_COMPRESSED, 10)) {
        $g_mcl['set'] = 'OK';
    } else {
        $g_mcl['set'] = 'NO';
        return false;
    }
    if ($g_mcl['set'] == 'OK') {
        $cont = $memcache->get($key);
        if ($cont === false) { $g_mcl['get'] = 'NO'; return false; }
        else if ($cont == $content) { $g_mcl['get'] = 'OK'; }
        else { $g_mcl['get'] = 'Content Not Match'; return false; }
    }

    return true;
}

function gen_xml($resource_name, $resource_err, $resource_info, $start, $end) {
    return "<resource><name>$resource_name</name><errno>$resource_err</errno><info>$resource_info</info><starttime>$start</starttime><endtime>$end</endtime></resource>";
}

function dump_array(&$array) {
    $array_ret = "Array\n(";
    foreach ($array as $k => $v) {
        $array_ret .= "\t[$k] => $v\n";
    }
    $array_ret .= ")";
    return $array_ret;
}

function current_time() {
    return date("Y-m-d H:i:s");
}

function getr($i)
{
        $seedarray =microtime()+$i;
        $seedstr =split(" ",$seedarray,5);
        $seed =$seedstr[0]*10000;
        srand($seed);
        $random =rand(10,99);
        return $random;
}

function randstr($l)
{
        $s='';
        $i=0;
        while(strlen($s)<15){
                $i=getr($i);
                $s.=$i;
        }
        $i=strlen($s);
        return substr($s,$i-$l,$l);
}

//////////////////////////////////////////////////////
// main

get_cgi_var("act", $g_act);
dispatch_act($g_act);

// check vfs
if ($g_act == 'write_vfs' || $g_act == 'read_vfs') {
    get_cgi_var("from", $g_from);
    $errno = true;
    $start_time = current_time();
    $errno = test_vfs($g_act, $g_from);
    $end_time = current_time();
    $errno = $errno ? 0:1;
    $xmlret .= gen_xml($g_act, $errno, $g_func['vfs'], $start_time, $end_time);

    $xmlret .= "</xml>";
    echo $xmlret;
    exit(0);
}

get_env_variables();

// apache env check
$SINASRV_CONFIG = "$_SERVER[DOCUMENT_ROOT]/system/SINASRV_CONFIG";
$env_info = "";
$start_time = current_time();
$errno = read_sinasrv_config($SINASRV_CONFIG);
if($errno) $errno = test_env_match();
$end_time = current_time();
$errno = $errno ? 0:1;
if ($env_info == "") $env_info = "OK";
$xmlret .= gen_xml("apache env check", $errno, $env_info, $start_time, $end_time);

// check storage
$start_time = current_time();
$errno = true;
foreach($g_env_dir as $k => $v)
{
    $errno =  test_dir($v['dir']);
    $g_env_dir[$k]['status'] = $info;
    if($errno == false) break;
}
$end_time = current_time();

foreach($g_env_dir as $k => $v) {
    if ($g_env_dir[$k]['status'] === '') continue;
    $storage_info .= $g_env_dir[$k]['status'] . "\n";
}
$errno = $errno ? 0:1;
$xmlret .= gen_xml("storage check", $errno, $storage_info, $start_time, $end_time);

// check database
$errno = true;
foreach($g_env_dbw as $k => $v) {
    // check multiple write dbs
    $start_time = current_time();
    $errno = test_db_w($k, $v, $g_dbw[$k]);
    $end_time = current_time();
    $errno = $errno ? 0:1;
    $xmlret .= gen_xml("the ${k}th group write db check", $errno, dump_array($g_dbw[$k]), $start_time, $end_time);
    if(errno == 1) continue;

    // check read db immediatly
    $delay_limit = 20000000;
    $delay_total = $delay_limit;
    $delay = 1000000;
    $start_time = current_time();
    usleep(10000);
    $errno = test_db_r($k, $g_env_dbr[$k], $g_dbr[$k]);
/*
    while($delay_total > 0) {
        usleep(150000);
        if($errno = test_db_r($k, $g_env_dbr[$k], $g_dbr[$k])) break;
        usleep($delay);
        $delay = $delay * 2;
        $delay_total -= $delay;
    }
*/
    $end_time = current_time();
    //$g_dbr[$k]['sync_time'] = ($delay_limit - $delay_total)/1000 . "ms";
    $errno = $errno ? 0:1;
    $xmlret .= gen_xml("the ${k}th group read db check", $errno, dump_array($g_dbr[$k]), $start_time, $end_time);
}

// check session rw
$errno = true;
$start_time = current_time();
if($errno = test_session()) {
    $g_func['session'] = "OK";
} else {
    $g_func['session'] = "NO";
}
$end_time = current_time();
$errno = $errno ? 0:1;
$xmlret .= gen_xml("session check", $errno, $g_func['session'], $start_time, $end_time);

// check upload file
if($_SERVER['SERVER_NAME'] == "vip.book.sina.com.cn" ||
$_SERVER['SERVER_NAME'] == "nba.sports.sina.com.cn") {
$errno = true;
$start_time = current_time();
if($errno = test_upload()) {
    $g_func['upload'] = "OK";
} else {
    $g_func['upload'] = "NO";
}
$end_time = current_time();
$errno = $errno ? 0:1;
$xmlret .= gen_xml("upload check", $errno, $g_func['upload'], $start_time, $end_time);
}
// check memcache
$errno = true;
$start_time = current_time();
$errno = test_memcache();
$end_time = current_time();
$errno = $errno ? 0:1;
$xmlret .= gen_xml("memcached check", $errno, dump_array($g_mc), $start_time, $end_time);

// check localhost memcache
if($_SERVER['SERVER_NAME'] == "vip.book.sina.com.cn" ||
$_SERVER['SERVER_NAME'] == "nba.sports.sina.com.cn") {
$errno = true;
$start_time = current_time();
$errno = test_memcache_localhost();
$end_time = current_time();
$errno = $errno ? 0:1;
$xmlret .= gen_xml("localhost memcached check", $errno, dump_array($g_mcl), $start_time, $end_time);
}

// check vfs read

if($_SERVER['SERVER_NAME'] == 'vip.book.sina.com.cn') {
$errno = true;
$start_time = current_time();
$errno = test_vfs_rw();
$end_time = current_time();
$errno = $errno ? 0:1;
$xmlret .= gen_xml("vfs rw check", $errno, dump_array($g_vfsrw), $start_time, $end_time);
}

$xmlret .= "</xml>";
echo $xmlret;


// change log
// 2006-05-17 add special env varibles:SINASRV_SERVER_NAME,SINASRV_DOCUMENT_ROOT,DOCUMENT_ROOT,SINASRV_SERVER_PORT
// 2006-05-18 fix SINASRV_DB_HOST(_R) problem, and a bug that is caused by errno.
// 2006-05-18 fix a regular bug.
// 2006-05-24 fix a regular bug: ereg("^\r?\n$", $line)
// 2006-05-24 add SINASRV_CGIBIN_DIR to special env array.
// 2006-05-25 fix apache env check return
// 2006-06-06 fix storage check return
// 2006-06-23 fix a bug of generating a random filename in function test_dir()
// 2006-07-25 fix a problem of regarding "SINASRV_CGIBIN_DIR" as storage
// 2006-07-31 improve the check of db, display db's IP.
// 2006-08-02 display the detailed error messages of mysql
// 2007-04-05 improve the write_db check.(not drop table again)
// 2007-05-10 add vfs check
// 2007-05-15 fix a bug that insert error will skip
// 2007-06-04 fix a bug that read NULL record from slave db.
// 2007-07-09 fix bugs of db syncing check
// 2007-09-04 set master/slave db sync to 20s
// 2007-11-27 add memcached check
// 2008-08-16 add localhost memcached check
// 2008-11-26 disable SINASRV_NDATA_DIR check

