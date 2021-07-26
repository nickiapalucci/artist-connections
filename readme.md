# Fyyur
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Setup guide for single machine deployment with Ubuntu 20.04 LTS

### 1. Download the repository
```
git clone https://github.com/nickiapalucci/fyyurnniapalucci.git
```
### 2. Prepare the local environment
Download and install the latest versions of these dependencies using `pip3`:
```
pip3 install SQLAlchemy
pip3 install postgres
pip3 install Flask
pip3 install Flask-Migrate
```
Install the remaining dependencies using pip3 and `requirements.txt`
```
pip3 install -r requirements.txt
```
### 3. Prepare the database
Launch a local postgresql server if you do not already have one
```
apt-get install postgresql-12
```
Connect to the postgres server with psql
```
sudo -u postgres psql
```
Create a new database named `fyyur` and a password
```sql
ALTER USER postgres PASSWORD ‘YourPassword’;

CREATE DATABASE fyyur;
```

### 4. Create a local configuration file
In the same root directory as app.py, create a new file named `config.py` with the following code
<BR>
Add your postgres password
```python
import os

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:YourPassword@localhost:5432/fyyur'
SECRET_KEY = os.urandom(32)
```
### 5. Create the schema for this database
Use flask migrate with the migrations script in this repository
```
flask db upgrade
```
## Launch the website

### 1. Launch flask with `app.py`
```
FLASK_APP=app.py flask run
```
### 2. Open the website in a local browser
```http
localhost:5000
```

## Testing
### 1. In the same root directory as app.py, run the fill_database function in `testing.py`
To create (1) new Venue, Artist, and a Show
```
python3 -c 'import testing; testing.fill_database()'
```
To create multiple new records, add an int to the function
```
python3 -c 'import testing; testing.fill_database(5)'
```

## Tech Stack (Dependencies)

### 1. Backend Dependencies
The tech stack includes the following:
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations