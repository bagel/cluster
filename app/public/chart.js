var page = require('webpage').create(),
    system = require('system'),
    fs = require('fs');

page.customHeaders = {
    "Cookie": "DP_token=Y2FveXUyLjEzOTg5MTc2NjIuNDllZmY=",
};

page.viewportSize = { "width": 1600, "height": 900 };

var url = system.args[1];
var tmpfile = system.args[2];


function waitChart(n) {
    setTimeout(function() {
        var chart = page.evaluate(function() {
            return document.getElementById("chartContainer").innerHTML;
        });
        var s1 = chart.search('<svg'),
            s2 = chart.search('</svg>'),
            svg_xml = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
            svg = svg_xml + chart.slice(s1, s2) + '</svg>';
        //console.log(chart);
        fs.write(tmpfile, svg, "w");
        phantom.exit();
    }, n);
}


page.open(url, function(status) {
    if (status != "success") {
        console.log("failed");
        phantom.exit();
    }
    waitChart(1000);
});
