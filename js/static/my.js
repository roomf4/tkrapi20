// my.js
// This script should copy CSV data into an array and then create an array full of features.

my_a = [1.1,2.2,3.3]

function d3csv_callback(arg0) {
    arg0
    true
}

function d3csv_rowparse(row) {
    row
    row.Date
    row.Close
    return [row.Date, +row.Close]
}

d3.csv('/static/^GSPC.csv',d3csv_rowparse,d3csv_callback)

'bye'
