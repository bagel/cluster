/*
 * @license FusionCharts JavaScript Library
 * Copyright FusionCharts Technologies LLP
 * License Information at <http://www.fusioncharts.com/license>
 *
 * @author FusionCharts Technologies LLP
 * @version fusioncharts/3.3.1-sr3.21100
 * @id fusionmaps.Morocco.20.10-30-2012 06:49:17
 */
FusionCharts(["private","modules.renderer.js-morocco",function(){var p=this,k=p.hcLib,n=k.chartAPI,h=k.moduleCmdQueue,a=k.injectModuleDependency,i="M",j="L",c="Z",f="Q",b="left",q="right",t="center",v="middle",o="top",m="bottom",s="maps",l=true&&!/fusioncharts\.com$/i.test(location.hostname),r=!!n.geo,d,e,u,g;
d=[{name:"Morocco",revision:20,creditLabel:l,standaloneInit:true,baseWidth:370,baseHeight:370,baseScaleFactor:10,entities:{"MA.GC":{outlines:[[i,2245,643,f,2239,648,2233,650,j,2233,650,f,2225,651,2215,657,2227,661,2243,684,2264,701,2270,701,2272,701,2290,685,2319,668,2325,664,2331,659,2339,643,2350,626,2350,625,2350,609,2348,598,2348,589,2341,582,2334,586,2326,592,j,2326,593,f,2326,593,2325,593,2321,595,2317,598,2311,603,2304,608,2303,609,2301,610,2296,613,2292,617,2289,620,2285,623,2281,625,2277,627,2276,628,2274,629,2267,631,2262,634,2261,636,2259,636,2254,637,2251,640,2250,641,2249,642,f,2247,642,2245,643,c]],label:"Grand Casablanca",shortLabel:"GC",labelPosition:[204.3,64.6],labelAlignment:[q,v],labelConnectors:[[i,2043,646,j,2278,646]]},"MA.CO":{outlines:[[i,2499,725,f,2468,720,2457,720,2447,705,2440,660,2437,649,2421,643,2413,640,2400,620,2397,617,2391,586,2388,576,2377,561,2370,574,2361,573,2361,573,2360,573,2360,574,2360,575,2359,575,2359,575,2351,577,2341,582,2348,589,2348,598,2350,609,2350,625,2350,626,2339,643,2331,659,2325,664,2319,668,2290,685,2272,701,2270,701,2264,701,2243,684,2227,661,2215,657,2209,661,2202,668,2202,668,2201,669,2202,670,2204,670,2201,670,2198,671,2197,671,2196,671,j,2198,671,f,2193,680,2184,705,2174,716,2174,728,2169,744,2169,750,2169,751,2169,752,j,2169,752,2185,816,f,2179,831,2177,839,j,2177,839,f,2177,840,2177,840,2201,845,2238,871,2282,904,2286,906,j,2286,906,f,2308,917,2316,916,2331,915,2348,925,2350,942,2353,946,2357,950,2360,953,2370,932,2384,917,2401,899,2405,891,2428,848,2469,848,2523,849,2533,850,2535,851,2535,851,2592,849,2608,840,j,2616,840,f,2608,836,2577,781,2559,750,2531,738,2529,737,2526,736,f,2504,726,2499,725,c]],label:"Chaouia-Ouardigha",shortLabel:"CO",labelPosition:[237.5,77.9],labelAlignment:[t,v]},"MA.DA ":{outlines:[[i,2149,688,f,2147,690,2141,694,2136,698,2124,698,2123,699,2122,700,2121,701,2119,701,2107,700,2106,702,2101,709,2093,716,2092,717,2090,719,2083,725,2076,733,2071,739,2063,745,2059,749,2055,752,2050,758,2045,762,2041,766,2038,770,2035,774,2033,777,2031,780,2031,785,2031,799,2022,800,2014,802,2013,807,2013,812,2003,814,1993,816,1991,823,1989,831,1983,836,1977,841,1973,844,1970,846,1969,848,1963,854,1952,859,1943,863,1936,873,1930,881,1924,888,1918,895,1918,911,1919,926,1916,937,1914,949,1913,950,1912,953,1911,957,1910,966,1910,975,1909,984,1908,992,1908,996,1906,998,1905,1001,1901,1005,1898,1009,1900,1015,1900,1016,1900,1017,j,1899,1017,1899,1025,f,1903,1031,1903,1038,1903,1039,1903,1040,1933,1051,1955,1057,1974,1068,1988,1077,2015,1082,2025,1086,2052,1096,2064,1096,2083,1096,2086,1089,2088,1083,2090,1053,2090,1051,2111,1030,2122,1019,2122,1018,2123,1016,2123,1006,2123,997,2110,983,2096,969,2096,963,2096,953,2120,923,2123,920,2136,913,2147,906,2150,900,2161,879,2166,858,2168,850,2175,843,2176,842,2176,840,2176,839,2177,838,2179,830,2185,815,j,2169,752,2169,751,f,2169,751,2169,750,2169,743,2174,727,2174,715,2184,705,2193,679,2198,671,j,2196,671,f,2186,673,2172,681,2166,678,2163,682,2160,687,2156,687,f,2152,687,2149,688,c]],label:"Doukkala-Abda",shortLabel:"DA",labelPosition:[204.8,88.6],labelAlignment:[t,v]},"MA.FB":{outlines:[[i,3151,561,f,3113,561,3107,577,3107,590,3097,600,3085,609,3081,613,3073,627,3069,632,3062,640,3047,640,3014,640,2999,581,2992,557,2991,557,2987,549,2971,552,2955,556,2948,549,2944,545,2940,537,2935,534,2924,527,2914,520,2904,508,2891,499,2881,501,2875,496,2866,485,2848,464,2836,461,2809,444,2792,448,2791,448,2791,448,2791,448,2792,448,j,2789,448,f,2790,448,2791,448,2790,448,2789,448,2770,444,2756,457,2751,463,2742,468,2756,482,2767,504,2783,536,2786,541,2787,558,2794,566,2812,590,2815,596,2816,599,2822,602,2828,604,2830,610,j,2835,642,f,2838,675,2839,685,2846,713,2846,718,2846,734,2859,751,2877,769,2879,775,2881,788,2897,802,2902,807,2920,806,j,2941,833,f,2950,842,2963,854,2972,867,2979,878,2984,882,3001,882,3024,882,3036,871,3037,871,3039,871,j,3039,860,f,3046,841,3079,813,3084,805,3113,777,3151,742,3191,745,3221,747,3246,743,3275,738,3275,727,3275,717,3236,685,3196,654,3196,646,3196,639,3211,631,3217,622,3229,613,3235,608,3235,598,3235,588,3223,579,3211,572,3209,570,3198,553,3190,546,f,3171,561,3151,561,c]],label:"Fès Boulemane",shortLabel:"FB",labelPosition:[299.4,68.9],labelAlignment:[t,v]},"MA.GB":{outlines:[[i,2683,320,f,2656,303,2638,298,2603,286,2580,278,j,2573,278,2573,301,f,2565,310,2565,320,2565,322,2564,325,2563,332,2563,340,2563,342,2562,344,2559,349,2555,357,2555,359,2554,360,2550,372,2543,382,2531,397,2524,417,2520,426,2513,430,2512,431,2511,432,2504,446,2500,451,2497,456,2493,458,2489,461,2485,463,2482,465,2480,465,2477,466,2476,470,2475,473,2476,476,2472,484,2463,494,2466,495,2468,495,2491,495,2537,478,2563,478,2585,481,2595,482,2620,502,2629,506,2636,509,2639,501,2650,494,2660,488,2663,488,2671,488,2683,492,j,2714,492,f,2713,487,2714,480,2716,473,2722,465,2728,454,2737,433,2740,425,2752,417,2788,394,2788,373,2788,366,2785,361,j,2779,365,f,2769,349,2737,350,f,2720,345,2683,320,c]],label:"Gharb Chrarda Béni Hssen",shortLabel:"GB",labelPosition:[262.2,39.4],labelAlignment:[t,v]},"MA.GE":{outlines:[[i,2327,1450,f,2327,1455,2323,1458,2316,1464,2315,1478,2315,1479,2313,1480,2302,1482,2298,1473,2294,1462,2280,1464,2273,1465,2265,1465,2252,1463,2243,1470,2242,1472,2240,1473,2234,1477,2235,1485,2229,1481,2225,1480,2219,1478,2213,1477,2205,1477,2199,1481,2197,1483,2193,1483,2190,1483,2187,1487,2181,1498,2171,1506,2169,1508,2167,1510,2159,1519,2145,1518,2140,1518,2138,1514,2138,1513,2135,1513,2122,1512,2117,1520,2117,1522,2115,1522,2104,1527,2090,1526,2080,1525,2070,1525,2066,1525,2062,1521,2060,1520,2059,1519,2057,1518,2055,1516,2052,1511,2047,1505,2034,1505,2031,1517,2030,1520,2027,1522,2019,1527,2016,1536,2015,1538,2015,1540,2015,1543,2011,1546,2004,1551,2003,1558,2001,1564,1999,1571,1998,1573,1998,1575,1997,1582,1994,1588,1993,1590,1993,1593,1992,1619,1996,1643,1997,1644,1997,1645,2000,1656,1988,1652,1981,1651,1979,1646,1978,1642,1973,1642,1959,1642,1948,1646,1945,1648,1942,1649,1936,1652,1934,1657,1933,1658,1930,1658,1921,1659,1914,1664,1913,1665,1910,1666,1905,1666,1900,1668,1892,1672,1878,1671,1847,1670,1815,1671,1813,1672,1811,1673,1806,1679,1800,1682,1798,1683,1796,1684,1790,1687,1783,1687,1780,1688,1778,1690,1768,1700,1760,1707,1748,1718,1730,1715,1709,1713,1696,1729,1695,1730,1689,1727,1683,1724,1674,1723,1666,1723,1659,1721,1652,1718,1649,1717,1647,1715,1647,1713,j,1645,1711,f,1636,1720,1618,1737,1613,1738,1609,1742,1608,1744,1606,1746,1599,1754,1592,1760,1584,1768,1581,1780,1579,1790,1570,1795,1569,1797,1568,1798,1560,1811,1543,1808,1540,1808,1539,1809,1537,1810,1534,1812,1533,1813,1531,1814,1527,1815,1524,1819,1510,1830,1495,1839,1471,1854,1457,1872,1451,1881,1442,1887,1435,1892,1428,1898,1420,1906,1410,1913,1401,1919,1395,1930,1393,1935,1391,1938,1388,1941,1382,1947,1380,1949,1378,1951,1370,1958,1358,1956,1355,1955,1355,1956,1355,1957,1355,1957,1353,1963,1353,1970,1353,1973,1354,1975,1356,1980,1357,1985,1358,1988,1359,1989,1369,2000,1376,2007,1378,2009,1378,2011,1379,2019,1386,2025,1388,2027,1390,2033,1392,2035,1394,2037,1401,2042,1396,2049,1395,2051,1394,2052,1384,2058,1382,2060,1380,2061,1378,2063,1376,2065,1374,2067,1369,2071,1354,2071,1339,2072,1334,2073,1329,2075,1322,2087,1316,2099,1314,2104,1312,2108,1310,2113,1303,2128,1295,2143,1293,2147,1289,2154,1286,2162,1279,2168,1272,2175,1267,2181,1262,2187,1259,2189,1243,2211,1238,2238,1238,2242,1237,2245,1232,2265,1217,2282,1215,2284,1213,2286,1195,2299,1183,2315,1169,2334,1148,2343,1144,2345,1141,2350,1139,2353,1143,2365,1147,2377,1144,2380,1141,2384,1147,2388,1153,2392,1147,2395,1141,2399,1145,2405,1152,2415,1155,2425,1157,2428,1157,2430,1158,2445,1158,2453,1159,2462,1166,2460,1174,2458,1170,2466,1167,2475,1175,2474,1183,2473,1193,2471,1195,2470,1197,2469,1205,2461,1213,2460,1226,2459,1233,2468,1234,2469,1235,2471,1238,2477,1242,2483,1244,2485,1245,2486,1250,2490,1258,2490,1259,2490,1260,2490,1296,2492,1326,2493,1358,2494,1402,2496,1446,2498,1495,2498,1544,2498,1593,2498,1640,2498,1688,2498,1735,2498,1783,2498,1831,2498,1880,2498,1929,2498,1978,2498,j,1980,2498,f,1980,2479,1980,2460,j,1980,2453,f,1980,2444,1980,2435,1980,2386,1980,2338,1980,2289,1980,2240,1980,2235,1979,2230,1978,2225,1981,2220,1985,2214,1980,2203,1976,2196,1971,2192,1959,2183,1960,2163,1960,2160,1961,2159,1965,2155,1965,2150,1965,2141,1971,2139,j,2460,1678,2481,1662,2483,1662,f,2498,1653,2520,1653,2517,1647,2518,1643,2520,1639,2521,1633,2523,1627,2523,1622,2523,1617,2524,1604,2525,1590,2525,1570,2525,1560,2526,1550,2531,1548,2533,1546,2536,1543,2537,1540,2538,1537,2539,1529,2540,1522,2534,1517,2532,1515,2530,1514,2524,1509,2521,1505,2520,1504,2519,1503,2514,1503,2509,1502,2508,1502,2507,1500,2506,1498,2506,1496,2505,1489,2510,1485,2511,1485,2511,1484,2514,1482,2515,1480,2515,1478,2517,1476,2518,1475,2518,1473,2522,1461,2520,1448,2520,1441,2515,1438,2497,1425,2483,1408,2480,1404,2476,1403,2474,1403,2472,1401,2463,1393,2450,1395,2447,1395,2443,1397,2440,1398,2437,1400,2433,1403,2427,1410,2422,1416,2416,1419,2412,1422,2403,1422,2395,1422,2393,1418,2392,1415,2390,1413,2385,1409,2378,1410,2374,1410,2370,1411,2364,1412,2358,1416,2357,1418,2355,1420,2353,1424,2348,1424,2347,1424,2345,1425,2336,1433,2330,1440,f,2326,1444,2327,1450,c]],label:"Guelmim Es Semara",shortLabel:"GE",labelPosition:[183.7,194.6],labelAlignment:[t,v]},"MA.LB":{outlines:[[i,1378,2010,f,1378,2009,1376,2007,1369,1999,1359,1989,1358,1987,1357,1985,1356,1980,1354,1974,1353,1972,1353,1970,1353,1963,1355,1956,1347,1958,1322,1972,1318,1971,1313,1971,1290,1971,1271,1978,1269,1979,1268,1979,1259,1979,1252,1984,1250,1985,1248,1985,1230,1985,1213,1988,1199,1990,1191,1994,1182,1998,1171,2001,1159,2003,1140,2002,1120,2000,1102,2009,1083,2018,1054,2022,1025,2027,995,2092,j,993,2092,f,981,2104,978,2119,978,2122,977,2125,975,2129,974,2132,973,2135,971,2138,966,2145,967,2155,967,2163,961,2168,959,2171,956,2187,953,2203,948,2214,942,2224,940,2228,938,2231,936,2238,935,2241,934,2244,933,2249,931,2253,928,2259,924,2266,923,2269,922,2272,922,2274,921,2275,910,2296,898,2315,896,2319,894,2322,893,2324,891,2325,890,2326,871,2337,851,2348,838,2350,825,2351,823,2352,811,2357,800,2362,793,2365,786,2369,784,2370,782,2371,779,2374,776,2376,762,2384,751,2395,740,2405,722,2410,704,2415,704,2422,703,2429,701,2432,694,2444,687,2452,685,2454,684,2456,683,2457,682,2460,682,2462,680,2465,676,2473,669,2485,668,2487,668,2490,669,2515,653,2530,646,2537,642,2547,639,2554,635,2560,631,2565,630,2572,630,2574,629,2576,627,2579,626,2582,623,2607,609,2628,604,2635,600,2642,598,2646,596,2650,593,2662,587,2673,585,2676,585,2680,585,2689,581,2698,580,2700,580,2702,580,2728,578,2755,578,2759,576,2763,575,2765,574,2767,573,2770,572,2771,572,2772,576,2775,579,2778,593,2779,606,2780,612,2783,617,2786,620,2791,622,2795,622,2805,623,2810,624,2815,624,2816,624,2816,624,2818,625,2821,632,2827,648,2826,661,2825,675,2825,690,2825,705,2822,707,2822,708,2820,710,2819,712,2817,716,2815,720,2813,723,2812,725,2811,728,2810,731,2808,733,2807,754,2805,775,2803,785,2811,795,2818,795,2821,795,2823,807,2830,821,2839,831,2846,834,2847,838,2847,846,2846,852,2839,858,2833,864,2828,865,2827,868,2827,874,2825,881,2823,884,2822,911,2815,937,2808,949,2811,962,2814,978,2815,993,2815,1003,2821,1013,2827,1018,2829,1023,2830,1028,2830,1034,2831,1040,2833,1042,2834,1043,2834,1047,2835,1051,2837,1057,2841,1061,2847,1061,2848,1063,2848,1065,2848,1066,2849,1075,2852,1088,2851,1113,2850,1138,2850,1173,2850,1208,2850,1209,2849,1210,2848,j,1210,2847,f,1210,2800,1210,2752,1210,2706,1210,2660,1210,2611,1210,2562,1210,2533,1210,2502,1211,2502,1212,2501,1223,2489,1245,2492,j,1245,2486,f,1244,2484,1242,2483,1238,2477,1235,2470,1234,2469,1233,2467,1226,2459,1213,2460,1205,2461,1197,2469,1195,2470,1193,2470,1183,2473,1175,2474,1167,2475,1171,2466,1174,2457,1167,2459,1159,2461,1159,2453,1158,2445,1157,2430,1157,2427,1155,2425,1152,2415,1145,2405,1141,2398,1147,2395,1153,2392,1147,2388,1141,2384,1144,2380,1147,2376,1143,2364,1139,2352,1141,2350,1144,2345,1148,2343,1169,2334,1183,2315,1195,2299,1213,2285,1215,2284,1217,2282,1232,2265,1237,2245,1238,2241,1238,2237,1243,2211,1259,2189,1262,2186,1267,2181,1272,2175,1279,2168,1286,2161,1290,2154,1293,2146,1295,2142,1303,2127,1310,2112,1312,2108,1314,2103,1316,2099,1323,2087,1329,2075,1334,2073,1339,2071,1354,2071,1369,2071,1374,2067,1376,2065,1378,2063,1380,2061,1382,2059,1384,2058,1394,2052,1395,2050,1396,2049,1401,2042,1394,2036,1392,2035,1390,2032,1388,2027,1386,2024,f,1379,2019,1378,2010,c]],label:"Laâyoune Boujdour Sakia El Hamra",shortLabel:"LB",labelPosition:[91,252.3],labelAlignment:[t,v]},"MA.MK":{outlines:[[i,2177,840,f,2177,840,2176,840,2176,842,2175,843,2168,850,2166,858,2161,879,2150,900,2147,906,2136,913,2123,920,2120,923,2096,953,2096,963,2096,969,2110,983,2123,997,2123,1006,2123,1016,2122,1018,2122,1019,2111,1030,2090,1051,2090,1053,2088,1083,2086,1089,2083,1096,2064,1096,2052,1096,2025,1086,2015,1082,1988,1077,1974,1068,1955,1057,1933,1051,1903,1040,1902,1044,1897,1052,1894,1057,1891,1060,1889,1062,1888,1062,1886,1062,1885,1062,1874,1066,1866,1078,1857,1090,1845,1097,1842,1100,1828,1120,1817,1136,1800,1151,1797,1153,1794,1156,1782,1185,1784,1200,1786,1217,1783,1244,1780,1271,1780,1279,1779,1286,1781,1297,1781,1299,1782,1299,1782,1300,1783,1300,1789,1301,1797,1298,1805,1295,1809,1302,1813,1309,1817,1307,1820,1304,1822,1301,1825,1296,1832,1291,1843,1284,1858,1285,1862,1285,1864,1287,1872,1292,1883,1290,1887,1290,1890,1291,1893,1292,1896,1293,1913,1295,1930,1294,1943,1294,1955,1292,1958,1292,1959,1291,1964,1287,1970,1280,1972,1279,1972,1277,1976,1269,1983,1269,1994,1270,2005,1271,2011,1271,2014,1278,2018,1285,2023,1287,2025,1287,2028,1287,2059,1287,2083,1283,2107,1279,2122,1279,2136,1280,2145,1280,2155,1281,2165,1272,2172,1267,2175,1255,2178,1244,2186,1238,2195,1230,2208,1224,2219,1219,2230,1216,2250,1210,2265,1204,2268,1204,2270,1203,2282,1200,2290,1194,2312,1180,2328,1165,2330,1162,2333,1161,2337,1159,2338,1156,j,2345,1156,f,2350,1157,2354,1159,2352,1139,2338,1119,2338,1113,2348,1101,2357,1091,2361,1088,2383,1078,2383,1050,2383,1031,2375,1002,2372,991,2370,962,2370,961,2360,953,2357,950,2353,946,2350,941,2348,925,2331,915,2316,916,2308,917,2286,906,2282,904,2238,871,f,2201,844,2177,840,c]],label:"Marrakech Tensift Al Haouz",shortLabel:"MK",labelPosition:[216.6,115.3],labelAlignment:[t,v]},"MA.MT":{outlines:[[i,3036,871,f,3024,883,3001,883,2984,883,2979,878,2972,867,2963,854,2950,843,2941,834,j,2920,806,f,2902,808,2897,803,2881,789,2879,775,2877,770,2859,751,2846,735,2846,719,2846,714,2839,685,2838,675,2835,643,j,2830,610,f,2828,605,2822,602,2816,600,2815,596,2812,590,2794,566,2787,558,2786,541,2783,536,2767,504,2756,482,2742,468,2731,475,2714,481,2712,487,2714,493,j,2682,493,f,2671,489,2663,489,2659,489,2650,494,2638,501,2635,510,2657,520,2659,524,2671,542,2673,546,2675,550,2675,568,2667,615,2664,638,2664,659,2661,672,2655,698,2631,698,2604,698,2580,681,2556,664,2555,664,2542,664,2539,674,2540,687,2540,691,2539,716,2531,738,2559,750,2577,781,2608,836,2616,840,2618,841,2620,842,2651,860,2682,883,2695,899,2704,908,2715,920,2715,938,2715,960,2685,976,2653,994,2651,999,j,2651,1005,2659,1006,f,2660,1006,2661,1006,2658,1009,2663,1013,2669,1009,2674,1004,2675,1003,2678,1002,2689,1001,2696,1010,2698,1012,2700,1013,2713,1025,2720,1036,2724,1042,2723,1047,2722,1052,2718,1059,2715,1067,2709,1072,2703,1077,2701,1078,2699,1080,2698,1083,2693,1095,2683,1103,2689,1107,2698,1107,2702,1107,2705,1107,2719,1107,2730,1113,2733,1114,2735,1116,2745,1123,2758,1124,2762,1124,2774,1128,2787,1133,2791,1138,2795,1144,2802,1148,2809,1152,2810,1163,2811,1175,2809,1187,2807,1199,2805,1203,2798,1217,2798,1235,2798,1238,2796,1241,2792,1247,2793,1255,2793,1264,2787,1277,2782,1291,2776,1293,2770,1295,2769,1300,2768,1305,2767,1317,2767,1330,2775,1334,2783,1338,2785,1342,2788,1345,2794,1345,2800,1345,2802,1357,2804,1369,2804,1370,2804,1373,2802,1375,2795,1384,2795,1389,2795,1394,2793,1394,2790,1395,2794,1404,2798,1413,2801,1415,2814,1423,2826,1435,2832,1442,2835,1450,2835,1452,2835,1453,2835,1455,2833,1460,2831,1464,2831,1470,2832,1475,2833,1480,2835,1486,2839,1488,2844,1490,2848,1495,2852,1501,2862,1508,2872,1516,2876,1523,2880,1530,2878,1533,2876,1537,2876,1546,2878,1554,2882,1574,2883,1574,2884,1574,j,3305,1216,3306,1210,f,3306,1204,3293,1193,3280,1182,3280,1178,3280,1174,3283,1170,j,3281,1170,f,3270,1158,3216,1078,3208,1066,3209,1056,3209,1032,3209,1028,3205,1000,3201,997,3198,994,3175,994,j,3149,996,f,3126,1001,3125,1008,j,3119,1008,f,3098,997,3096,980,3095,970,3079,944,3071,916,3064,905,3058,893,3053,885,3047,875,3041,872,3040,872,3039,871,f,3037,871,3036,871,c]],label:"Meknès Tafilalet",shortLabel:"MT",labelPosition:[291.6,102.1],labelAlignment:[t,v]},"MA.OR":{outlines:[[i,3471,345,f,3470,332,3467,320,3465,309,3453,306,3442,304,3441,298,3440,293,3432,285,3425,278,3407,267,3376,255,3340,256,3305,256,3254,255,3245,230,3245,212,3245,197,3228,199,3225,200,3225,201,3222,207,3218,212,3211,222,3205,230,3204,231,3203,232,3197,235,3194,240,3189,247,3183,248,3170,249,3163,245,3160,244,3158,243,3150,242,3143,242,3140,242,3138,241,3128,237,3122,227,3122,226,3120,226,3118,225,3116,224,3112,222,3105,221,3104,221,3103,221,3094,220,3085,220,3085,220,3085,221,3080,215,3065,216,j,3064,277,f,3064,289,3085,302,3106,315,3106,329,j,3100,360,f,3099,370,3100,373,3102,380,3113,380,3122,380,3131,367,3140,364,3160,355,3162,353,3181,334,3189,326,3212,327,3246,327,3246,363,j,3244,392,f,3231,397,3227,400,3214,413,3210,416,3206,437,3206,442,3211,442,3216,462,j,3216,482,f,3216,507,3214,511,j,3217,511,f,3184,524,3191,545,3191,545,3190,546,3198,553,3209,570,3211,572,3223,579,3235,588,3235,598,3235,608,3229,613,3217,622,3210,631,3196,639,3196,646,3196,654,3236,685,3275,717,3275,727,3275,738,3246,743,3221,747,3191,745,3151,742,3113,777,3084,805,3079,813,3046,841,3039,860,j,3039,871,3041,872,f,3047,875,3053,885,3058,893,3064,905,3071,916,3079,943,3095,969,3096,980,3098,997,3119,1007,j,3125,1007,f,3126,1000,3149,996,j,3175,993,f,3198,993,3201,996,3205,1000,3209,1027,3209,1032,3209,1055,3208,1066,3216,1077,3270,1157,3281,1170,j,3283,1170,f,3283,1169,3284,1168,j,3284,1158,f,3290,1158,3295,1155,3418,1059,3486,1005,3554,951,3555,954,3557,958,3563,948,3569,938,3575,935,3576,934,3577,933,3595,915,3599,907,3603,899,3598,888,3592,877,3587,868,3584,863,3583,860,3579,846,3575,833,3574,831,3574,830,3572,817,3565,805,3560,797,3561,787,3561,780,3556,774,3553,770,3552,765,3548,747,3541,729,3535,714,3530,697,3529,695,3529,692,3530,663,3513,647,3512,645,3511,642,3510,640,3510,637,3508,629,3508,620,3509,603,3504,587,3504,586,3504,585,3500,573,3495,560,3494,557,3494,555,3495,547,3490,542,3489,541,3488,540,3481,530,3482,517,3483,515,3484,513,3488,502,3494,495,3495,494,3497,491,3498,490,3498,487,3501,459,3493,435,3493,432,3492,430,3488,422,3486,407,3485,404,3483,401,3474,389,3473,372,f,3471,359,3471,345,c]],label:"Oriental",shortLabel:"OR",labelPosition:[337.5,76.8],labelAlignment:[t,v]},"MA.OL":{outlines:[[i,949,2811,f,937,2808,910,2815,884,2822,881,2823,874,2825,868,2827,865,2827,864,2828,858,2833,852,2839,846,2846,838,2847,834,2847,831,2846,821,2839,807,2830,795,2823,795,2821,795,2818,785,2811,775,2803,754,2805,733,2807,731,2808,728,2810,725,2811,723,2812,720,2813,716,2815,712,2817,710,2819,708,2820,707,2822,705,2822,690,2825,675,2825,661,2825,648,2826,632,2827,624,2820,624,2818,624,2816,624,2816,624,2815,623,2810,622,2805,622,2795,619,2790,617,2786,611,2783,606,2780,592,2779,579,2778,575,2775,572,2772,572,2771,j,569,2771,f,569,2783,564,2791,564,2798,568,2803,j,566,2812,f,565,2812,563,2812,560,2812,558,2813,547,2816,537,2824,533,2827,530,2829,519,2838,508,2848,507,2850,505,2851,499,2855,493,2858,473,2869,455,2882,453,2884,451,2886,444,2896,431,2903,428,2905,425,2906,415,2910,408,2918,407,2920,404,2921,398,2925,393,2930,385,2937,376,2943,367,2949,360,2957,358,2959,356,2960,346,2970,335,2979,327,2986,325,2995,324,2997,322,2998,317,3001,314,3008,311,3013,305,3020,303,3022,301,3025,298,3030,295,3032,294,3034,294,3035,293,3040,303,3050,304,3074,308,3077,310,3080,311,3083,313,3086,313,3090,315,3103,308,3112,j,305,3115,f,298,3126,291,3125,284,3123,276,3123,269,3124,255,3132,252,3135,251,3138,248,3162,248,3187,249,3196,245,3202,240,3209,231,3215,228,3217,228,3220,229,3249,213,3268,210,3271,208,3275,206,3281,202,3287,191,3303,190,3322,190,3328,187,3331,184,3335,182,3338,178,3346,171,3353,159,3364,146,3373,142,3376,137,3377,117,3380,95,3380,93,3380,91,3381,85,3384,82,3387,80,3389,76,3405,72,3421,67,3421,62,3422,56,3428,51,3434,50,3441,48,3448,49,3449,50,3451,52,3453,53,3455,54,3456,55,3459,56,3460,58,3467,57,3470,57,3473,51,3490,46,3506,40,3518,35,3531,32,3541,29,3551,28,3555,28,3559,43,3570,j,903,3619,f,912,3617,921,3617,922,3616,922,3614,922,3596,922,3577,922,3528,922,3480,922,3432,922,3385,922,3337,922,3290,922,3270,921,3250,920,3228,939,3220,942,3219,944,3217,954,3207,967,3205,979,3204,989,3200,996,3198,1002,3195,1021,3187,1039,3177,1050,3171,1062,3171,1066,3171,1069,3171,1081,3170,1092,3168,1094,3167,1106,3162,1118,3157,1127,3156,1136,3155,1145,3149,1154,3144,1156,3141,1167,3124,1192,3125,j,1195,3125,f,1195,3104,1195,3082,1195,3033,1195,2985,1195,2941,1195,2892,1195,2890,1195,2887,1195,2887,1194,2887,1202,2877,1204,2862,1205,2854,1208,2850,1173,2850,1138,2850,1113,2850,1088,2851,1075,2852,1066,2849,1065,2848,1063,2848,1061,2848,1061,2847,1057,2841,1050,2837,1047,2835,1043,2834,1042,2834,1040,2833,1034,2831,1028,2830,1023,2830,1018,2828,1013,2827,1003,2821,993,2815,977,2814,f,962,2814,949,2811,c]],label:"Oued Ed Dahab Lagouira",shortLabel:"OL",labelPosition:[61.8,319.2],labelAlignment:[t,v]},"MA.RZ":{outlines:[[i,2536,479,f,2490,495,2467,495,2465,495,2462,494,2459,498,2456,501,2456,501,2455,501,2454,502,2452,503,2451,504,2449,505,2447,505,2446,506,2440,511,2437,513,2436,514,2435,515,2423,528,2420,537,2416,547,2408,545,2402,544,2399,552,2386,555,2379,558,2379,558,2378,559,2378,560,2377,561,2388,576,2391,586,2396,617,2399,620,2413,640,2421,643,2437,649,2439,660,2446,705,2457,720,2467,720,2498,725,2503,726,2526,736,2528,737,2531,738,2539,716,2539,691,2539,687,2539,674,2541,664,2555,664,2556,664,2580,681,2603,698,2630,698,2655,698,2661,672,2664,659,2663,638,2667,615,2674,568,2674,550,2672,546,2671,542,2658,524,2656,520,2635,510,2628,507,2619,503,2594,483,2584,481,f,2562,479,2536,479,c]],label:"Rabat Salé Zemmour Zaer",shortLabel:"RZ",labelPosition:[252.3,57.8],labelAlignment:[t,v]},"MA.SM":{outlines:[[i,2536,1106,f,2535,1109,2533,1110,2521,1117,2509,1123,2507,1125,2503,1126,2497,1128,2493,1129,2482,1130,2471,1133,2468,1134,2464,1136,2453,1146,2445,1160,2440,1168,2432,1171,2429,1172,2425,1172,2404,1172,2383,1172,2381,1173,2380,1171,2374,1172,2369,1169,2364,1165,2358,1161,2357,1161,2355,1160,2355,1160,2354,1160,j,2354,1159,f,2350,1157,2345,1156,j,2338,1155,f,2337,1159,2333,1161,2330,1162,2328,1165,2312,1180,2290,1194,2282,1200,2270,1203,2268,1204,2265,1204,2250,1210,2230,1216,2219,1219,2208,1224,2195,1230,2186,1238,2178,1244,2175,1255,2172,1267,2165,1272,2155,1281,2145,1280,2136,1280,2121,1279,2107,1279,2083,1283,2059,1287,2028,1287,2025,1287,2023,1287,2018,1285,2014,1278,2011,1271,2005,1271,1994,1270,1983,1269,1976,1269,1972,1277,1972,1279,1970,1280,1964,1287,1959,1291,1958,1292,1955,1292,1943,1294,1930,1294,1913,1295,1896,1293,1893,1292,1890,1291,1887,1290,1883,1290,1872,1292,1864,1287,1862,1285,1858,1285,1843,1284,1832,1291,1825,1296,1822,1301,1820,1304,1816,1306,1813,1309,1809,1302,1805,1295,1797,1298,1789,1301,1783,1300,1782,1300,1782,1299,j,1782,1312,f,1788,1326,1788,1331,j,1787,1339,f,1777,1349,1782,1358,1790,1375,1795,1372,1800,1369,1811,1385,1812,1386,1813,1387,1821,1393,1826,1399,1828,1401,1828,1403,1830,1412,1829,1422,1829,1426,1829,1430,1828,1455,1822,1480,1822,1484,1822,1487,1822,1501,1818,1512,1809,1536,1795,1554,1793,1557,1791,1560,1788,1567,1784,1574,1783,1577,1780,1579,1773,1585,1767,1592,1760,1601,1750,1612,1741,1621,1736,1633,1734,1638,1727,1644,1725,1646,1724,1648,1712,1666,1695,1675,1683,1681,1671,1690,1663,1696,1652,1701,1646,1705,1646,1707,1646,1708,1646,1709,1647,1711,1647,1712,1647,1715,1649,1716,1652,1718,1659,1720,1666,1723,1674,1723,1683,1724,1689,1727,1695,1730,1696,1729,1709,1712,1730,1715,1748,1717,1760,1707,1768,1700,1778,1690,1780,1687,1783,1687,1790,1686,1796,1683,1798,1682,1800,1681,1806,1678,1811,1673,1813,1671,1815,1671,1847,1670,1878,1671,1892,1671,1900,1668,1905,1666,1910,1665,1913,1665,1914,1664,1921,1659,1930,1658,1933,1657,1934,1656,1936,1652,1942,1649,1945,1647,1948,1646,1959,1641,1973,1641,1978,1641,1979,1645,1981,1650,1988,1652,2000,1655,1997,1645,1997,1644,1996,1642,1992,1618,1993,1592,1993,1590,1994,1588,1997,1582,1998,1575,1998,1572,1999,1570,2001,1563,2003,1557,2004,1550,2011,1546,2015,1543,2015,1540,2015,1537,2016,1535,2019,1527,2027,1522,2030,1520,2031,1517,2034,1504,2047,1505,2052,1511,2055,1515,2057,1517,2059,1519,2060,1520,2062,1521,2066,1524,2070,1525,2080,1525,2090,1525,2104,1526,2115,1522,2117,1521,2117,1520,2122,1511,2135,1512,2138,1512,2138,1513,2140,1518,2145,1518,2159,1519,2167,1509,2169,1507,2171,1506,2181,1498,2187,1487,2190,1483,2193,1483,2197,1482,2199,1481,2205,1477,2213,1477,2219,1477,2225,1479,2229,1481,2235,1485,2234,1477,2240,1472,2242,1471,2243,1470,2252,1463,2265,1464,2273,1465,2280,1464,2294,1462,2298,1472,2302,1482,2313,1479,2315,1479,2315,1477,2316,1464,2323,1458,2327,1454,2327,1450,2326,1444,2330,1439,2336,1432,2345,1425,2347,1424,2348,1423,2353,1423,2355,1420,2357,1417,2358,1416,2364,1411,2370,1410,2374,1410,2378,1409,2385,1408,2390,1413,2392,1415,2393,1418,2395,1421,2403,1421,2412,1422,2416,1419,2422,1416,2427,1409,2433,1402,2437,1400,2440,1397,2443,1396,2447,1395,2450,1394,2463,1393,2472,1401,2474,1402,2476,1403,2480,1404,2483,1407,2497,1425,2515,1437,2520,1440,2520,1447,2522,1461,2518,1472,2518,1474,2517,1476,2515,1478,2515,1480,2514,1482,2511,1484,2511,1484,2510,1485,2505,1489,2506,1496,2506,1498,2507,1499,2508,1501,2509,1501,2514,1503,2519,1502,2520,1503,2521,1504,2524,1509,2530,1513,2532,1515,2534,1516,2540,1521,2539,1529,2538,1536,2537,1539,2536,1543,2533,1545,2531,1548,2526,1550,2525,1560,2525,1570,2525,1590,2524,1603,2523,1617,2523,1622,2523,1627,2521,1632,2520,1638,2518,1642,2517,1646,2520,1652,2520,1653,2520,1653,2523,1660,2523,1662,2523,1664,2525,1665,2546,1678,2560,1695,2562,1697,2563,1698,2572,1702,2578,1715,2585,1709,2591,1705,2601,1698,2612,1691,2617,1689,2621,1686,2631,1679,2643,1673,2655,1667,2668,1658,2681,1650,2714,1631,2716,1630,2745,1613,2757,1608,2760,1603,2764,1598,2767,1598,2770,1598,2777,1596,2784,1595,2790,1587,2795,1580,2803,1576,2805,1575,2807,1574,2823,1569,2835,1577,2837,1579,2838,1579,2845,1580,2853,1580,2852,1579,2852,1578,2856,1575,2882,1573,2878,1554,2876,1545,2876,1537,2878,1533,2880,1529,2876,1522,2872,1516,2862,1508,2852,1500,2848,1495,2844,1489,2839,1487,2835,1485,2833,1480,2832,1475,2831,1469,2831,1464,2833,1459,2835,1455,2835,1452,2835,1451,2835,1449,2832,1441,2826,1434,2814,1423,2801,1414,2798,1412,2794,1403,2790,1395,2793,1394,2795,1393,2795,1388,2795,1383,2802,1374,2804,1372,2804,1370,2804,1369,2802,1356,2800,1344,2794,1344,2788,1345,2785,1341,2783,1338,2775,1333,2767,1329,2767,1317,2768,1305,2769,1299,2770,1294,2776,1292,2782,1290,2787,1277,2793,1263,2793,1255,2792,1247,2796,1240,2798,1237,2798,1235,2798,1217,2805,1202,2807,1199,2809,1187,2811,1175,2810,1163,2809,1151,2802,1147,2795,1144,2791,1138,2787,1132,2774,1128,2762,1124,2758,1123,2745,1122,2735,1115,2733,1114,2730,1112,2719,1107,2705,1106,2702,1106,2698,1106,2689,1107,2683,1102,2693,1094,2698,1082,2699,1080,2701,1078,2703,1076,2709,1071,2715,1066,2718,1059,2722,1051,2723,1046,2724,1041,2720,1035,2713,1025,2700,1013,2698,1011,2696,1009,2689,1000,2678,1002,2675,1002,2674,1003,2669,1008,2663,1012,2658,1009,2661,1006,2660,1006,2659,1006,2648,1007,2644,1020,2642,1026,2640,1030,2634,1048,2632,1051,2632,1055,2632,1060,2631,1066,2625,1069,2623,1070,2621,1071,2618,1072,2615,1074,2613,1076,2610,1077,2598,1083,2585,1087,2562,1095,2543,1102,f,2538,1103,2536,1106,c]],label:"Souss Massa Draâ",shortLabel:"SM",labelPosition:[226.2,136.5],labelAlignment:[t,v]},"MA.TD":{outlines:[[i,2683,882,f,2651,859,2621,842,2619,841,2617,840,j,2608,840,f,2593,848,2536,851,2536,850,2534,850,2523,848,2470,847,2429,847,2406,891,2401,899,2385,916,2370,931,2361,953,2370,961,2371,962,2373,991,2376,1002,2383,1031,2383,1050,2383,1078,2362,1088,2357,1091,2348,1101,2338,1113,2338,1119,2353,1139,2354,1159,2355,1160,2356,1160,2357,1161,2359,1162,2364,1165,2369,1169,2374,1172,2380,1171,2381,1173,2383,1172,2405,1172,2426,1172,2430,1172,2433,1171,2440,1168,2446,1160,2454,1146,2465,1136,2468,1134,2472,1133,2482,1130,2493,1129,2497,1128,2504,1126,2507,1125,2510,1123,2521,1117,2533,1110,2536,1109,2537,1106,2539,1103,2543,1102,2563,1095,2586,1087,2598,1083,2611,1077,2613,1076,2615,1074,2618,1072,2621,1071,2623,1070,2625,1069,2632,1066,2632,1060,2633,1055,2633,1051,2634,1048,2641,1031,2643,1026,2645,1020,2649,1007,2660,1006,j,2652,1005,2652,998,f,2653,994,2686,976,2715,959,2715,937,2715,920,2704,907,f,2696,898,2683,882,c]],label:"Tadla Azilal",shortLabel:"TD",labelPosition:[251.7,98.6],labelAlignment:[t,v]},"MA.TO":{outlines:[[i,2826,192,f,2798,183,2792,173,2781,156,2752,96,2741,78,2728,55,2718,41,2700,41,2687,41,2631,91,2624,97,2620,117,2616,140,2612,146,2607,154,2607,173,2609,178,2604,189,2598,199,2599,200,2598,206,2573,255,2573,255,2573,256,j,2573,278,2580,278,f,2602,286,2637,298,2655,303,2682,320,2720,345,2736,350,2768,349,2779,365,j,2791,357,2789,357,f,2795,340,2799,337,2800,336,2817,328,2827,324,2845,318,2858,310,2870,310,2934,281,2932,247,2931,246,2931,245,2932,245,2932,244,2925,236,2904,230,j,2884,215,f,2879,212,2864,211,f,2840,197,2826,192,c]],label:"Tanger Tétouan",shortLabel:"TO",labelPosition:[273.5,22.8],labelAlignment:[t,v]},"MA.TH":{outlines:[[i,2989,225,f,2947,228,2932,244,2932,245,2931,245,2931,246,2932,247,2934,281,2870,310,2858,310,2845,318,2827,324,2817,328,2800,336,2799,337,2795,340,2789,357,j,2791,357,2785,361,f,2787,366,2787,373,2787,394,2751,417,2740,425,2736,433,2728,454,2722,465,2716,473,2714,481,2731,475,2742,468,2751,463,2756,457,2770,444,2789,448,2790,448,2791,448,2791,448,2792,448,2809,444,2836,461,2848,464,2866,485,2875,496,2881,501,2891,499,2904,508,2914,520,2924,527,2935,534,2940,537,2944,545,2948,549,2955,556,2971,552,2987,549,2991,557,2992,557,2999,581,3014,640,3047,640,3062,640,3069,632,3073,627,3081,613,3085,609,3097,600,3107,590,3107,577,3113,561,3151,561,3171,561,3190,546,3191,545,3191,545,3184,524,3217,511,j,3214,511,f,3216,507,3216,482,j,3216,462,f,3211,442,3206,442,3206,437,3210,416,3214,413,3227,400,3231,397,3244,392,j,3246,363,f,3246,327,3212,327,3189,326,3181,334,3162,353,3160,355,3140,364,3131,367,3122,380,3113,380,3102,380,3100,373,3099,370,3100,360,j,3106,329,f,3106,315,3085,302,3064,289,3064,277,j,3065,216,f,3064,216,3062,216,3038,212,3037,212,3028,212,3018,218,f,3007,223,2989,225,c]],label:"Taza Al Hoceima Taounate",shortLabel:"TH",labelPosition:[298,42.6],labelAlignment:[t,v]}}}];
g=d.length;if(r){while(g--){e=d[g];n(e.name.toLowerCase(),e,n.geo);}}else{while(g--){e=d[g];u=e.name.toLowerCase();a(s,u,1);h[s].unshift({cmd:"_call",obj:window,args:[function(w,x){if(!n.geo){p.raiseError(p.core,"12052314141","run","JavaScriptRenderer~Maps._call()",new Error("FusionCharts.HC.Maps.js is required in order to define vizualization"));
return;}n(w,x,n.geo);},[u,e],window]});}}}]);