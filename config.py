import os

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:YourPassword@localhost:5432/fyyur'
SECRET_KEY = os.urandom(32)