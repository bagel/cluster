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

function postJSON(postUrl, postData) {
    $.ajax({
        async: false,
        type: "POST",
        url: postUrl,
        data: postData,
        dataType: "json",
        contentType: "application/json",
        success: function() { alert("完成"); }
    });
}

function chartsTemplate(chartid){
    if (!chartid) {
        chartid = "#chartContainer";
    }

    $(function () {
        $(document).ready(function() {
            Highcharts.theme = {
               colors: ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
               chart: {
                  backgroundColor: {
                     linearGradient: { x1: 0, y1: 0, x2: 1, y2: 1 },
                     stops: [
                        [0, 'rgb(255, 255, 255)'],
                        [1, 'rgb(240, 240, 255)']
                     ]
                  },
                  borderColor: '#e3e3e3',
                  borderWidth: 2,
                  plotBackgroundColor: 'rgba(255, 255, 255, .9)',
                  plotShadow: true,
                  plotBorderWidth: 1
               },
               title: {
                  style: {
                     color: '#000',
                     font: '14px "Trebuchet MS", Verdana, sans-serif'
                  }
               },
               subtitle: {
                  style: {
                     color: '#666666',
                     font: 'bold 12px "Trebuchet MS", Verdana, sans-serif'
                  }
               },
               xAxis: {
                  gridLineWidth: 1,
                  lineColor: '#000',
                  tickColor: '#000',
                  labels: {
                     style: {
                        color: '#000',
                        font: '11px Trebuchet MS, Verdana, sans-serif'
                     }
                  },
                  title: {
                     style: {
                        color: '#333',
                        fontWeight: 'bold',
                        fontSize: '12px',
                        fontFamily: 'Trebuchet MS, Verdana, sans-serif'
            
                     }
                  }
               },
               yAxis: {
                  //minorTickInterval: 'auto',
                  lineColor: '#000',
                  lineWidth: 1,
                  tickWidth: 1,
                  tickColor: '#000',
                  labels: {
                     style: {
                        color: '#000',
                        font: '11px Trebuchet MS, Verdana, sans-serif'
                     }
                  },
                  title: {
                     style: {
                        color: '#333',
                        fontWeight: 'bold',
                        fontSize: '12px',
                        fontFamily: 'Trebuchet MS, Verdana, sans-serif'
                     }
                  }
               },
               legend: {
                  itemStyle: {
                     font: '9pt Trebuchet MS, Verdana, sans-serif',
                     color: 'black'
            
                  },
                  itemHoverStyle: {
                     color: '#039'
                  },
                  itemHiddenStyle: {
                     color: 'gray'
                  }
               },
               labels: {
                  style: {
                     color: '#99b'
                  }
               },
            
               navigation: {
                  buttonOptions: {
                     theme: {
                        stroke: '#CCCCCC'
                     }
                  }
               }
            };
    
            Highcharts.setOptions({
                global: {
                    useUTC: false
                }
            });
    
            Highcharts.setOptions(Highcharts.theme);

    
            $(chartid).highcharts({
                chart: {
                    type: "spline",
                    plotBorderWidth: 0,
                },
                title: {
                    text: "null",
                },
                xAxis: {
                    type: "datetime",
                    tickPixelInterval: 150,
                    dateTimeLabelFormats: {
                        day: "%m/%d %H:%M",
                    }
                },
                yAxis: {
                    title: {
                        text: "hits/s",
                    },
                    min: -2,
                    startOnTick: false
                },
                credits: {
                    enabled: false,
                    text: ''
                },
                plotOptions: {
                    spline: {
                        /*events: {
                            legendItemClick: function() {
                                location.href = "http://" + location.hostname + "/status";
                            }
                        },*/
                        marker: {
                            enabled: false
                        },
                        states: {
                            hover: {
                                enabled: true
                            }
                        }
                    },
                    series: {
                        cursor: "pointer",
                        turboThreshold: 3000,  //最大点数
                        /*events: {
                            click: function() {
                                location.href = "http://" + location.hostname + "/mon/data";
                            }
                        }*/
                    },
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + Highcharts.dateFormat('%m/%d %H:%M', this.x) + 
                               '</b><br/>' + this.series.name + ': ' +
                               Highcharts.numberFormat(this.y, 0);
                    }
                },
                series: [],
            });
    
        });
    });
}


function chartsData(urls, chartid, maxTitle, single) {
    if (!chartid) {
        chartid = "#chartContainer";
    }
    if (!single) {
        single = 0;
    }

    var chart = $(chartid).highcharts(),
        title = "",
        mark = "|";

    if (single == 0) {
        var mark = "";
    }

    $.each(urls, function(n, url) {
        var tail = "_url" + n;
        if (urls.length == 1) {
            tail = "";
        }
        $.getJSON(url, function(data) {
            if (single == 0) {
                while (chart.series.length > 0) {
                    chart.series[0].remove(true);
                }
                chart.counters.color = 0;
                chart.counters.symbol = 0;
            }
            var datas = data["data"],
                sumDatas = {};
            for (var i in datas) {
                $.each(datas[i], function(xAxis, values) {
                    var maxData = 0,
                        maxDate = "",
                        sumData = 0; 
                    chart.addSeries({
                        name: xAxis + tail,
                        data: (function() {
                            var data = [];
                            for (var j in values) {
                                var k = parseInt(values[j][0]),
                                    v = parseInt(values[j][1]);
                                if (maxData < v) {
                                    maxDate = k;
                                    maxData = v;
                                }
                                data.push({
                                    x: k * 1000,
                                    y: (v ? parseInt(v) : 0) / 60
                                });
                                if (! v) {
                                    v = 0;
                                }
                                sumData += parseInt(v);
                            }
                            return data;
                        })()
                    });
                    maxDate = dateFormat(maxDate);
                    maxDate = maxDate[3] + ':' + maxDate[4];
                    sumDatas[xAxis] = {"maxData": numberFix(maxData / 60, 2), "maxDate": maxDate, "sumData": numberFix(sumData, 2)};
                    title += data["title"] + mark;
                    if (maxTitle) {
                        title += [title, sumDatas[xAxis]["maxData"], sumDatas[xAxis]["maxDate"], sumDatas[xAxis]["sumData"]].join(' ') + mark;
                    }
                    var title0 = 0;
                    if (title.substr(-1) == "|") {
                        title = title.slice(0, -1);
                        title0 = 1;
                    }
                    chart.setTitle({"text": title});
                    if (title0 == 1) {
                        title += "|";
                    }
                });
            }
        });
    });
    chart.redraw();
}
