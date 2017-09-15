/* my.js
This script should copy CSV data into an array and then create an array full of features.
*/

function prt(inp){console.log(inp)}

function d3csv_callback(csv_a) {
    /* This function should expose CSV data from d3.csv().
        The data appears in parameter: csv_a. */
    csv_a
    // I should move syntax below into a func:
    var data   = csv_a
    var period = 3
    var i
    var j
    var l = csv_a.length
    var sum    = 0
    var buffer = data.slice(0, period)

    for (i=period;i<l;i++) {
	sum= 0
	for (j=period;j>0;j--) {
	    sum += data[i-j][1];
	}
	    buffer[i] = [data[i][0], sum/period];
    }

    buffer // mvg avg s.b. in buffer now?
    // I should move syntax above into a func:
}

function d3csv_rowparse(row) {
    // This function should operate on each row in CSV data from d3.csv()
    return [row.Date, +row.Close]
}

d3.csv('/static/^GSPC.csv',d3csv_rowparse,d3csv_callback)

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
