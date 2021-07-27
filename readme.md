# **Fyyur**
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

# Setup guide for single machine deployment with Ubuntu 20.04 LTS

## 1. Download the repository

##### bash
```
git clone https://github.com/nickiapalucci/fyyurnniapalucci.git
```

## 2. Prepare the local environment

Download and install the latest versions of these dependencies using pip3:

##### bash
```
pip3 install SQLAlchemy
pip3 install postgres
pip3 install Flask
pip3 install Flask-Migrate
```

Install the remaining dependencies using pip3 and `requirements.txt`

##### bash
```
pip3 install -r requirements.txt
```

## 3. Prepare the database

Launch a local postgresql server if you do not already have one

##### bash
```
apt-get install postgresql-12
```

Launch the psql shell as user `postgres` which has no password by default

##### bash
```
sudo -u postgres psql
```

Create a password for `postgres` and create a new database named `fyyur` which will inherit the new password.  Exit the psql shell when finished.

##### psql
```
ALTER USER postgres PASSWORD ‘YourPassword’;

CREATE DATABASE fyyur;

exit
```

## 4. Create a local configuration file

In the same root directory as app.py, open a text editor and create a new file named `config.py` with the following code and the new password

##### config.py
```
import os

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:YourPassword@localhost:5432/fyyur'
SECRET_KEY = os.urandom(32)
```

## 5. Create the schema for the fyyur database

Use flask migrate with the included the migration script in this repository

##### bash
```
flask db upgrade
```

# Launch the website

## 1. Launch flask with `app.py`

##### bash
```
FLASK_APP=app.py flask run
```

## 2. Open the website in a local browser

##### url
```http
localhost:5000
```

# Testing

You can use the included `fill_database()` function in `Testing.py` to generate database records.

To create 1 Venue, 1 Artist, and 1 Show:

##### bash
```
python3 -c 'import testing; testing.fill_database()'
```

The default argument is 1.  To create, for example, 5 records:

##### bash
```
python3 -c 'import testing; testing.fill_database(5)'
```

# Tech Stack (Dependencies)

## Backend Dependencies
The tech stack includes the following:
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations