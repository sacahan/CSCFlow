## 網頁直接顯示的運動中心
| 運動中心 | 官方網站 URL | 健身房 | 游泳池 | 健身房容留人數 | 游泳池容留人數 |
| -------- | ------------ | ------ | ------ | -------------- | -------------- |
| 台北市北投運動中心 | [https://www.btsport.org.tw/](https://www.btsport.org.tw/) | 是 | 是 | 60 | 200 |
| 台北市士林運動中心 | [https://www.slsc-taipei.org/](https://www.slsc-taipei.org/) | 是 | 是 | 100 | 200 |
| 台北市松山運動中心 | [http://sssc.com.tw/](http://sssc.com.tw/) | 是 | 是 | 100 | 400 |
| 台北市大同運動中心 | [https://www.dtsc-wdyg.com.tw/](https://www.dtsc-wdyg.com.tw/) | 是 | 是 | 90 | 250 |
| 台北市中正運動中心 | [https://wsjjsc.com.tw/](https://wsjjsc.com.tw/) | 是 | 是 | 120 | 200 |
| 台北市萬華運動中心 | [https://whsc.com.tw/](https://whsc.com.tw/) | 是 | 是 | 150 | 100 |
| 新北市蘆洲國民運動中心 | [https://lzsc.chanchao.com.tw/](https://lzsc.chanchao.com.tw/) | 是 | 是 | 75 | 200 |
| 新北市淡水國民運動中心 | [http://www.tssc.tw/](http://www.tssc.tw/) | 是 | 是 | 60 | 300 |
| 新北市五股國民運動中心 | [https://wgsc.chanchao.com.tw/](https://wgsc.chanchao.com.tw/) | 是 | 是 | - | - |

## API 資料來源的運動中心
| 運動中心               | 官方網站 URL                                                       | 健身房 | 游泳池 | API 端點                                                       | 請求方法 | 回應格式範例                       | 健身房容留人數 | 游泳池容留人數 |
| ---------------------- | ------------------------------------------------------------------ | ------ | ------ | ------------------------------------------------------------ | -------- | ---------------------------------- | -------------- | -------------- |
| 台北市內湖運動中心     | [https://nhsc.cyc.org.tw/](https://nhsc.cyc.org.tw/)               | 是     | 是     | https://nhsc.cyc.org.tw/api                                   | POST     | {"gym":[""],"swim":[""]}          | 130            | 200            |
| 台北市南港運動中心     | [http://ngsc.cyc.org.tw/](http://ngsc.cyc.org.tw/)                 | 是     | 是     | https://ngsc.cyc.org.tw/api                                   | POST     | {"gym":["79","130","0"],"swim":["25","200","0"]} | -       | -       |
| 台北市信義運動中心     | [https://xysc.teamxports.com/](https://xysc.teamxports.com/)       | 是     | 是     | https://api.teamxports.com/XPORTS-API                        | POST     | {"Now":"40","Max":"165","Other":"0"} | 65             | 165            |
| 台北市中山運動中心     | [https://cssc.cyc.org.tw/](https://cssc.cyc.org.tw/)               | 是     | 是     | https://cssc.cyc.org.tw/api                                   | POST     | {"gym":["25","50","0"],"swim":["39","150","0"]} | 50             | 150            |
| 台北市文山運動中心     | [https://wssc.cyc.org.tw/](https://wssc.cyc.org.tw/)               | 是     | 是     | https://wssc.cyc.org.tw/api                                   | POST     | {"gym":["28","110","0"],"swim":["48","200","0"],"ice":["0","120","0"]} | 110            | 200            |
| 新北市新莊國民運動中心 | [https://www.xzsports.com.tw/](https://www.xzsports.com.tw/)       | 是     | 是     | https://www.xzsports.com.tw/parser.php                        | GET      | 44,152                             | 150            | 250            |
| 新北市三重國民運動中心 | [https://www.scsports.com.tw/](https://www.scsports.com.tw/)       | 是     | 是     | http://www.scsports.com.tw/proxy1.php                        | GET      | {"swim":["58","400","0"],"gym":["26","60","0"]} | 60             | 400            |
| 新北市土城國民運動中心 | [https://www.tcsports.com.tw/](https://www.tcsports.com.tw/)       | 是     | 是     | https://www.tcsports.com.tw/proxy1.php                        | GET      | {"swim":["017","280","000"],"gym":["042","120","000"],"ice":["000","250","000"]} | 120            | 280            |
| 新北市中和國民運動中心 | [https://www.zhsc.com.tw/](https://www.zhsc.com.tw/)               | 是     | 是     | https://zhs.mraytec.com/state/{fitness:健身房;pool:游泳池} | GET      | {"value":118}                     | 120            | 300            |
| 新北市樹林國民運動中心 | [https://www.ntcslsports.com.tw/](https://www.ntcslsports.com.tw/) | 是     | 是     | https://www.ntcslsports.com.tw/parser.php                    | GET      | 10,11                              | 90             | 250            |
| 新北市鶯歌國民運動中心 | [https://ygsc.teamxports.com/](https://ygsc.teamxports.com/)       | 否     | 否     | https://webapi.teamxports.com/api/web/carosel/get-court-cat-people-flow?siteId=6 | GET      | {"returnCode": "200","returnMsg": "成功","data": [{"courtCatTitle": "體適能中心","upperBound": 70,"currCapacity": 1,"capacityControl": 1}]} | 70             | -       |
| 新北市三峽國民運動中心 | [https://sxsc.teamxports.com/](https://sxsc.teamxports.com/)       | 是     | 是     | https://webapi.teamxports.com/api/web/carosel/get-court-cat-people-flow?siteId=7 | GET     | {"returnCode": "200","returnMsg": "成功","data": [{"courtCatTitle": "健身房","upperBound": 65,"currCapacity": 6,"capacityControl": 1},{"courtCatTitle": "游泳池","upperBound": 250,"currCapacity": 31,"capacityControl": 1}]} | 65             | 250            |
| 新北市林口國民運動中心 | [https://lkcsc.cyc.org.tw/](https://lkcsc.cyc.org.tw/)             | 是     | 是     | https://lkcsc.cyc.org.tw/api                                   | POST     | {"gym":["0","80","0"],"swim":["0","230","0"]} | 80             | 230            |

## Lazy load URL 資料來源的運動中心
| 運動中心 | 官方網站 URL | 健身房 | 游泳池 | API 端點 | 健身房容留人數 | 游泳池容留人數 |
| -------- | ------------ | ------ | ------ | -------- | -------------- | -------------- |
| 台北市大安運動中心 | [https://www.daansports.com.tw/](https://www.daansports.com.tw/) | 是 | 是 | https://www.daansports.com.tw/zh_TW/onsitenum | 80 | 250 |
| 新北市板橋國民運動中心 | [https://www.bqsports.com.tw/](https://www.bqsports.com.tw/) | 是 | 是 | https://www.bqsports.com.tw/zh-TW/onsitenum | - | 140 |
| 新北市新店國民運動中心 | [https://www.xdsports.com.tw/](https://www.xdsports.com.tw/) | 是 | 是 | https://www.xdsports.com.tw/zh_TW/onsitenumonsitenum | 100 | 180 |
