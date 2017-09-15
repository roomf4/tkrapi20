/* my.js
This script should copy CSV data into an array and then create an array full of features.
The features should match features created by Pandas.
*/

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

function d3csv_callback(csv_a) {
    /* This function should expose CSV data from d3.csv().
        The data appears in parameter: csv_a. */
    csv_a
    var mvgavg_a = mvgavg(csv_a,3)
    mvgavg_a
}

function d3csv_callback2(csv_a) {
    /* This function should expose CSV data from d3.csv().
        The data appears in parameter: csv_a. */
    csv_a
}

function d3csv_rowparse(row) {
    // This function should operate on each row in CSV data from d3.csv()
    return [row.Date, +row.Close]
}
/* First method:
d3.csv('/static/^GSPC.csv',d3csv_rowparse,d3csv_callback)
*/

d3.csv('/static/features.csv',d3csv_callback2)


'bye'
/*
Ref:
https://github.com/26medias/timeseries-analysis

// Moving Average
timeseries.prototype.ma = function(options) {
	options = _.extend({
		period:		12
	}, options);
	var i;
	var j;
	var l 	= this.data.length;
	var sum	= 0;
	
	// Reset the buffer
	this.buffer 	= [];
	
	// Leave the datapoints [0;period[ intact
	this.buffer = this.data.slice(0, options.period);
	
	for (i=options.period;i<l;i++) {
		sum	= 0;
		for (j=options.period;j>0;j--) {
			sum += this.data[i-j][1];
		}
		this.buffer[i] = [this.data[i][0], sum/options.period];
	}
	this.data = this.buffer;
	return this;
}
*/
