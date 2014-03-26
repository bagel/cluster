/*
 * @license FusionCharts JavaScript Library
 * Copyright FusionCharts Technologies LLP
 * License Information at <http://www.fusioncharts.com/license>
 *
 * @author FusionCharts Technologies LLP
 * @version fusioncharts/3.3.1-sr3.21100
 * @id fusionmaps.CapeVerde.20.10-30-2012 06:07:35
 */
FusionCharts(["private","modules.renderer.js-capeverde",function(){var p=this,k=p.hcLib,n=k.chartAPI,h=k.moduleCmdQueue,a=k.injectModuleDependency,i="M",j="L",c="Z",f="Q",b="left",q="right",t="center",v="middle",o="top",m="bottom",s="maps",l=true&&!/fusioncharts\.com$/i.test(location.hostname),r=!!n.geo,d,e,u,g;
d=[{name:"CapeVerde",revision:20,creditLabel:l,standaloneInit:true,baseWidth:700,baseHeight:620,baseScaleFactor:10,entities:{"CV.MO":{outlines:[[i,2620,5495,f,2624,5507,2633,5517,2637,5520,2639,5524,2640,5525,2642,5526,2646,5528,2649,5532,2655,5542,2663,5549,2664,5550,2665,5551,2670,5557,2677,5561,2679,5562,2681,5564,2686,5568,2694,5566,2703,5565,2701,5574,2700,5578,2701,5582,2703,5590,2704,5599,2704,5606,2707,5609,2712,5614,2716,5621,2722,5630,2726,5639,2732,5644,2734,5650,2736,5653,2737,5655,2739,5658,2743,5659,2745,5659,2747,5661,2749,5663,2753,5662,2757,5661,2762,5664,2767,5667,2772,5664,2778,5662,2782,5662,2782,5662,2783,5663,2785,5663,2787,5663,2812,5663,2815,5661,2818,5659,2824,5658,2830,5656,2843,5657,2857,5659,2884,5659,2883,5653,2882,5647,2881,5641,2880,5635,2878,5624,2878,5612,2878,5610,2877,5607,2876,5578,2864,5552,2862,5547,2860,5544,2851,5533,2849,5522,2849,5520,2848,5518,2846,5516,2846,5514,2844,5507,2839,5504,2826,5496,2816,5485,2814,5484,2812,5482,2809,5480,2806,5478,2801,5476,2797,5472,2790,5465,2779,5459,2776,5457,2773,5456,2757,5449,2742,5442,2738,5440,2733,5439,2722,5436,2716,5427,2715,5426,2713,5425,2706,5421,2694,5422,2680,5423,2668,5431,2665,5434,2662,5436,2654,5443,2644,5448,2636,5452,2627,5456,2618,5460,2611,5464,2613,5472,2615,5480,2617,5486,2619,5492,f,2619,5494,2620,5495,c]],label:"Mosteiros",shortLabel:"MO",labelPosition:[302,551.6],labelAlignment:[b,v],labelConnectors:[[i,3020,5516,j,2784,5516]]},"CV.PA":{outlines:[[i,1147,386,f,1142,392,1135,400,1129,407,1125,414,1120,423,1113,428,1103,434,1096,444,1096,446,1095,446,1093,449,1091,451,1096,458,1095,467,1095,468,1096,469,1101,474,1110,473,1125,472,1138,475,1145,476,1153,477,1160,478,1168,478,1176,478,1183,482,1193,489,1208,489,1209,489,1210,489,1223,495,1233,507,1244,519,1255,527,1265,534,1270,543,1270,544,1270,545,1272,551,1274,555,1275,559,1276,563,1283,555,1295,546,1307,537,1320,520,1322,519,1322,517,1323,503,1323,490,1324,477,1319,465,1318,461,1313,459,1303,454,1293,448,1281,440,1270,433,1266,431,1261,426,1256,422,1248,416,1243,412,1237,408,1216,392,1200,381,1191,375,1191,365,1185,364,1179,364,1178,364,1177,365,1171,371,1163,375,f,1154,379,1147,386,c]],label:"Paul",shortLabel:"PA",labelPosition:[139.4,43.8],labelAlignment:[b,v],labelConnectors:[[i,1394,438,j,1224,438]]},"CV.RG":{outlines:[[i,1065,260,f,1049,254,1040,247,1033,240,1020,240,1017,240,1016,241,1014,242,1011,244,1010,245,1009,246,1005,250,1002,250,998,250,995,251,987,256,977,255,974,255,972,256,969,257,966,258,963,260,960,261,953,264,942,268,934,271,926,277,918,283,907,288,904,290,901,291,898,292,896,294,890,299,879,298,877,297,876,298,872,303,867,303,864,302,863,303,844,317,828,335,822,341,814,341,803,340,792,339,791,339,789,338,783,336,777,335,774,335,773,336,771,337,768,339,767,340,765,341,756,346,749,355,746,359,740,363,738,365,736,366,732,368,730,370,728,372,726,374,724,375,723,376,718,381,719,386,719,391,711,395,703,397,698,406,702,415,713,424,722,432,731,442,735,447,738,454,739,457,742,459,743,459,743,460,748,467,755,471,757,472,759,474,765,481,770,488,775,494,781,496,787,498,795,499,803,500,811,501,817,502,822,506,826,509,825,514,825,522,824,530,824,531,822,532,820,534,819,538,817,543,817,549,817,550,819,547,821,544,826,542,837,536,845,528,848,524,853,520,859,515,866,513,867,513,871,514,875,514,880,513,885,512,894,508,903,504,916,506,926,508,936,508,938,509,947,506,955,503,966,504,977,504,981,505,985,506,990,506,991,506,992,505,1009,496,1025,489,1032,485,1040,482,1057,475,1072,465,1077,462,1083,459,1087,458,1091,453,1092,452,1093,451,1095,449,1097,446,1098,446,1098,444,1105,434,1115,428,1122,423,1127,414,1131,407,1137,400,1144,392,1149,386,1156,379,1165,375,1173,371,1179,365,1180,364,1181,364,1187,364,1193,365,1192,342,1193,320,1194,307,1189,300,1189,299,1187,298,1182,296,1177,295,1163,293,1150,291,1145,290,1140,289,1120,287,1103,279,1091,274,1079,268,1077,267,1076,266,f,1071,262,1065,260,c]],label:"Ribeira Grande",shortLabel:"RG",labelPosition:[94.5,39.4],labelAlignment:[t,v]},"CV.PN":{outlines:[[i,894,508,f,885,512,880,513,875,514,871,514,867,513,866,513,859,515,853,520,848,524,845,528,837,536,826,542,821,544,819,547,817,550,817,549,817,543,819,538,820,534,822,532,824,531,824,530,825,522,825,514,826,509,822,506,817,502,811,501,803,500,795,499,787,498,781,496,775,494,770,488,765,481,759,474,757,472,755,471,748,467,743,460,743,459,742,459,739,457,738,454,735,447,731,442,722,432,713,424,702,415,698,406,697,406,697,407,691,416,682,419,673,422,671,423,663,425,659,428,654,432,646,435,638,438,631,437,624,435,626,443,627,452,621,451,614,450,608,451,603,451,598,453,593,455,587,456,581,457,579,458,565,460,552,460,549,460,548,461,546,462,543,464,542,465,542,469,542,473,538,476,533,479,526,477,519,474,519,480,518,485,512,480,507,475,505,476,503,477,501,479,499,480,497,481,495,482,478,488,460,494,442,515,424,536,400,599,413,605,412,622,412,634,419,645,420,646,420,647,422,652,423,657,423,660,425,661,427,662,428,663,432,667,437,671,438,672,440,672,443,673,446,674,457,678,468,685,470,686,472,688,482,699,489,711,490,713,492,715,500,725,501,739,502,758,496,773,496,775,496,777,494,795,500,810,500,811,501,811,509,814,512,822,512,823,512,824,513,831,511,837,510,841,509,844,509,846,508,847,507,849,507,850,505,856,503,862,499,869,496,876,496,877,496,879,494,892,501,903,505,908,506,912,528,937,533,942,538,948,546,949,553,949,560,950,563,951,565,951,569,952,571,949,573,944,580,942,582,942,583,941,587,939,591,937,592,937,593,937,600,937,605,935,607,934,608,934,611,932,614,931,615,930,617,929,626,923,637,920,639,919,641,919,652,918,662,921,670,922,675,925,688,934,702,939,704,939,706,939,720,941,735,941,749,941,763,939,765,939,766,938,772,933,777,926,778,925,780,924,786,922,795,922,804,923,813,922,815,922,816,922,823,919,828,912,836,901,843,889,852,876,865,867,867,866,871,863,875,859,881,852,886,845,889,843,892,840,895,832,897,824,911,820,926,815,918,818,j,943,809,f,946,805,948,799,949,797,949,795,950,794,950,793,954,786,959,780,969,770,981,762,983,761,985,759,990,756,995,751,1014,731,1029,708,1032,705,1034,702,1037,698,1041,696,1048,693,1053,688,1059,683,1066,683,1080,684,1095,684,1109,685,1121,677,1124,675,1129,674,1130,674,1131,673,1144,666,1157,660,1170,654,1183,647,1185,645,1188,643,1190,641,1192,640,1202,633,1210,626,1274,581,1275,580,1277,577,1274,574,1271,571,1278,563,1277,559,1276,555,1274,551,1272,545,1272,544,1272,543,1267,534,1257,527,1246,519,1235,507,1225,495,1212,489,1211,489,1210,489,1195,489,1185,482,1178,478,1170,478,1162,478,1155,477,1147,476,1140,475,1127,472,1112,473,1103,474,1098,469,1097,468,1097,467,1098,458,1093,451,1092,452,1091,453,1087,458,1083,459,1077,462,1072,465,1057,475,1040,482,1032,485,1025,489,1009,496,992,505,991,506,990,506,985,506,981,505,977,504,966,504,955,503,947,506,938,509,936,508,926,508,916,506,f,903,504,894,508,c]],label:"Porto Novo",shortLabel:"PN",labelPosition:[75.1,67.9],labelAlignment:[t,v]},"CV.SV":{outlines:[[i,1974,1525,f,1965,1527,1965,1534,1965,1546,1971,1552,1973,1555,1977,1559,1978,1560,1978,1561,1980,1562,1982,1564,1987,1567,1991,1570,1994,1572,1997,1573,2000,1574,2003,1576,2014,1583,2022,1594,2023,1595,2023,1596,2024,1600,2030,1599,2032,1599,2033,1597,2036,1582,2027,1570,2026,1569,2025,1567,2021,1557,2012,1552,2007,1549,2003,1545,2003,1544,2002,1542,1995,1533,1987,1528,f,1981,1524,1974,1525,c],[i,1948,1325,f,1925,1327,1905,1320,1902,1319,1900,1319,1892,1318,1885,1317,1876,1316,1870,1310,1869,1309,1867,1308,1854,1290,1838,1265,1836,1263,1834,1261,1832,1259,1831,1257,1821,1241,1807,1228,1805,1227,1802,1225,1791,1218,1780,1210,1776,1208,1772,1207,1748,1204,1743,1228,1742,1228,1741,1229,1737,1231,1738,1238,1739,1249,1735,1258,1735,1259,1735,1260,1736,1266,1733,1271,1732,1272,1732,1274,1732,1288,1739,1297,1741,1299,1742,1303,1749,1307,1757,1306,1761,1305,1764,1307,1778,1313,1790,1320,1794,1322,1797,1324,1799,1325,1800,1326,1810,1328,1821,1337,1830,1345,1828,1358,1827,1360,1828,1360,1833,1361,1837,1365,1840,1368,1845,1370,1847,1370,1849,1371,1851,1373,1853,1374,1855,1375,1857,1376,1861,1378,1865,1378,1885,1380,1905,1380,1919,1380,1933,1379,1957,1377,1973,1360,1975,1358,1976,1355,f,1979,1323,1948,1325,c],[i,2231,1664,f,2233,1662,2232,1660,2228,1653,2222,1647,2216,1643,2211,1640,2210,1639,2208,1638,2206,1637,2204,1635,2202,1631,2196,1632,2189,1633,2185,1638,2184,1640,2182,1641,2176,1645,2172,1649,2169,1652,2166,1654,2162,1656,2159,1660,2158,1661,2157,1662,2156,1664,2156,1665,2155,1672,2161,1675,2163,1676,2164,1676,2167,1676,2169,1679,2172,1683,2176,1684,2178,1685,2179,1685,2186,1684,2191,1687,2193,1687,2193,1688,2195,1691,2200,1691,2218,1692,2224,1675,f,2226,1669,2231,1664,c],[i,1422,929,f,1415,927,1407,927,1400,927,1395,932,1394,933,1392,935,1388,940,1385,944,1381,950,1378,953,1377,954,1375,955,1374,955,1373,956,1370,958,1367,958,1358,958,1348,958,1341,958,1336,953,1335,953,1334,952,1332,950,1331,949,1322,941,1312,936,1310,934,1308,934,1303,934,1297,934,1296,934,1295,934,1292,937,1288,940,1286,941,1284,942,1278,947,1272,951,1272,952,1271,952,1263,955,1261,960,1260,962,1258,964,1251,973,1249,984,1249,986,1249,988,1248,1002,1249,1016,1249,1022,1246,1023,1239,1028,1232,1031,1230,1031,1229,1032,1227,1033,1226,1033,1217,1034,1208,1034,1193,1035,1181,1025,1180,1025,1180,1024,1178,1023,1176,1022,1172,1017,1163,1015,1162,1015,1161,1014,1156,1014,1151,1013,1142,1013,1136,1017,1130,1021,1122,1021,1120,1021,1118,1022,1114,1023,1113,1026,1112,1027,1112,1028,1108,1037,1103,1045,1102,1047,1101,1049,1099,1058,1091,1062,1081,1066,1072,1071,1072,1072,1071,1073,1065,1081,1060,1085,1055,1089,1052,1094,1050,1100,1045,1107,1045,1108,1044,1109,1041,1115,1042,1124,1042,1131,1042,1138,1042,1148,1045,1156,1045,1157,1047,1158,1053,1160,1061,1159,1070,1159,1078,1159,1084,1159,1086,1164,1092,1175,1098,1186,1099,1187,1100,1187,1108,1192,1110,1199,1112,1205,1116,1207,1119,1208,1126,1208,1133,1208,1135,1208,1148,1209,1160,1212,1161,1212,1162,1212,1177,1218,1189,1229,1191,1231,1193,1232,1194,1234,1196,1235,1203,1239,1211,1242,1213,1243,1215,1243,1228,1244,1240,1249,1255,1256,1266,1267,1271,1273,1280,1271,1287,1270,1292,1265,1294,1264,1296,1263,1309,1255,1321,1248,1328,1244,1337,1244,1339,1244,1341,1243,1343,1243,1346,1242,1348,1242,1350,1240,1355,1237,1359,1234,1360,1234,1361,1233,1364,1231,1368,1231,1376,1230,1383,1230,1398,1230,1413,1229,1415,1229,1417,1228,1424,1227,1430,1222,1432,1221,1433,1221,1435,1220,1437,1219,1450,1212,1463,1207,1468,1205,1472,1204,1474,1204,1476,1203,1480,1202,1483,1200,1484,1199,1485,1198,1487,1198,1488,1197,1491,1196,1494,1195,1495,1194,1497,1194,1513,1195,1526,1189,1533,1185,1540,1181,1544,1179,1547,1176,1549,1175,1552,1176,1552,1172,1552,1169,1552,1168,1553,1166,1554,1163,1554,1160,1555,1152,1555,1144,1555,1128,1553,1114,1551,1098,1557,1085,1558,1083,1559,1082,1560,1081,1560,1080,1562,1072,1558,1066,1557,1064,1555,1064,1541,1062,1527,1061,1512,1060,1497,1060,1494,1060,1491,1060,1483,1058,1475,1056,1465,1053,1455,1049,1454,1048,1454,1048,1451,1042,1447,1038,1447,1037,1446,1035,1444,1021,1445,1005,1445,1003,1445,1001,1446,1000,1447,998,1447,996,1448,994,1449,993,1449,992,1450,989,1453,985,1454,984,1454,983,1456,971,1456,959,1456,951,1450,946,1448,945,1447,942,1443,935,1436,933,f,1428,931,1422,929,c]],label:"Sao Vicente",shortLabel:"SV",labelPosition:[130.9,110.9],labelAlignment:[t,v]},"CV.SN":{outlines:[[i,2866,1560,f,2862,1557,2858,1553,2826,1519,2786,1508,2773,1505,2758,1505,2756,1505,2754,1506,2748,1509,2745,1512,2742,1515,2739,1519,2736,1523,2730,1524,2714,1529,2696,1528,2689,1528,2683,1527,2670,1525,2660,1532,2652,1539,2641,1543,2638,1544,2636,1546,2633,1550,2626,1553,2619,1556,2613,1559,2611,1560,2609,1561,2598,1570,2591,1583,2590,1585,2588,1587,2586,1590,2585,1593,2579,1613,2581,1635,2581,1639,2583,1641,2588,1648,2586,1658,2586,1662,2587,1665,2588,1668,2589,1671,2591,1674,2592,1677,2594,1680,2602,1687,2610,1695,2648,1719,2677,1738,2707,1749,2720,1750,2729,1755,2734,1758,2735,1767,2736,1768,2736,1769,2742,1779,2743,1789,2744,1795,2744,1800,2744,1806,2744,1812,2801,1893,2816,1946,2816,1952,2814,1957,2813,1958,2813,1959,2813,1970,2814,1981,2815,1982,2816,1982,2817,1983,2818,1982,2833,1982,2848,1982,2856,1982,2863,1981,2867,1975,2863,1971,2862,1971,2862,1970,2858,1964,2859,1956,2860,1953,2861,1949,2861,1948,2862,1946,2866,1936,2868,1927,2868,1924,2869,1921,2869,1916,2871,1912,2875,1907,2876,1901,2879,1894,2883,1888,2893,1876,2898,1863,2902,1850,2907,1845,2911,1840,2910,1838,2909,1835,2913,1833,2916,1832,2917,1827,2917,1826,2917,1824,2920,1812,2927,1800,2928,1799,2929,1797,2931,1793,2934,1789,2935,1788,2936,1787,2939,1783,2942,1779,2943,1778,2944,1776,2946,1772,2949,1770,2950,1768,2952,1765,2953,1764,2954,1762,2956,1758,2962,1755,2964,1755,2965,1754,2976,1746,2988,1741,2990,1741,2992,1740,2997,1738,3002,1738,3006,1738,3010,1738,3013,1730,3019,1726,3031,1718,3046,1711,3047,1711,3048,1710,3049,1709,3051,1709,3069,1708,3083,1714,3084,1715,3086,1715,3089,1714,3090,1716,3091,1717,3092,1717,3102,1717,3112,1718,3114,1718,3115,1719,3118,1720,3120,1724,3120,1725,3121,1726,3126,1729,3135,1728,3141,1728,3147,1727,3159,1727,3169,1730,3175,1732,3182,1735,3189,1739,3197,1740,3199,1740,3200,1740,3215,1747,3230,1752,3242,1755,3252,1763,3261,1770,3271,1777,3273,1778,3275,1779,3283,1785,3292,1793,3294,1794,3296,1795,3304,1800,3312,1805,3318,1809,3324,1813,3331,1819,3342,1817,3348,1817,3355,1817,3374,1816,3392,1818,3394,1819,3396,1819,3410,1821,3424,1819,3425,1819,3426,1818,3434,1813,3441,1805,3443,1804,3447,1804,3459,1804,3470,1806,3471,1806,3471,1808,3474,1816,3479,1819,3485,1823,3492,1822,3499,1822,3506,1822,3514,1823,3521,1820,3523,1819,3524,1818,3537,1814,3544,1800,3548,1793,3548,1784,3547,1773,3548,1763,3548,1760,3530,1742,3528,1741,3527,1740,3525,1738,3523,1737,3509,1728,3491,1726,3488,1725,3485,1723,3479,1719,3481,1710,3482,1702,3476,1701,3469,1699,3461,1696,3447,1691,3434,1687,3411,1679,3389,1674,3385,1673,3382,1671,3376,1667,3369,1665,3356,1662,3344,1657,3341,1657,3339,1657,3331,1657,3324,1652,3319,1648,3311,1649,3300,1650,3289,1649,3278,1648,3274,1653,3271,1655,3268,1657,3263,1661,3256,1663,3254,1664,3251,1664,3225,1668,3203,1661,3196,1659,3193,1656,3186,1647,3174,1640,3166,1635,3161,1630,3159,1628,3156,1627,3144,1622,3138,1613,3136,1610,3133,1610,3121,1607,3108,1604,3102,1603,3096,1603,3083,1604,3076,1601,3066,1597,3058,1595,3056,1594,3053,1594,3043,1593,3033,1592,3022,1591,3016,1596,3007,1603,2996,1608,2993,1609,2991,1609,2973,1610,2956,1610,2953,1610,2952,1611,2950,1613,2948,1615,2940,1622,2926,1621,2921,1620,2916,1619,2910,1618,2905,1611,2901,1604,2898,1600,2888,1587,2879,1572,f,2874,1565,2866,1560,c]],label:"Sao Nicolau",shortLabel:"SN",labelPosition:[282.3,170],labelAlignment:[t,v]},"CV.SL":{outlines:[[i,6095,1093,f,6087,1105,6082,1108,6076,1110,6076,1114,6076,1117,6065,1113,6055,1109,6053,1110,6046,1113,6040,1117,6038,1119,6036,1121,6028,1131,6013,1128,6003,1126,5996,1130,5993,1132,5992,1133,5987,1140,5979,1146,5976,1148,5973,1149,5948,1157,5933,1180,5932,1210,5931,1239,5931,1254,5934,1268,5934,1272,5935,1277,5935,1278,5936,1279,5940,1291,5944,1303,5946,1308,5950,1312,5951,1313,5952,1314,5958,1322,5963,1329,5964,1331,5964,1332,5969,1340,5969,1349,5969,1353,5966,1355,5965,1356,5964,1357,5958,1363,5956,1370,5955,1374,5954,1377,5953,1379,5953,1382,5953,1398,5954,1414,5954,1422,5954,1429,5954,1436,5949,1441,5948,1442,5947,1443,5944,1453,5948,1462,5949,1464,5951,1464,5954,1466,5959,1470,5962,1472,5966,1472,5970,1472,5974,1475,5977,1477,5982,1478,5983,1479,5984,1479,5987,1479,5989,1477,5992,1472,5998,1471,6000,1471,6002,1471,6009,1469,6014,1472,6027,1478,6042,1481,6044,1482,6046,1482,6056,1487,6063,1496,6064,1516,6063,1536,6063,1538,6061,1541,6058,1545,6056,1550,6056,1551,6055,1553,6055,1554,6054,1555,6052,1557,6050,1561,6047,1567,6045,1574,6045,1578,6045,1581,6045,1601,6060,1615,6062,1616,6063,1618,6066,1625,6073,1630,6083,1639,6083,1653,6082,1670,6085,1686,6087,1692,6087,1699,6088,1710,6090,1719,6091,1724,6091,1729,6092,1730,6092,1731,6097,1734,6105,1732,6106,1732,6107,1731,6114,1726,6121,1718,6122,1716,6125,1713,6127,1711,6130,1709,6137,1705,6143,1703,6145,1703,6146,1702,6150,1701,6153,1698,6159,1692,6157,1684,6157,1684,6157,1683,6156,1682,6158,1680,6157,1678,6156,1675,6156,1672,6154,1668,6149,1654,6151,1638,6151,1635,6152,1633,6157,1623,6157,1615,6157,1607,6166,1604,6174,1600,6175,1592,6176,1584,6177,1582,6182,1575,6185,1567,6189,1558,6193,1559,6197,1560,6203,1550,6209,1540,6210,1528,6211,1525,6210,1523,6207,1519,6206,1515,6206,1513,6205,1510,6202,1493,6203,1475,6203,1472,6202,1469,6195,1459,6188,1453,6187,1452,6186,1450,6184,1446,6184,1440,6183,1435,6181,1432,6180,1430,6180,1428,6180,1420,6176,1415,6170,1406,6169,1393,6168,1390,6171,1379,6173,1367,6170,1349,6167,1331,6168,1330,6168,1328,6170,1323,6171,1319,6178,1319,6185,1318,6187,1311,6188,1303,6192,1299,6196,1294,6196,1290,6199,1266,6191,1245,6187,1236,6178,1229,6175,1226,6172,1222,6165,1213,6159,1205,6150,1189,6156,1173,6157,1170,6158,1168,6159,1162,6163,1158,6166,1154,6167,1150,6171,1137,6158,1132,6149,1129,6138,1129,6123,1130,6124,1115,6125,1100,6115,1091,f,6103,1080,6095,1093,c]],label:"Sal",shortLabel:"SL",labelPosition:[607.1,129.7],labelAlignment:[t,v]},"CV.BV":{outlines:[[i,6390,2613,f,6391,2616,6390,2618,6387,2629,6379,2636,6373,2643,6366,2644,6361,2646,6356,2648,6353,2648,6351,2649,6344,2652,6336,2658,6332,2661,6328,2661,6296,2663,6263,2664,6244,2664,6226,2660,6223,2660,6221,2659,6210,2658,6200,2654,6187,2648,6178,2641,6165,2632,6151,2625,6139,2620,6133,2613,6128,2608,6118,2604,6113,2605,6109,2607,6109,2607,6107,2608,6103,2610,6102,2615,6102,2615,6101,2616,6100,2617,6100,2618,6100,2622,6098,2624,6097,2625,6097,2625,6090,2639,6102,2648,6104,2650,6105,2652,6110,2666,6104,2679,6104,2681,6103,2683,6102,2684,6102,2685,6101,2686,6100,2687,6088,2696,6090,2713,6091,2719,6090,2726,6089,2738,6095,2748,6096,2749,6096,2751,6097,2752,6097,2753,6104,2767,6112,2778,6116,2783,6120,2791,6123,2797,6123,2805,6123,2806,6123,2808,6123,2820,6123,2832,6123,2837,6123,2841,6122,2847,6118,2852,6117,2854,6117,2855,6116,2858,6113,2861,6108,2865,6105,2873,6105,2875,6104,2876,6103,2879,6101,2881,6097,2884,6095,2886,6085,2893,6076,2902,6075,2904,6073,2904,6067,2907,6063,2912,6062,2913,6061,2914,6060,2916,6057,2916,6052,2917,6050,2915,6040,2920,6031,2925,6026,2928,6023,2930,6018,2934,6015,2940,6014,2942,6011,2945,6010,2947,6009,2948,6004,2955,6002,2972,6000,2988,5999,2991,5998,2995,5991,3077,5992,3078,5993,3080,6000,3090,6009,3100,6014,3104,6017,3110,6018,3112,6019,3113,6026,3119,6034,3125,6039,3128,6044,3132,6051,3138,6058,3145,6059,3146,6075,3143,6090,3141,6103,3144,6116,3146,6121,3147,6125,3147,6131,3149,6139,3151,6144,3159,6148,3164,6153,3170,6155,3171,6157,3173,6159,3176,6163,3180,6165,3181,6166,3183,6171,3189,6173,3194,6175,3197,6180,3200,6185,3203,6188,3208,6189,3210,6190,3210,6194,3213,6196,3215,6196,3216,6201,3220,6206,3225,6211,3220,6217,3216,6222,3217,6227,3218,6231,3216,6234,3213,6243,3211,6252,3208,6267,3209,6272,3210,6276,3210,6291,3211,6305,3211,6307,3211,6309,3212,6323,3213,6336,3216,6348,3218,6358,3223,6368,3228,6383,3236,6383,3233,6384,3229,6385,3226,6385,3224,6387,3217,6391,3213,6394,3209,6394,3203,6393,3201,6394,3199,6404,3181,6425,3168,6446,3155,6454,3150,6462,3145,6504,3122,6545,3100,6556,3091,6567,3082,6577,3076,6580,3075,6584,3073,6588,3071,6592,3069,6613,3060,6629,3048,6633,3046,6639,3041,6644,3036,6651,3030,6657,3025,6660,3019,6663,3013,6663,3006,6664,3001,6664,2996,6665,2991,6668,2987,6674,2976,6681,2966,6680,2963,6680,2961,6680,2960,6682,2958,6683,2957,6684,2949,6684,2941,6683,2932,6682,2922,6679,2915,6679,2914,6679,2912,6677,2906,6675,2900,6671,2886,6665,2872,6661,2867,6661,2861,6660,2853,6664,2851,6673,2847,6678,2838,6683,2829,6682,2818,6681,2815,6680,2811,6677,2803,6672,2795,6657,2774,6636,2753,6635,2752,6634,2751,6615,2738,6601,2726,6599,2725,6598,2723,6592,2706,6594,2688,6594,2686,6593,2684,6591,2679,6588,2671,6588,2668,6586,2668,6573,2666,6561,2663,6547,2659,6534,2657,6526,2655,6519,2652,6516,2651,6513,2649,6502,2644,6489,2640,6486,2640,6484,2639,6466,2635,6449,2628,6445,2626,6441,2624,6417,2615,6408,2601,6407,2598,6405,2596,6403,2595,6401,2595,f,6389,2599,6390,2613,c]],label:"Boa Vista",shortLabel:"BV",labelPosition:[633.7,291.6],labelAlignment:[t,v]},"CV.MA":{outlines:[[i,5631,4821,f,5632,4813,5627,4807,5619,4796,5606,4795,5596,4795,5589,4799,5584,4803,5576,4809,5565,4819,5551,4821,5547,4821,5545,4819,5537,4814,5528,4811,5525,4810,5522,4808,5513,4801,5503,4797,5489,4791,5479,4781,5465,4766,5458,4751,5458,4756,5457,4761,5456,4764,5457,4769,5458,4779,5448,4784,5446,4785,5444,4787,5442,4789,5440,4789,5433,4791,5426,4790,5419,4790,5419,4796,5420,4799,5421,4800,5432,4804,5427,4818,5419,4844,5403,4864,5402,4865,5401,4866,5391,4873,5385,4878,5383,4880,5381,4880,5366,4878,5356,4886,j,5356,4887,f,5343,4907,5351,4931,5353,4938,5357,4944,5364,4953,5369,4958,5376,4965,5382,4972,5388,4980,5384,4987,5379,4994,5363,5020,5346,5046,5344,5064,5341,5082,5341,5088,5341,5094,5339,5101,5338,5103,5337,5105,5335,5108,5333,5111,5332,5113,5332,5114,5331,5136,5330,5159,5330,5170,5336,5179,5342,5188,5350,5195,5353,5198,5356,5201,5367,5220,5387,5235,5390,5238,5393,5239,5407,5246,5421,5254,5441,5265,5466,5268,5479,5270,5493,5273,5500,5274,5506,5274,5521,5274,5536,5273,5538,5273,5540,5271,5545,5266,5549,5262,5552,5260,5556,5258,5557,5258,5558,5257,5570,5249,5583,5245,5586,5244,5588,5241,5605,5228,5625,5217,5627,5216,5629,5214,5635,5205,5642,5197,5645,5195,5646,5191,5647,5190,5649,5189,5652,5184,5655,5178,5658,5175,5660,5173,5662,5171,5663,5166,5668,5148,5676,5134,5679,5130,5680,5126,5681,5119,5681,5111,5682,5089,5676,5069,5675,5066,5674,5064,5674,5060,5673,5056,5670,5037,5671,5016,5672,4998,5668,4981,5663,4963,5654,4949,5653,4946,5651,4944,5644,4936,5644,4926,5644,4923,5646,4920,5651,4913,5648,4904,5648,4903,5648,4901,5648,4892,5643,4887,5638,4882,5635,4874,5635,4873,5634,4871,5632,4869,5632,4866,f,5631,4844,5631,4821,c]],label:"Maio",shortLabel:"MA",labelPosition:[550.6,501.2],labelAlignment:[t,v]},"CV.BR":{outlines:[[i,1962,5808,f,1958,5803,1956,5798,1953,5792,1949,5788,1944,5782,1935,5784,1927,5787,1920,5790,1902,5799,1883,5809,1882,5810,1880,5810,1872,5810,1864,5811,1849,5811,1835,5808,1836,5827,1837,5846,1837,5850,1835,5853,1833,5856,1825,5856,1818,5859,1813,5863,1813,5865,1811,5865,1806,5866,1805,5868,1801,5874,1801,5881,1801,5911,1801,5940,1801,5942,1802,5942,1806,5944,1810,5944,1813,5944,1815,5944,1817,5945,1819,5945,1823,5946,1825,5948,1829,5955,1835,5962,1844,5974,1859,5981,1862,5983,1866,5985,1867,5985,1869,5986,1872,5987,1875,5989,1888,5998,1900,6006,1906,6010,1913,6011,1915,6011,1916,6011,1929,6007,1939,5996,1940,5996,1940,5995,1951,5989,1964,5983,1966,5983,1967,5981,1973,5974,1977,5966,1979,5962,1981,5958,1985,5952,1984,5943,1982,5928,1986,5915,1986,5913,1987,5912,1988,5910,1988,5909,1989,5899,1989,5889,1989,5885,1988,5881,1987,5872,1984,5863,1982,5857,1980,5851,1980,5850,1979,5848,1976,5842,1974,5835,1974,5833,1973,5832,1973,5830,1972,5829,1970,5819,1964,5811,f,1963,5810,1962,5808,c],[i,2047,5603,f,2039,5608,2036,5615,2034,5617,2036,5621,2038,5625,2040,5629,2044,5636,2055,5633,2062,5631,2069,5628,2074,5626,2076,5620,2078,5616,2083,5613,2088,5610,2087,5604,2087,5599,2085,5595,2080,5587,2070,5585,2062,5584,2059,5588,2058,5588,2058,5589,2054,5597,2049,5602,f,2048,5603,2047,5603,c],[i,1918,5628,f,1919,5629,1920,5630,1924,5632,1926,5636,1931,5643,1940,5642,1942,5641,1943,5640,1950,5632,1958,5624,1959,5623,1959,5623,1960,5615,1960,5606,1960,5604,1959,5603,1958,5600,1954,5599,1947,5599,1940,5599,1939,5600,1938,5601,1934,5605,1930,5609,1924,5615,1922,5623,f,1915,5625,1918,5628,c]],label:"Brava",shortLabel:"BR",labelPosition:[189.9,588.8],labelAlignment:[t,v]},"CV.SF":{outlines:[[i,2640,5523,f,2638,5519,2634,5516,2625,5506,2621,5494,2620,5493,2620,5491,2618,5485,2616,5479,2614,5471,2612,5463,2611,5463,2610,5464,2605,5466,2600,5468,2597,5469,2596,5470,2588,5476,2577,5474,2574,5474,2570,5475,2567,5476,2564,5477,2561,5479,2559,5481,2556,5484,2550,5487,2549,5488,2547,5488,2544,5490,2540,5492,2536,5494,2532,5494,2525,5495,2520,5498,2516,5501,2512,5506,2510,5508,2508,5509,2500,5517,2489,5523,2486,5525,2483,5527,2481,5529,2479,5530,2466,5539,2460,5551,2438,5573,2429,5596,2427,5601,2423,5605,2421,5606,2420,5609,2416,5617,2411,5622,2410,5624,2409,5625,2407,5628,2405,5629,2399,5633,2398,5641,2397,5648,2396,5654,2395,5660,2393,5666,2392,5669,2391,5672,2390,5675,2390,5679,2391,5690,2386,5697,2385,5699,2384,5701,2382,5704,2381,5707,2373,5720,2373,5736,2372,5763,2373,5789,2373,5795,2377,5797,2379,5798,2379,5799,2386,5819,2403,5836,2408,5841,2418,5848,2420,5849,2422,5849,2431,5852,2435,5855,2443,5860,2449,5867,2454,5873,2458,5878,2460,5881,2462,5884,2468,5890,2479,5897,2485,5901,2492,5902,2497,5903,2498,5906,2501,5913,2506,5915,2510,5918,2512,5921,2518,5932,2531,5938,2535,5940,2538,5943,2557,5960,2575,5981,2577,5983,2579,5984,2747,5998,2812,5942,2864,5897,2876,5883,2879,5880,2880,5878,2880,5867,2880,5856,2880,5853,2881,5849,2884,5841,2887,5833,2890,5825,2893,5817,2899,5801,2898,5781,2897,5756,2894,5731,2894,5729,2893,5726,2890,5711,2889,5696,2887,5677,2885,5658,2858,5658,2844,5656,2831,5655,2825,5657,2819,5658,2816,5660,2813,5662,2788,5662,2786,5662,2784,5662,2783,5661,2783,5661,2779,5661,2773,5663,2768,5666,2763,5663,2758,5660,2754,5661,2750,5662,2748,5660,2746,5658,2744,5658,2740,5657,2738,5654,2737,5652,2735,5649,2733,5643,2727,5638,2723,5629,2717,5620,2713,5613,2708,5608,2705,5605,2705,5598,2704,5589,2702,5581,2701,5577,2702,5573,2704,5564,2695,5565,2687,5567,2682,5563,2680,5561,2678,5560,2671,5556,2666,5550,2665,5549,2664,5548,2656,5541,2650,5531,2647,5527,2643,5525,f,2641,5524,2640,5523,c]],label:"Sao Filipe",shortLabel:"SF",labelPosition:[263.5,572.4],labelAlignment:[t,v]},"CV.TF":{outlines:[[i,4233,4761,f,4232,4760,4230,4760,4215,4756,4210,4766,4209,4769,4208,4771,4197,4789,4178,4781,4174,4779,4171,4773,4170,4771,4169,4769,4167,4765,4164,4761,4157,4751,4140,4753,4138,4754,4137,4755,4131,4761,4123,4767,4120,4769,4117,4770,4114,4771,4112,4773,4111,4774,4110,4775,4110,4777,4110,4779,4110,4794,4108,4808,4108,4811,4106,4814,4096,4827,4083,4839,4079,4844,4080,4851,4080,4854,4081,4856,4084,4864,4092,4868,4095,4870,4099,4875,4103,4880,4104,4886,4105,4892,4111,4909,4117,4925,4117,4930,4117,4935,4125,4938,4133,4940,4142,4949,4151,4958,4155,4966,4159,4974,4153,4987,4147,5001,4140,5002,4137,5011,4132,5014,4130,5015,4129,5018,4128,5024,4126,5029,4125,5033,4126,5036,4128,5046,4121,5050,4120,5051,4120,5054,4120,5062,4118,5067,4116,5072,4115,5077,4143,5077,4172,5078,4173,5078,4175,5079,4178,5081,4182,5086,4184,5087,4185,5087,4197,5089,4203,5081,4204,5080,4205,5079,4208,5076,4211,5071,4212,5069,4212,5067,4222,5069,4229,5075,4233,5078,4238,5080,4240,5081,4242,5082,4243,5082,4245,5082,4250,5083,4254,5083,4263,5085,4273,5085,4274,5082,4275,5079,4284,5061,4293,5042,4294,5041,4295,5039,4298,5034,4305,5029,4316,5021,4323,5009,4324,5007,4325,5005,4330,4997,4336,4993,4339,4992,4340,4990,4343,4986,4345,4982,4346,4981,4346,4980,4347,4968,4347,4957,4341,4956,4339,4957,4334,4959,4331,4959,4328,4958,4324,4950,4320,4943,4319,4940,4314,4931,4307,4929,4300,4927,4294,4916,4287,4905,4283,4894,4279,4883,4277,4879,4270,4869,4272,4856,4273,4854,4274,4852,4275,4850,4277,4848,4278,4846,4279,4845,4280,4843,4281,4841,4283,4828,4283,4814,4283,4811,4282,4809,4280,4806,4279,4803,4274,4793,4266,4783,4260,4776,4255,4774,f,4246,4770,4233,4761,c]],label:"Tarrafal",shortLabel:"TF",labelPosition:[421.3,492],labelAlignment:[t,v]},"CV.SM":{outlines:[[i,4431,5002,f,4415,5001,4408,4993,4402,4985,4394,4982,4385,4978,4389,4971,4392,4964,4368,4960,4355,4957,4347,4957,4347,4968,4346,4980,4346,4981,4345,4982,4343,4986,4340,4990,4339,4992,4336,4993,4330,4997,4325,5005,4324,5007,4323,5009,4316,5021,4305,5029,4298,5034,4295,5039,4294,5041,4293,5042,4284,5061,4275,5079,4274,5082,4273,5085,4273,5088,4271,5090,4270,5091,4270,5092,4270,5094,4269,5096,4268,5097,4268,5099,4268,5104,4271,5112,4273,5121,4277,5130,4280,5140,4290,5132,4299,5125,4313,5125,4317,5125,4321,5128,4333,5138,4347,5147,4353,5151,4359,5155,4360,5156,4361,5157,4366,5164,4365,5174,4364,5178,4363,5181,4363,5183,4362,5184,4356,5197,4351,5211,4348,5219,4348,5227,4348,5230,4352,5230,4353,5231,4354,5231,4362,5232,4366,5228,4367,5227,4369,5226,4370,5224,4371,5223,4372,5220,4375,5218,4379,5217,4383,5214,4395,5208,4408,5202,4416,5198,4422,5192,4425,5188,4430,5186,4434,5184,4438,5182,4446,5178,4454,5174,4456,5174,4457,5172,4471,5163,4483,5151,4488,5147,4492,5142,4494,5139,4496,5138,4498,5138,4499,5136,4507,5129,4513,5119,4515,5116,4517,5114,4521,5108,4523,5100,4523,5099,4523,5099,4515,5081,4501,5071,4497,5069,4495,5065,4486,5052,4476,5041,4472,5038,4469,5033,4464,5028,4461,5024,f,4447,5003,4431,5002,c]],label:"Sao Miguel",shortLabel:"SM",labelPosition:[439.5,509.4],labelAlignment:[t,v]},"CV.SZ":{outlines:[[i,4611,5186,f,4607,5185,4604,5183,4585,5169,4565,5181,4544,5192,4549,5174,4554,5155,4544,5140,4533,5124,4524,5101,j,4523,5100,f,4521,5108,4517,5114,4515,5116,4513,5119,4507,5129,4499,5136,4498,5138,4496,5138,4494,5139,4492,5142,4488,5147,4483,5151,4471,5163,4457,5172,4456,5174,4454,5174,4446,5178,4438,5182,4437,5191,4437,5200,4438,5202,4438,5204,4438,5217,4438,5230,4438,5242,4437,5254,4437,5256,4436,5257,4436,5259,4436,5260,4437,5272,4428,5280,4455,5280,4481,5282,4482,5282,4484,5283,4487,5287,4486,5295,4485,5299,4482,5300,4481,5302,4479,5304,4470,5318,4453,5325,4451,5326,4449,5328,4447,5331,4448,5344,4448,5356,4442,5367,4437,5377,4436,5381,4436,5385,4429,5389,4422,5393,4416,5398,4415,5399,4413,5401,4410,5404,4407,5405,4406,5406,4404,5407,4403,5408,4401,5409,4393,5412,4386,5416,j,4386,5416,f,4388,5417,4389,5419,4392,5422,4392,5425,4392,5439,4402,5449,4406,5454,4409,5459,4411,5463,4413,5466,j,4414,5466,f,4422,5468,4432,5468,4448,5467,4464,5466,4466,5466,4468,5465,4481,5458,4494,5454,4496,5454,4498,5454,4502,5453,4506,5452,4518,5448,4528,5440,4530,5438,4532,5436,4543,5426,4549,5412,4552,5405,4558,5399,4565,5391,4573,5390,4581,5389,4586,5395,4590,5399,4594,5403,4606,5412,4618,5422,4620,5423,4621,5424,4624,5427,4628,5430,4635,5435,4644,5436,4658,5436,4672,5436,4673,5436,4674,5435,4683,5432,4690,5428,4692,5428,4693,5426,4697,5424,4700,5419,4701,5417,4703,5414,4706,5409,4709,5404,4710,5403,4710,5402,4711,5395,4716,5390,4717,5389,4717,5386,4720,5373,4726,5361,4731,5353,4737,5346,4739,5343,4742,5340,4732,5339,4731,5324,4730,5310,4725,5306,4719,5301,4717,5293,4715,5285,4713,5248,4697,5238,4695,5238,4672,5241,4667,5239,4662,5237,4659,5235,4656,5232,4655,5223,4653,5213,4646,5204,4645,5203,4643,5202,4641,5201,4639,5200,f,4626,5192,4611,5186,c]],label:"Santa Cruz",shortLabel:"SZ",labelPosition:[456.4,528.4],labelAlignment:[t,v]},"CV.SD":{outlines:[[i,4753,5344,f,4751,5341,4743,5340,j,4742,5340,f,4739,5343,4737,5346,4731,5353,4726,5361,4720,5373,4717,5386,4717,5389,4716,5390,4711,5395,4710,5402,4710,5403,4709,5404,4706,5409,4703,5414,4701,5417,4700,5419,4697,5424,4693,5426,4692,5428,4690,5428,4683,5432,4674,5435,4673,5436,4672,5436,4658,5436,4644,5436,4635,5435,4628,5430,4624,5427,4621,5424,4620,5423,4618,5422,4606,5412,4594,5403,4590,5399,4586,5395,4581,5389,4573,5390,4565,5391,4558,5399,4552,5405,4549,5412,4543,5426,4532,5436,4530,5438,4528,5440,4518,5448,4506,5452,4502,5453,4498,5454,4496,5454,4494,5454,4481,5458,4468,5465,4466,5466,4464,5466,4448,5467,4432,5468,4422,5468,4414,5466,j,4414,5467,f,4424,5479,4433,5492,4435,5495,4436,5497,4440,5500,4440,5505,4441,5520,4439,5535,4439,5537,4438,5539,4434,5545,4429,5549,4425,5552,4427,5560,4429,5574,4443,5579,4444,5579,4446,5580,4449,5581,4452,5583,4460,5588,4467,5593,4474,5599,4482,5600,4490,5602,4497,5602,4504,5603,4510,5603,4518,5604,4524,5601,4527,5599,4530,5598,4537,5595,4544,5592,4546,5591,4547,5591,4549,5590,4550,5589,4555,5587,4559,5587,4562,5587,4565,5586,4566,5585,4568,5585,4572,5585,4575,5583,4578,5581,4581,5580,4582,5579,4584,5579,4604,5579,4624,5578,4626,5578,4627,5577,4634,5574,4640,5569,4644,5565,4653,5566,4657,5566,4662,5566,4680,5565,4695,5573,4698,5575,4702,5576,4706,5576,4710,5578,4712,5579,4713,5579,4719,5579,4723,5582,4725,5583,4727,5584,4731,5586,4737,5587,4739,5588,4740,5588,4750,5591,4761,5596,4762,5596,4764,5597,4766,5598,4767,5598,4769,5599,4770,5599,4782,5601,4791,5607,4793,5608,4795,5608,4802,5609,4807,5613,4810,5615,4811,5617,4812,5618,4814,5619,4817,5609,4831,5600,4835,5598,4838,5596,4861,5588,4874,5575,4877,5573,4878,5569,4879,5561,4875,5555,4873,5553,4872,5549,4871,5545,4868,5541,4855,5522,4858,5496,4859,5486,4853,5479,4847,5472,4845,5464,4844,5457,4840,5450,4839,5448,4835,5433,4819,5431,4803,5431,4801,5431,4798,5431,4790,5428,4789,5419,4786,5405,4778,5394,4765,5375,4758,5354,4757,5351,4756,5349,f,4755,5346,4753,5344,c]],label:"Sao Domingos",shortLabel:"SD",labelPosition:[464.6,547.9],labelAlignment:[t,v]},"CV.PI":{outlines:[[i,4568,5585,f,4566,5585,4565,5586,4562,5587,4559,5587,4555,5587,4550,5589,4549,5590,4547,5591,4546,5591,4544,5592,4537,5595,4530,5598,4527,5599,4524,5601,4518,5604,4510,5603,4504,5603,4497,5602,4490,5602,4482,5600,4474,5599,4467,5593,4460,5588,4452,5583,4449,5581,4446,5580,4444,5579,4443,5579,4429,5574,4427,5560,4425,5552,4429,5549,4434,5545,4438,5539,4439,5537,4439,5535,4441,5520,4440,5505,4440,5500,4436,5497,4435,5495,4433,5492,4424,5479,4414,5467,j,4413,5466,f,4411,5463,4409,5459,4406,5454,4402,5449,4392,5439,4392,5425,4392,5422,4389,5419,4388,5417,4386,5416,j,4386,5416,f,4375,5409,4363,5410,4360,5410,4358,5411,4352,5412,4347,5416,4345,5417,4344,5418,4342,5418,4341,5420,4335,5427,4337,5438,4338,5447,4333,5451,4321,5461,4305,5463,4304,5464,4302,5465,4300,5466,4297,5466,4291,5465,4287,5469,4280,5476,4277,5485,4274,5492,4275,5500,4275,5504,4276,5508,4277,5513,4272,5516,4271,5517,4270,5518,4269,5532,4269,5546,4269,5548,4269,5550,4268,5552,4267,5553,4265,5561,4258,5567,4245,5577,4237,5590,4233,5596,4227,5601,4222,5606,4215,5607,4223,5616,4225,5624,4226,5632,4232,5635,4238,5638,4245,5643,4253,5647,4263,5659,4273,5671,4283,5678,4293,5684,4310,5690,4326,5696,4330,5699,4335,5701,4342,5706,4348,5711,4354,5714,4359,5716,4365,5722,4371,5727,4378,5728,4391,5731,4402,5738,4405,5739,4408,5740,4412,5742,4414,5744,4415,5747,4421,5753,4426,5758,4442,5755,4458,5752,4461,5752,4474,5754,4485,5760,4488,5762,4491,5763,4498,5766,4506,5768,4508,5768,4522,5769,4536,5769,4551,5770,4566,5771,4578,5776,4590,5780,4613,5783,4620,5784,4639,5783,4658,5781,4672,5785,4685,5789,4690,5786,4695,5783,4698,5781,4705,5775,4714,5773,4717,5772,4721,5772,4737,5772,4753,5771,4762,5770,4756,5759,4751,5747,4781,5696,4811,5645,4811,5641,4811,5636,4813,5624,4813,5621,4814,5619,4812,5618,4811,5617,4810,5615,4807,5613,4802,5609,4795,5608,4793,5608,4791,5607,4782,5601,4770,5599,4769,5599,4767,5598,4766,5598,4764,5597,4762,5596,4761,5596,4750,5591,4740,5588,4739,5588,4737,5587,4731,5586,4727,5584,4725,5583,4723,5582,4719,5579,4713,5579,4712,5579,4710,5578,4706,5576,4702,5576,4698,5575,4695,5573,4680,5565,4662,5566,4657,5566,4653,5566,4644,5565,4640,5569,4634,5574,4627,5577,4626,5578,4624,5578,4604,5579,4584,5579,4582,5579,4581,5580,4578,5581,4575,5583,f,4572,5585,4568,5585,c]],label:"Praia",shortLabel:"PI",labelPosition:[451.4,566.3],labelAlignment:[t,v]},"CV.SC":{outlines:[[i,4347,5147,f,4333,5138,4321,5128,4317,5125,4313,5125,4299,5125,4290,5132,4280,5140,4277,5130,4273,5121,4271,5112,4268,5104,4268,5099,4268,5097,4269,5096,4270,5094,4270,5092,4270,5091,4271,5090,4273,5088,4273,5085,4263,5085,4254,5083,4250,5083,4245,5082,4243,5082,4242,5082,4240,5081,4238,5080,4233,5078,4229,5075,4222,5069,4212,5067,4212,5069,4211,5071,4208,5076,4205,5079,4204,5080,4203,5081,4197,5089,4185,5087,4184,5087,4182,5086,4178,5081,4175,5079,4173,5078,4172,5078,4143,5077,4115,5077,4114,5078,4114,5079,4114,5081,4113,5084,4111,5093,4107,5101,4105,5104,4103,5107,4102,5110,4099,5113,4098,5115,4096,5117,4095,5119,4095,5121,4095,5166,4095,5211,4095,5219,4092,5224,4089,5229,4089,5234,4089,5239,4091,5245,4093,5251,4092,5266,4091,5281,4090,5292,4088,5304,4087,5306,4086,5317,4075,5324,4061,5332,4057,5349,4057,5351,4056,5354,4055,5365,4054,5376,4054,5387,4058,5396,4062,5406,4075,5406,4079,5406,4083,5409,4097,5419,4101,5436,4103,5444,4108,5451,4111,5457,4114,5463,4115,5466,4118,5468,4122,5470,4125,5472,4128,5474,4131,5475,4133,5476,4135,5476,4182,5485,4195,5501,4208,5516,4214,5529,4219,5541,4212,5549,4205,5556,4205,5565,4206,5573,4204,5577,4202,5581,4202,5586,4203,5595,4213,5605,4214,5606,4215,5607,4222,5606,4227,5601,4233,5596,4237,5590,4245,5577,4258,5567,4265,5561,4267,5553,4268,5552,4269,5550,4269,5548,4269,5546,4269,5532,4270,5518,4271,5517,4272,5516,4277,5513,4276,5508,4275,5504,4275,5500,4274,5492,4277,5485,4280,5476,4287,5469,4291,5465,4297,5466,4300,5466,4302,5465,4304,5464,4305,5463,4321,5461,4333,5451,4338,5447,4337,5438,4335,5427,4341,5420,4342,5418,4344,5418,4345,5417,4347,5416,4352,5412,4358,5411,4360,5410,4363,5410,4375,5409,4386,5416,4393,5412,4401,5409,4403,5408,4404,5407,4406,5406,4407,5405,4410,5404,4413,5401,4415,5399,4416,5398,4422,5393,4429,5389,4436,5385,4436,5381,4437,5377,4442,5367,4448,5356,4448,5344,4447,5331,4449,5328,4451,5326,4453,5325,4470,5318,4479,5304,4481,5302,4482,5300,4485,5299,4486,5295,4487,5287,4484,5283,4482,5282,4481,5282,4455,5280,4428,5280,4437,5272,4436,5260,4436,5259,4436,5257,4437,5256,4437,5254,4438,5242,4438,5230,4438,5217,4438,5204,4438,5202,4437,5200,4437,5191,4438,5182,4434,5184,4430,5186,4425,5188,4422,5192,4416,5198,4408,5202,4395,5208,4383,5214,4379,5217,4375,5218,4372,5220,4371,5223,4370,5224,4369,5226,4367,5227,4366,5228,4362,5232,4354,5231,4353,5231,4352,5230,4348,5230,4348,5227,4348,5219,4351,5211,4356,5197,4362,5184,4363,5183,4363,5181,4364,5178,4365,5174,4366,5164,4361,5157,4360,5156,4359,5155,f,4353,5151,4347,5147,c]],label:"Santa Catarina",shortLabel:"SC",labelPosition:[424,528.7],labelAlignment:[t,v]}}}];
g=d.length;if(r){while(g--){e=d[g];n(e.name.toLowerCase(),e,n.geo);}}else{while(g--){e=d[g];u=e.name.toLowerCase();a(s,u,1);h[s].unshift({cmd:"_call",obj:window,args:[function(w,x){if(!n.geo){p.raiseError(p.core,"12052314141","run","JavaScriptRenderer~Maps._call()",new Error("FusionCharts.HC.Maps.js is required in order to define vizualization"));
return;}n(w,x,n.geo);},[u,e],window]});}}}]);