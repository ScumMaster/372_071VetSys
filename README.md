# VetSys
A veterinary database system.

## Developer Environment

Our web application runs on a Python Flask backend. To be able to build your own developer environment in order for the website to run and tested, follow the instructions.

Install flask and ensure the framework is up-to-date with Python3.

```
~$ pip install flask
~$ sudo apt install python3-flask
```

In the project directory, activate the virtual environment.

```
~$ source venv/bin/activate
```

Export the app.

```
(venv) ~$ export FLASK_APP=flask_master.py
```

Run it.

```
(venv) ~$ flask run
```

If everything is ok, website should be appear on your http://localhost:5000/
