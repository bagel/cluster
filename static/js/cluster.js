function numberFix(n, m) {
    if (n / 100000000 > 1) {
        n = (n / 100000000).toFixed(m) + "亿";
    } else if (n / 10000 > 1) {
        n = (n / 10000).toFixed(m) + "万";
    } else {
        n = n.toFixed(0);
    }   
    return n;
}

function dateFormat(t) {
    var d = new Date(parseInt(t) * 1000);
    var year = d.getFullYear(),
        month = d.getMonth() + 1 < 10 ? '0' + (d.getMonth() + 1) : (d.getMonth() + 1),
        day = d.getDate() < 10 ? '0' + d.getDate() : d.getDate(),
        hour = d.getHours() < 10 ? '0' + d.getHours() : d.getHours(),
        minute = d.getMinutes() < 10 ? '0' + d.getMinutes() : d.getMinutes(),
        second = d.getSeconds() < 10 ? '0' + d.getSeconds() : d.getSeconds();
    return [year, month, day, hour, minute, second];
}

function page(s, url, num, id, func) {
    $.getJSON(url, function(jsonData) {
        var pagehtml = "";
        count = jsonData["count"];
        if ( count < num ) {
            var pageMax = 0;
        } else if ( count % num != 0 ) {
            var pageMax = Math.floor(count / num + 1);
        } else {
            var pageMax = count / num;
        }
        if (!s) {
            s = 1;
        }
        if (s == 1) {
            if ( pageMax != 0 ) {
                pagehtml += '<li class="disabled"><a>1</a></li>';
            }
        } else {
            pagehtml += '<li><a onclick=' + func + '(' + (s - 1) + ')>&laquo;</a></li>';
            pagehtml += '<li><a onclick=' + func + '(1)>1</a></li>';
            if ( s != 2 ) {
                pagehtml += '<li class="disabled"><a>...</a></li>';
            }
        }
        if ( s != 1 && s != pageMax) {
            pagehtml += '<li class="disabled"><a>' + s + '</a></li>';
        }
        if ( pageMax > 1) {
            if ( s == pageMax ) {
                pagehtml += '<li class="disabled"><a>' + pageMax + '</a></li>';
            } else {
                if ( s != (pageMax - 1) ) {
                    pagehtml += '<li class="disabled"><a>...</a></li>';
                }
                pagehtml += '<li><a onclick=' + func + '(' + pageMax + ')>' + pageMax + '</a></li>';
                pagehtml += '<li><a onclick=' + func + '(' + (s + 1) + ')>&raquo;</a></li>';
            }
        }
        document.getElementById(id).innerHTML = pagehtml;
    });
}

function pageContent(s, url, num, id, func) {
    if(!s) {
        s = 1;
    }
    var st = (s - 1) * num;
    var url = url + "?num=" + num.toString() + "&start=" + st;
    $.getJSON(url, function(jsonData) {
        var contenthtml = "";
        for (i in jsonData) {
            contenthtml += "<tr>";
            for (j in jsonData[i]) {
                contenthtml += "<td>" + jsonData[i][j] + "</td>";
            }
            contenthtml += "</tr>";
        }
        document.getElementById(id).innerHTML = contenthtml;
    });
    func(s);
}

