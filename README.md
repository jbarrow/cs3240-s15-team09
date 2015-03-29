# cs3240-s15-team09 - SECUREWITNESS project
# Sprint Zero demo:
- https://github.com/nynguyen/sprint_zero_demo (files and forms)

# Installation Instructions

## Getting MySQL

SecureWitness uses MySQL as the database, so the first step is installing
and running a MySQL server. First, I suggest using XAMPP (https://www.apachefriends.org/index.html), so download and install that.

Once that's installed, start an Apache Server and a MySQL server. Then navigate
your browser to:

http://localhost/phpmyadmin

In PHPMyAdmin, create a new database "secure_witness" (sans quotes).

Then, in the root directory of secure_witness in a terminal, run:

```python manage.py syncdb```

And set up a new superuser.

Note: Every time you want to run SecureWitness, you have to have a MySQL server
running.
