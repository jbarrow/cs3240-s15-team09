Installation Instructions

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

##Deployment Instructions
If you have an error like: MySQL “incorrect string value” error when save unicode string in Django"
go to:

Windows: C:\xampp\mysql\bin
```mysql -u root```
```ALTER TABLE secure_witness.report_form_report MODIFY COLUMN AES_key VARCHAR(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;```

and that appeared to help me to be able to submit encrypted reports and decrypt the results.

##Starting the GUI standalone app for decryption and file downloads:
run  ```python client/gui.py``` in the terminal
