/* my.js
This script should copy CSV data into an array and then create an array full of features.
The features should match features created by Pandas.
*/

function csva2o(csv_a) {
    csvlen_i = csv_a.length
    col_a    = csv_a.columns
    collen_i = col_a.length
    csv_o = {} // w.b. object full of arrays
    // I should convert array full of objects into
    // object full of arrays:            
    // I should loop through column names:
    for (col_i=0; col_i<collen_i; col_i++) {
        col_s        = col_a[col_i]
        csv_o[col_s] = []
        // I should loop through csv_a:
        for(row_i=0; row_i<csvlen_i; row_i++) {
            var row = csv_a[row_i]
            csv_o[col_s].push(row[col_s])
        }
    }
    return csv_o
}

function prt(inp){console.log(inp)}

function mvgavg(input_a,window_i) {
    // This function should create a moving avg from a time series of numbers.
    // input_a s.b. like: [['2017-01-02',44.4],['2017-01-03',45.8]]
    var outer_i
    var inner_i
    var l = input_a.length
    var sum    = 0
    var output_a = input_a.slice(0, window_i-1)
    for (outer_i=window_i;outer_i<l+1;outer_i++) {
        sum= 0
        for (inner_i=window_i;inner_i>0;inner_i--) {
            sum += input_a[outer_i-inner_i][1]
        }
        output_a[outer_i-1] = [input_a[outer_i-1][0], sum/window_i]
    }
    return output_a
}

function lag(col_a,wdw_i) {
    // This function should return array which lags col_a by wdw_i.
    var lag_a = col_a.slice()
    var len_i = col_a.length
    var start_lag_i = wdw_i // I should start filling lag_a here.
    for (c_i=start_lag_i; c_i<len_i; c_i++) {
        lag_a[c_i] = col_a[c_i - wdw_i]
    }
    return lag_a
}

function pctlag(col_a,wdw_i) {
    // This function should return array which has pctlags between values in col_a.
    // I should assume col_a contains numbers.
    var pctlag_a    = col_a.slice()
    var len_i       = col_a.length
    var start_lag_i = wdw_i // I should start filling lag_a here.
    for (c_i=0; c_i<start_lag_i; c_i++) {
        pctlag_a[c_i] = 0.0 // s.b. good default
    }
    // I should start filling:
    for (c_i=start_lag_i; c_i<len_i; c_i++) {
        head_f        = col_a[c_i]
        lag_f         = col_a[c_i - wdw_i]
        pctlag_a[c_i] = 100*(head_f-lag_f)/lag_f
    }
    return pctlag_a
}

function pctlead(col_a) {
    // This function should return array which has pctleads between values in col_a.
    // I should assume col_a contains numbers.
    var pctlead_a      = col_a.slice()
    var len_i          = col_a.length
    pctlead_a[len_i-1] = 0.0 // s.b. good default
    // I should start filling:
    for (c_i=0; c_i<start_lead_i-1; c_i++) {
        head_f         = col_a[c_i+1]   
        lag_f          = col_a[c_i  ]
        pctlead_a[c_i] = 100*(head_f-lag_f)/lag_f
    }
    return pctlead_a
}


function d3csv_callback(csv_a) {
    /* This function should expose CSV data from d3.csv().
        The data appears in parameter: csv_a. */
    csv_a
    var csv_o = csva2o(csv_a)
    var cp_a  = csv_o.cp
    var pctlag1_a = pctlag(cp_a,1)
    var pctlag2_a = pctlag(cp_a,2)
    var pctlag4_a = pctlag(cp_a,4)
    var pctlag8_a = pctlag(cp_a,8)
    csv_o.pct_lead
    var pctlead_a = pctlead(cp_a)
    pctlead_a
}

function d3csv_rowparse(row) {
    // Currently this function is not used.
    // This function should operate on each row in CSV data from d3.csv()
    return [row.Date, +row.Close]
}

d3.csv('/static/featFB.csv',d3csv_callback)

'bye'

/*
Ref:
https://github.com/26medias/timeseries-analysis

// Moving Average
timeseries.prototype.ma = function(options) {
        options = _.extend({
                period:         12
        }, options);
        var i;
        var j;
        var l   = this.data.length;
        var sum = 0;
        
        // Reset the buffer
        this.buffer     = [];
        
        // Leave the datapoints [0;period[ intact
        this.buffer = this.data.slice(0, options.period);
        
        for (i=options.period;i<l;i++) {
                sum     = 0;
                for (j=options.period;j>0;j--) {
                        sum += this.data[i-j][1];
                }
                this.buffer[i] = [this.data[i][0], sum/options.period];
        }
        this.data = this.buffer;
        return this;
}
*/
