/* my.js
This script should copy CSV data into an array and then create an array full of features.
*/

function d3csv_callback(csv_a) {
    // This function should expose CSV data from d3.csv() via parameter: csv_a.
    csv_a
}

function d3csv_rowparse(row) {
    return [row.Date, +row.Close]
}

d3.csv('/static/^GSPC.csv',d3csv_rowparse,d3csv_callback)

'bye'
