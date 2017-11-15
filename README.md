# README.md

The software in this repo was developed on Ubuntu 16.

If you want to run the demos on your laptop, you should install Ubuntu 16 on your laptop.

If you are on Mac or windows, a straightforward way to do this is to install VirtualBox.

After you install VirtualBox, download the file listed below and then import it into VirtualBox.

https://drive.google.com/file/d/1LMoQWKFtcBAj6B1vYSrLK_b4ZdbgDniR/

Next, I cloned this repo using a simple shell command:

```bash
cd ~dan
git clone ssh://git@bitbucket.org/bikle/tkrapi20.git
```

Next, I worked with Postgres so this repo could interact with database tables.

I issued some shell commands:

```bash
sudo apt-get install postgresql postgresql-server-dev-all libpq-dev
sudo su - postgres
psql
```

At this point I was inside the psql interface which accepts both Postgres and SQL commands.

I typed three commands:

```sql
create database tkrapi;
create role tkrapi with login superuser password 'tkrapi';
\q
```

Next, I ran the first demo by issuing some shell commands:

```bash
cd ~ann
cd tkrapi20
. env.bash
python
```

I saw in the Python banner that I was running this:

```
ann@tkrapi:~/tkrapi20 $ python
Python 3.6.3 |Anaconda, Inc.| (default, Oct 13 2017, 12:02:49) 
[GCC 7.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> quit()
```

The next demo I ran was a single shell command which is listed below:

```bash
conda install flask keras numpy pandas psycopg2 sqlalchemy
```

The above command finished after 90 seconds.

Next, I ran this shell command:

```bash
conda install flask-restful -c conda-forge
```

But first we need to get some data.

# Get Data

I used shell commands listed below to get stock price data:

```bash
cd ~/tkrapi20
bin/request_tkr.bash
```

The above script needs between 5 and 6 hours to run.

I ran it on my laptop; after it finished I checked the disk usage:

```bash
ann@ub16aug:~/tkrapi20$ du -sh ~/tkrcsv/*
2.9M	/home/ann/tkrcsv/div
255M	/home/ann/tkrcsv/history
2.9M	/home/ann/tkrcsv/split
ann@ub16aug:~/tkrapi20$ 
ann@ub16aug:~/tkrapi20$ 
```

The above script depends on tkrlist.txt, a list of 728 tickers, to declare which stocks to get.

If I am in a hurry, I update the script so it uses tkrlist_small.txt which lists these tickers:

```bash
ann@ub16aug:~/tkrapi20$ ll
total 104
drwxrwxr-x  7 ann ann  4096 Aug 24 00:11 .
drwxr-xr-x 41 ann ann  4096 Aug 24 00:10 ..
drwxrwxr-x  2 ann ann  4096 Aug 24 00:08 bin
-rw-rw-r--  1 ann ann   372 Aug 23 20:29 cr_tkrapi.sql
-rw-rw-r--  1 ann ann  5055 Aug 23 20:29 dev.py
-rw-rw-r--  1 ann ann   565 Aug 23 20:39 env.bash
-rw-rw-r--  1 ann ann  2685 Aug 23 21:04 features.txt
-rwxrwxr-x  1 ann ann   181 Aug 23 20:29 flaskr.bash
-rw-rw-r--  1 ann ann 10178 Aug 23 20:29 flaskr.py
drwxrwxr-x  8 ann ann  4096 Aug 24 00:08 .git
-rw-rw-r--  1 ann ann    12 Aug 23 20:29 .gitignore
-rw-rw-r--  1 ann ann  2218 Aug 23 20:29 meetup.txt
drwxrwxr-x  2 ann ann  4096 Aug 23 23:28 py
-rw-rw-r--  1 ann ann  5196 Aug 24 00:08 README.md
-rw-rw-r--  1 ann ann   713 Aug 23 20:29 README.old.md
-rw-rw-r--  1 ann ann    15 Aug 23 20:29 requirements.txt
-rw-rw-r--  1 ann ann    13 Aug 23 20:29 runtime.txt
drwxrwxr-x  2 ann ann  4096 Aug 23 20:29 static
drwxrwxr-x  2 ann ann  4096 Aug 23 20:29 tests
-rw-rw-r--  1 ann ann    70 Aug 23 20:29 tkrlist_small.txt
-rw-rw-r--  1 ann ann  3030 Aug 23 20:29 tkrlist.txt
-rw-rw-r--  1 ann ann    40 Aug 23 20:29 years.txt
ann@ub16aug:~/tkrapi20$ 
ann@ub16aug:~/tkrapi20$ wc -l tkrlist.txt
728 tkrlist.txt
ann@ub16aug:~/tkrapi20$ 
ann@ub16aug:~/tkrapi20$ cat tkrlist_small.txt 
^GSPC
^RUT
QQQ
DIA
GLD
TLT
AAPL
AMZN
BAC
FB
GOOG
JNJ
JPM
MSFT
WFC
XOM
ann@ub16aug:~/tkrapi20$ 
ann@ub16aug:~/tkrapi20$
```

