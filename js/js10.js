// js10.js

// This script should demo nodejs.

function p(inp) {
  console.log(inp)
}

var hello = 123.4
hello = 123.45
p(hello)

my_a = [1.1,2.2,3.2,4.4,5.1,6.2,7.7,8.3,9.9]
p(my_a)

// Ref:
// https://www.npmjs.com/package/timeseries-analysis

var timeseries = require("timeseries-analysis");

var ts_a = [
['2017-03-02',24.00]
,['2017-03-03',26.38]
,['2017-03-06',28.17]
,['2017-03-07',22.20]
,['2017-03-08',22.03]
,['2017-03-09',23.17]
,['2017-03-10',23.36]
,['2017-03-13',22.04]
,['2017-03-14',20.90]
,['2017-03-15',20.08]
,['2017-03-16',20.65]
,['2017-03-17',19.79]
,['2017-03-20',19.94]
,['2017-03-21',20.04]
,['2017-03-22',20.65]
,['2017-03-23',22.69]
,['2017-03-24',23.04]
,['2017-03-27',23.09]
,['2017-03-28',23.30]
,['2017-03-29',21.77]
,['2017-03-30',22.54]
,['2017-03-31',22.04]
]

// Load the data
var my_ts = new timeseries.main(ts_a)
// fails?: my_ts.chart()
// var mychart = my_ts.chart() // this work?

// p(ts_a)
//p(my_ts.output())

// my_ts.save('sv10')
// p(my_ts.saved)

// mvg avg:
debugger
var ur_ts = my_ts.ma({period: 3})
p(ur_ts)

'bye'
