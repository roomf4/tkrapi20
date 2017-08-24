# README.md

This repo, tkrapi20, should contain demos for a Meetup:

2017-08-24

Stock Market ML API with Flask-RESTful AND Keras-Tensor-Flow

https://www.meetup.com/BAyPIGgies/events/239118816/

https://www.meetup.com/Palo-Alto-Data-Science-Association/events/242451739/

The software in this repo was developed on Ubuntu 16.

If you want to run the demos on your laptop, you should install Ubuntu 16 on your laptop.

If you are on Mac or windows, a straightforward way to do this is to install VirtualBox.

After you install VirtualBox, download the file listed below and then import it into VirtualBox.

https://drive.google.com/file/d/0Bx3iDDAtxxI4VUtZcTRxTnZKZlk/

It is a large 10GB file.

After you import the above file, you should use the green-arrow in the VirtualBox GUI to boot Ubuntu 16.

After you boot Ubuntu 16, you should see a login screen for an account named: 'ann'.

The password is: 'a'

After I did the above steps, I logged in as 'ann' with password 'a'.

Next, I cloned this repo using a simple shell command:

```bash
cd ~ann
git clone https://github.com/danbikle/tkrapi20
```

I ran the first demo by issuing some shell commands:

```bash
cd ~ann
cd tkrapi20
. env.bash
python
```

I saw in the Python banner that I was running this:

```bash
ann@ub16aug:~/tkrapi20$ python
Python 3.6.1 |Anaconda 4.4.0 (64-bit)| (default, May 11 2017, 13:09:58) 
[GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> quit()
ann@ub16aug:~/tkrapi20$
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

Then, I checked that the above packages were installed with shell commands:

```bash
conda list flask
conda list keras
conda list numpy
conda list pandas
conda list psycopg2
conda list sqlalchemy
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

I typed exit at the shell prompt to exit the postgres Linux account and return to the ann account:

```bash
exit
```

In the py folder of this repo, I wrote some demos of packages:

* SQLAlchemy
* Keras
* FlaskRESTful

The shell commands for the first demo are listed below:

```bash
cd ~/tkrapi20/py
. ../env.bash
~/anaconda3/bin/python demosql.py
```

The above demo worked well so I stepped through the script with the pdb-debugger:

```bash
~/anaconda3/bin/python -m pdb demosql.py
```

The above demo worked well so I pointed demosql.py at a Postgres database on Heroku:

```bash
cd ~/tkrapi20/py
heroku create myapp2017abc
heroku addons:create heroku-postgresql:hobby-dev
heroku config
export PGURL='postgres://afizipm:33abc8@ec2-23-13-220-251.compute-1.amazonaws.com:5432/ddrpugf'
~/anaconda3/bin/python demosql.py
heroku pg:psql
select * from dropme;
```

The above demo worked well so I ran some shell commands to start the Keras demo:

```bash
cd ~/tkrapi20/py
. ../env.bash
~/anaconda3/bin/python demokeras.py
```

The above demo worked well so I stepped through the script with the pdb-debugger:

```bash
~/anaconda3/bin/python -m pdb demokeras.py
```

The above demo worked well so I ran some shell commands to start the FlaskRESTful demo:

```bash
cd ~/tkrapi20/py
. ../env.bash
export PORT=5050
export FLASK_DEBUG=1
~/anaconda3/bin/python demoflask_restful.py
```

The above shell became locked. I call it Shell-1.

I started another shell, called Shell-2, and issued curl commands:

```bash
curl                            localhost:5050/hello.json
curl -d 'msg2flask=hello-flask' localhost:5050/hello.json
```

I saw this:

```bash

```
