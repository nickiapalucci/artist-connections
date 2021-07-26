from . import app
from app import Venue, Artist, Show
import random, string
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime, timedelta

testapp = Flask(__name__)
testapp.config.from_object('config')
db = SQLAlchemy(testapp)

def random_string(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def genres_filler():
    unique_genres_list = [
            "Alternative",
            "Blues",
            "Classical",
            "Country",
            "Electronic",
            "Folk",
            "Funk",
            "Hip-Hop",
            "Heavy Metal",
            "Instrumental",
            "Jazz",
            "Musical Theatre",
            "Pop",
            "Punk",
            "R&B",
            "Reggae",
            "Rock n Roll",
            "Soul",
            "Other",
        ]
    
    unique_genres_list = random.shuffle(unique_genres_list)
    unique_genres_list = unique_genres_list[:random.randrange(1,4)]

    return unique_genres_list

def fill_database(quantity=10):
    new_venue = app.Venue()
    new_artist = app.Artist()
    newshow = app.Show()
    
    for x in range(quantity):
        new_venue.name = random_string()
        new_venue.genres = genres_filler()
        new_venue.address = random_string()
        new_venue.city = random_string()
        new_venue.state = "TX"
        new_venue.phone = 972-123-4567
        new_venue.website = "https://www.udacity.com"
        new_venue.facebook_link = "https://www.facebook.com/Udacity/"
        new_venue.seeking_talent = bool(random.getrandbits(1))
        new_venue.seeking_description = random_string(20)
        new_venue.image_link = "https://picsum.photos/seed/" + random_string() + "/picsum/200/300"
        db.session.add(new_venue)
        db.session.commit()
    
    for x in range(quantity):
        new_artist.name = random_string()
        new_artist.genres = genres_filler()
        new_artist.city = random_string()
        new_artist.state = "TX"
        new_artist.phone = 972-123-4567
        new_artist.website = "https://www.udacity.com"
        new_artist.facebook_link = "https://www.facebook.com/Udacity/"
        new_artist.seeking_venue = bool(random.getrandbits(1))
        new_artist.seeking_description = random_string(20)
        new_artist.image_link = "https://picsum.photos/seed/" + random_string() + "/picsum/200/300"
        db.session.add(new_artist)
        db.session.commit()
    
    for x in range(quantity / 4):
        newshow.venue_id = random.randrange(quantity - 1)
        newshow.artist_id = random.randrange(quantity - 1)
        newshow.start_time = datetime.now() + timedelta(days=random.randrange(3))
        db.session.add(newshow)
        db.session.commit()