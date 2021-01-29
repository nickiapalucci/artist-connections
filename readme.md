Fyyur
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack will include the following:
 * **git** as our repository and version control
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations

## Setup

### 1. Local environment
You can download and install the python3 dependencies mentioned above using `pip` as:
```
pip3 install SQLAlchemy
pip3 install postgres
pip3 install Flask
pip3 install Flask-Migrate
```
Install the remaining dependencies using the `requirements.txt`
```
sudo pip3 install -r requirements.txt
```
### 2. Download the repository
Once this has become a public repository, you can download it here
```
https://github.com/nickiapalucci/
```
### 3. Prepare the database
Launch a local postgresql server if you do not already have one, then create a new database named `fyyur`

### 4. Configure the app to use the datbase
Add your postgresql connection to `config.py`
```
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:xyz@localhost:5432/fyyur'
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
### 2. By default, flask listens to port 5000 locally
```
localhost:5000
```