The script bin/request_tkr.bash, depends on py/request_tkr.py which depends on the Python requests package:

http://docs.python-requests.org

If you study request_tkr.py you will see it sends an initial request to a URL like this:

https://finance.yahoo.com/quote/IBM

Yahoo responds to that request with two pieces of information I need to track.

The first piece is in a browser cookie.

The second piece, I call it a crumb, is embedded within the HTML response from Yahoo.

The next request goes to a url like this:

https://finance.yahoo.com/quote/IBM/history?p=IBM

Then, another request goes to a url like this:

https://query1.finance.yahoo.com/v7/finance/download/IBM?period1=-631123200&period2=1503561650&interval=1d&events=div&crumb=UCaZNLyqkGQ

Notice the crumb parameter at the end.

The Python script request_tkr.py figures out what that crumb should be by using a regexp search against a previous Yahoo HTML response.

If I send the wrong crumb (a crumb which fails to match my cookie), Yahoo responds with this friendly message:

```json
{
    "finance": {
        "error": {
            "code": "Unauthorized",
            "description": "Invalid cookie"
        }
    }
}
```

That is the only 'tricky' part of the script; the rest is plain-old web-scraping.

When Yahoo sees the above request, it usually responds with a CSV file after it matches the crumb with the cookie it had served me earlier.

I'm not sure why Yahoo is serving crumbs and cookies which frequently change but I thought that solving the puzzle was fun.

After the above script finishes, I run another script to copy all the CSV data into a Postgres table.

That script is named: csv2db.bash which wraps csv2db.py

I should run csv2db.bash after request_tkr.bash finishes.

The shell commands in csv2db.bash are listed below:

```bash
#!/bin/bash

# csv2db.bash

# This script should insert csv files into a table.
# This script will hang if the FlaskRESTful server is running.
# So I should shutdown the server before I run this script.

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd ${SCRIPTPATH}/../

. env.bash
bin/rmbad_cookies.bash
$PYTHON py/csv2db.py

exit
```

I ran the above script on my laptop and it finished in about 30 seconds.

The script rmbad_cookies.bash removes CSV files which contain error messages from Yahoo rather than good data.

After I run csv2db.py, I am ready to generate machine learning features from dates and prices of each ticker.

# Generate Features

The features I use in this repo are listed below:

* pct_lag1 (1 day pct pricelag)
* pct_lag2
* pct_lag4
* pct_lag8
* slope3 (normalized 3 day price moving avg slope)
* slope4
* slope5
* slope6
* slope7
* slope8
* slope9
* dow (integer day of week)
* moy (integer month of year)

Counting them up, we see that this repo has 13 features.

The script which generates the above features from the CSV files is genf.bash which wraps genf.py

The script genf.bash is listed below

```bash
#!/bin/bash

# genf.bash

# This script should generate features from dates and prices.

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd ${SCRIPTPATH}/../

. env.bash
$PYTHON py/genf.py

exit
```

I ran the above script on my laptop and it finished after 5 minutes.
I used the Postgres psql command to see the features inside the features table:

```sql
ann@ub16aug:~/tkrapi20/py$ cd ..
ann@ub16aug:~/tkrapi20$ bin/psql.bash 
psql (9.5.8)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

tkrapi=# \d features
        Table "public.features"
 Column |       Type        | Modifiers 
--------+-------------------+-----------
 tkr    | character varying | 
 csv    | text              | 

tkrapi=# select count(tkr) from features;
 count 
-------
   711
(1 row)

tkrapi=# select tkr from features where tkr = '^GSPC';
  tkr  
-------
 ^GSPC
(1 row)

tkrapi=# select tkr, length(csv) from features where tkr = '^GSPC';
  tkr  | length  
-------+---------
 ^GSPC | 1840709
(1 row)

tkrapi=# select tkr, substring(csv for 256) from features where tkr = '^GSPC';
  tkr  |                                                   substring                                                    
-------+----------------------------------------------------------------------------------------------------------------
 ^GSPC | cdate,cp,pct_lead,pct_lag1,pct_lag2,pct_lag4,pct_lag8,slope3,slope4,slope5,slope6,slope7,slope8,slope9,dow,moy+
       | 1950-01-03,16.660,1.140,0.000,0.000,0.000,0.000,,,,,,,,0.020,0.010                                            +
       | 1950-01-04,16.850,0.475,1.140,0.000,0.000,0.000,,,,,,,,0.030,0.010                                            +
       | 1950-01-05,
(1 row)

tkrapi=# \q
ann@ub16aug:~/tkrapi20$
ann@ub16aug:~/tkrapi20$
ann@ub16aug:~/tkrapi20$
```

# Learn, Predict

After the features are ready, I can learn from them.

I use the script below to create models and save them to the db:

bin/cr_models.bash

Note that the above script depends on a table which I need to create beforehand:

sql/cr_mlmodels.sql

After I run bin/cr_models.bash, I can query information about the models with SQL:

qry_mlmodels.sql

If you have questions, e-me: bikle101 at gmail
