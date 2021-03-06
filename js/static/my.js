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

function mvgavg0(input_a,window_i) {
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

function slopemv(cp_a, wdw_i) {
    // This function should return a normalized slope of a price mvg avg over a window.
    // Output should match output of py/genf.py
    // I should get mvg avg:
    var mvav_a = mvav(cp_a,wdw_i)
    // I should get normalized diff:
    var len_i = mvav_a.length
    var slp_a = [0] // Initially slope s.b. 0.0
    for (c_i=1; c_i<len_i; c_i++) {
        var diff_f = 100*(mvav_a[c_i]-mvav_a[c_i-1])/mvav_a[c_i]
        // Assuming mvav_a[c_i] != 0
        slp_a[c_i] = diff_f
    }
    return slp_a
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
    var pctlead_a = col_a.slice()
    var len_i     = col_a.length
    var end_i     = len_i - 1 // s.b. place to stop
    pctlead_a[end_i] = 0.0    // s.b. good default
    // I should start filling:
    for (c_i=0; c_i<end_i; c_i++) {
        head_f         = col_a[c_i+1]   
        lag_f          = col_a[c_i  ]
        pctlead_a[c_i] = 100*(head_f-lag_f)/lag_f
    }
    return pctlead_a
}


function mvav(cp_a,wdw_i) {
    // This function should return array with mvg avg over wdw_i.
    var mvav_a       = cp_a.slice()
    var len_i        = cp_a.length
    var start_mvav_i = wdw_i-1 // I should start filling mvav_a here.
    for (c_i=start_mvav_i; c_i<len_i; c_i++) {
        var wdwstart_i = c_i - wdw_i+1
        var wdwend_i   = c_i+1
        // I should calc mean over window:
        var wdw_a   = cp_a.slice(wdwstart_i,wdwend_i)
        mvav_a[c_i] = d3.mean(wdw_a)
    }
    return mvav_a
}

function genf(cdate_a,cp_a) {
    // This function should generate features from cdate_a and cp_a.
    var features_o = {} // I should fill this
    // I should generate pct_lead:
    features_o['cdate']   = cdate_a
    features_o['cp']      = cp_a
    features_o['pctlead'] = pctlead(cp_a)
    features_o['pctlag1'] = pctlag(cp_a,1)
    features_o['pctlag2'] = pctlag(cp_a,2)
    features_o['pctlag4'] = pctlag(cp_a,4)
    features_o['pctlag8'] = pctlag(cp_a,8)
    var slp_a = [3,4,5,6,7,8,9]
    for (s_i=0; s_i<slp_a.length; s_i++){
        var slp_s   = 'slope'+slp_a[s_i]
        var slope_a = slopemv(cp_a, slp_a[s_i])
        features_o[slp_s] = slope_a
    }
    // I should generate Day-of-week, Month-of-year:
    features_o['dow'] = cdate_a.map(function(d_s) {return new Date(d_s+'T20:00:00Z').getDay()/100.0})
    features_o['moy'] = cdate_a.map(function(d_s) {return +d_s.substring(5,7)/100.0})
    return features_o
}

function d3csv_callback(csv_a) {
    /* This function should expose CSV data from d3.csv().
        The data appears in parameter: csv_a. */
    var csv_o   = csva2o(csv_a)
    // I should get cdate_a and cp_a for genf():
    var cp_a    = csv_o.cp
    var cdate_a = csv_o.cdate
    var feat_o  = genf(cdate_a,cp_a)
    'bye'
    /* debug:
    var tst_a = [0,1,2,3,4,5,6,7,8,9]
    mvav3_a = mvav(tst_a,3)
    mvav3_a
    var slp3_a = slopemv(tst_a, 3)
    slp3_a
    csv_a
    var pctlag1_a = pctlag(cp_a,1)
    var pctlag2_a = pctlag(cp_a,2)
    var pctlag4_a = pctlag(cp_a,4)
    var pctlag8_a = pctlag(cp_a,8)
    var pctlead_a = pctlead(cp_a)
    pctlead_a
    var slp3_a = slopemv(cp_a, 3)
    slp3_a
    csv_o.slope3
    */
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
