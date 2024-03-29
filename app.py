#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_wtf.csrf import CSRFProtect
from forms import *
from flask_migrate import Migrate
from datetime import datetime
from models import app, db, Venue, Artist, Show

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

moment = Moment(app)
csrf = CSRFProtect(app)
csrf.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  value = value.strftime("%Y-%m-%dT%H:%M:%S")
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  venues = Venue.query.all()
  places = Venue.query.distinct(Venue.city, Venue.state).all()
  for place in places:
    data.append({
      'city': place.city,
      'state': place.state,
      'venues': [
        {
          'id': venue.id,
          'name': venue.name,
        }
        for venue in venues if
          venue.city == place.city and venue.state == place.state
      ]
    })
  return render_template('pages/venues.html',areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  searchterm = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike("%"+searchterm+"%")).all()

  response = {
    "count": len(venues),
    "data": venues
    }

  return render_template('pages/search_venues.html', results=response, search_term=searchterm)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = Venue.query.get(venue_id)

  upcoming_shows = db.session.query(Artist, Show).join(Venue).join(Artist).filter(
    Show.venue_id == venue_id,
    Show.start_time > datetime.now()
  ).all()

  past_shows = db.session.query(Artist, Show).join(Venue).join(Artist).filter(
    Show.venue_id == venue_id,
    Show.start_time < datetime.now()
  ).all()

  data.upcoming_shows = [
    {
      'artist_id': Artist.id,
      'artist_name': Artist.name,
      'artist_image_link': Artist.image_link,
      'start_time' : Show.start_time
    }
    for Artist, Show in upcoming_shows
  ]

  data.upcoming_shows_count = len(upcoming_shows)

  data.past_shows = [
    {
      'artist_id': Artist.id,
      'artist_name': Artist.name,
      'artist_image_link': Artist.image_link,
      'start_time' : Show.start_time
    }
    for Artist, Show in past_shows
  ]

  data.past_shows_count = len(past_shows)

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    newvenue = Venue()
    form = VenueForm(request.form)
    form.populate_obj(newvenue)
    db.session.add(newvenue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
  try:
    deletethis = Venue.query.get(venue_id)
    db.session.delete(deletethis)
    db.session.commit()
    flash('Venue was successfully deleted!')
  except:
    db.session.rollback()
    flash('An error occurred: Venue could not deleted.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  searchterm = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike("%"+searchterm+"%")).all()

  response = {
    "count": len(artists),
    "data": artists
    }

  return render_template('pages/search_artists.html', results=response, search_term=searchterm)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = Artist.query.get(artist_id)

  upcoming_shows = db.session.query(Venue, Show).join(Artist).join(Venue).filter(
    Show.artist_id == artist_id,
    Show.start_time > datetime.now()
  ).all()

  past_shows = db.session.query(Venue, Show).join(Artist).join(Venue).filter(
    Show.artist_id == artist_id,
    Show.start_time < datetime.now()
  ).all()

  data.upcoming_shows_count = len(upcoming_shows)

  data.upcoming_shows = [
    {
      'venue_id': Venue.id,
      'venue_name': Venue.name,
      'venue_image_link': Venue.image_link,
      'start_time': Show.start_time
    }
    for Venue, Show in upcoming_shows
  ]

  data.past_shows_count = len(past_shows)

  data.past_shows = [
    {
      'venue_id': Venue.id,
      'venue_name': Venue.name,
      'venue_image_link': Venue.image_link,
      'start_time': Show.start_time
    }
    for Venue, Show in past_shows
  ]

  data.past_shows_count = len(past_shows)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  data = Artist.query.get(artist_id)
  form = ArtistForm(obj=data)
  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)
  try:
    data = Artist.query.get(artist_id)
    form.populate_obj(data)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully edited!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be edited.')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  data = Venue.query.get(venue_id)
  form = VenueForm(obj=data)
  return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(request.form)
  try:
    data = Venue.query.get(venue_id)
    form.populate_obj(data)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully edited!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be edited.')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    newartist = Artist()
    form = ArtistForm(request.form)
    form.populate_obj(newartist)
    db.session.add(newartist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

  return render_template('pages/home.html')

@app.route('/artists/<artist_id>/delete', methods=['POST'])
def delete_artist(artist_id):
  try:
    deletethis = Artist.query.get(artist_id)
    db.session.delete(deletethis)
    db.session.commit()
    flash('Artist was successfully deleted!')
  except:
    db.session.rollback()
    flash('An error occurred: Artist could not deleted.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Show.query.filter(Show.start_time > datetime.now()).all()
  for ashow in shows:
    avenue = Venue.query.get(ashow.venue_id)
    ashow.venue_name = avenue.name
    aartist = Artist.query.get(ashow.artist_id)
    ashow.artist_name = aartist.name
    ashow.artist_image_link = aartist.image_link
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  newshow = Show()
  newshow.artist_id = request.form['artist_id']
  newshow.venue_id = request.form['venue_id']
  newshow.start_time = request.form['start_time']

  try:
    db.session.add(newshow)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('An error has occured.  Show could not be listed')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
