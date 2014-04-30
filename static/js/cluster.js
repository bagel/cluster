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
    return [year, month, day, hour, minute, second]
}

