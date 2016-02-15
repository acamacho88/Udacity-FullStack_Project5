Alex Camacho - 2/14/16

This is for PROJECT 5 of the Udacity Full Stack Nanodegree

I have configured the Amazon server to successfully host the Catalog
application previously designed for Project 3.

The IP address of the site is 52.24.236.0

The SSH port is 2200

The full URL of the Amazon page is
http://ec2-52-24-236-0.us-west-2.compute.amazonaws.com/

## Installations

I installed, via apt-get the following:
git
python
python-pip
apache2
postgresql python-psycopg2
python-sqlalchemy

I made sure via pip to install the following python packages:
oauth2client
requests
flask==0.9
Flask-Login==0.1.3
werkzeug==0.8.3
httplib2

## Configurations

I also made sure to disable the root user, and enable sudo by adding
the student and grader users to the sudoers.d directory (both of whose
passwords are just their names).

I blocked all incoming requests via the firewall except SSH, HTTP,
and NTP, and changed the SSH port from its default of 22 to 2200

## Outside resources

The main resource I used were the Udacity forums, mostly this
particular thread:
https://discussions.udacity.com/t/p5-how-i-got-through-it/15342

## Site Description

Users can click on artists to see existing albums, and if they are the
creator, edit, delete, and add albums to that artist's page.  Users
can also add artists to the site.

On a particular artist's page, the albums are ordered chronologically.
