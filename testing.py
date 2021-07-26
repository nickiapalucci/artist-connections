from app import *
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
    
    random.shuffle(unique_genres_list)
    unique_genres_list = unique_genres_list[:random.randrange(1,4)]

    return unique_genres_list

def fill_database(quantity=10):
    for x in range(quantity):
        new_venue = Venue()
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
        new_venue.image_link = "https://picsum.photos/seed/" + random_string() + "/200/300"
        db.session.add(new_venue)
        db.session.commit()
    
    for x in range(quantity):
        new_artist = Artist()
        new_artist.name = random_string()
        new_artist.genres = genres_filler()
        new_artist.city = random_string()
        new_artist.state = "TX"
        new_artist.phone = 972-123-4567
        new_artist.website = "https://www.udacity.com"
        new_artist.facebook_link = "https://www.facebook.com/Udacity/"
        new_artist.seeking_venue = bool(random.getrandbits(1))
        new_artist.seeking_description = random_string(20)
        new_artist.image_link = "https://picsum.photos/seed/" + random_string() + "/200/300"
        db.session.add(new_artist)
        db.session.commit()
    
    for x in range(int(quantity / 2)):
        newshow = Show()
        venue_id_list = [i[0] for i in db.session.query(Venue.id).all()]
        artist_id_list = [i[0] for i in db.session.query(Artist.id).all()]

        newshow.venue_id = random.choice(venue_id_list)
        newshow.artist_id = random.choice(artist_id_list)
        newshow.start_time = datetime.now() + timedelta(days=random.randrange(3))

        db.session.add(newshow)
        db.session.commit()