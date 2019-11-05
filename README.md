# VetSys
A veterinary database system.

## Developer Environment

Our web application runs on a Python Flask backend. To be able to build your own developer environment in order for the website to run and tested, follow the instructions.

Install flask and ensure the framework is up-to-date with Python3.

```
~$ pip install flask
~$ sudo apt install python3-flask
```

Clone and go to the project directory.

```
~$ git clone https://github.com/uyazar/372_071VetSys.git
~$ cd 372_071VetSys
```

Activate the virtual environment.

```
~$ source 372/bin/activate
```

Export the app.

```
(372) ~$ export FLASK_APP=run.py
```

Run it.

```
(372) ~$ flask run
```

If everything is ok, website should be appear on your http://localhost:5000/


Dependencies:
-flask
-flask_admin
-flask_login
-flask_sqlalchemy
-flask_bcrypt



