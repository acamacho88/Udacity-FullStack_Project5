from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Artist, Album, User

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('/var/www/CatalogApp/CatalogApp/client_secrets.json','r').read())['web']['client_id']

#Connect to Database and create database session
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('/var/www/CatalogApp/CatalogApp/client_secrets.json',scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    # Verify that the access token is used for the intended use
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."),401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),200)
        response.headers['Content-Type'] = 'application/json'
        return response


    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token':credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    user_id = getUserID(login_session['email'])

    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s"%login_session['username'])
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user is not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token.
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'),200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid
        response = make_response(json.dumps('Failed to revoke token for given user'),400)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/fbconnect',methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    # Exchange client token for long-lived server-side token with GET /oauth/
    # access_token?grant_type=fb_exchange_token&client_id={app-id}
    # &client_secret={app-secret}&fb_exchange_token={short-lived-token}
    app_id = json.loads(open('/var/www/CatalogApp/CatalogApp/fb_client_secrets.json','r').read())['web']['app_id']
    app_secret = json.loads(open('/var/www/CatalogApp/CatalogApp/fb_client_secrets.json','r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id,app_secret,access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.2/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url,'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    user_id = getUserID(login_session['email'])

    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s"%login_session['username'])
    return output

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['facebook_id']
    return "you have been logged out"

@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            #gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            #fbdisconnect()
            del login_session['facebook_id']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showArtists'))
    else:
        flash("You were not logged in to begin with!")
        redirect(url_for('showArtists'))

# Create a state token to prevent request forgery.
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html')

#JSON APIs to view Artist Information
@app.route('/artist/<int:artist_id>/albums/JSON')
def artistAlbumsJSON(artist_id):
    artist = session.query(Artist).filter_by(id = artist_id).one()
    items = session.query(Album).filter_by(artist_id = artist_id).all()
    return jsonify(Albums=[i.serialize for i in items])


@app.route('/artist/<int:artist_id>/albums/<int:album_id>/JSON')
def albumJSON(artist_id, album_id):
    Album = session.query(Album).filter_by(id = album_id).one()
    return jsonify(Album = Album.serialize)

@app.route('/artist/JSON')
def artistsJSON():
    artists = session.query(Artist).all()
    return jsonify(artists= [a.serialize for a in artists])


#Show all artists
@app.route('/')
@app.route('/artist/')
def showArtists():
    artists = session.query(Artist).order_by(asc(Artist.name))
    if 'username' not in login_session:
        return render_template('publicartists.html',artists=artists)
    else:
        return render_template('artists.html', artists = artists)

#Create a new artist
@app.route('/artist/new/', methods=['GET','POST'])
def newArtist():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newArtist = Artist(name = request.form['name'],user_id = login_session['user_id'])
        session.add(newArtist)
        flash('New Artist %s Successfully Created' % newArtist.name)
        session.commit()
        return redirect(url_for('showArtists'))
    else:
        return render_template('newArtist.html')

#Edit an artist
@app.route('/artist/<int:artist_id>/edit/', methods = ['GET', 'POST'])
def editArtist(artist_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedArtist = session.query(Artist).filter_by(id = artist_id).one()
    if editedArtist.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this artist. Please create your own artist in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedArtist.name = request.form['name']
            flash('%s Successfully Edited' % editedArtist.name)
            return redirect(url_for('showArtists'))
    else:
        return render_template('editArtist.html', artist = editedArtist)


#Delete an artist
@app.route('/artist/<int:artist_id>/delete/', methods = ['GET','POST'])
def deleteArtist(artist_id):
    if 'username' not in login_session:
        return redirect('/login')
    artistToDelete = session.query(Artist).filter_by(id = artist_id).one()
    if artistToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this artist. Please create your own artist in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(artistToDelete)
        flash('%s Successfully Deleted' % artistToDelete.name)
        session.commit()
        return redirect(url_for('showArtists', artist_id = artist_id))
    else:
        return render_template('deleteArtist.html',artist = artistToDelete)

#Show an artist's albums
@app.route('/artist/<int:artist_id>/')
@app.route('/artist/<int:artist_id>/album/')
def showAlbums(artist_id):
    artist = session.query(Artist).filter_by(id = artist_id).one()
    creator = getUserInfo(artist.user_id)
    albums = session.query(Album).filter_by(artist_id = artist_id).all()
    # Camacho - Sort the list of albums by release year
    albums.sort(key=lambda x:x.year, reverse=False)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicalbums.html',albums=albums,artist=artist,creator=creator)
    else:
        return render_template('albums.html', albums = albums, artist = artist,creator=creator)
     


#Create a new album
@app.route('/artist/<int:artist_id>/album/new/',methods=['GET','POST'])
def newAlbum(artist_id):
    if 'username' not in login_session:
        return redirect('/login')
    artist = session.query(Artist).filter_by(id = artist_id).one()
    if request.method == 'POST':
        newAlbum = Album(name = request.form['name'], description = request.form['description'], year = request.form['year'], numtracks = request.form['numtracks'], cover = request.form['cover'], artist_id = artist_id, user_id=login_session['user_id'])
        session.add(newAlbum)
        session.commit()
        flash('New Album %s Successfully Created' % (newAlbum.name))
        return redirect(url_for('showAlbums', artist_id = artist_id))
    else:
        return render_template('newalbum.html', artist_id = artist_id)

#Edit an album
@app.route('/artist/<int:artist_id>/album/<int:album_id>/edit', methods=['GET','POST'])
def editAlbum(artist_id, album_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedAlbum = session.query(Album).filter_by(id = album_id).one()
    artist = session.query(Artist).filter_by(id = artist_id).one()
    if editedAlbum.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this album. Please create your own album in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedAlbum.name = request.form['name']
        if request.form['description']:
            editedAlbum.description = request.form['description']
        if request.form['year']:
            editedAlbum.year = request.form['year']
        if request.form['numtracks']:
            editedAlbum.numtracks = request.form['numtracks']
        if request.form['cover']:
            editedAlbum.cover = request.form['cover']
        session.add(editedAlbum)
        session.commit() 
        flash('Album Successfully Edited')
        return redirect(url_for('showAlbums', artist_id = artist_id))
    else:
        return render_template('editalbum.html', artist_id = artist_id, album_id = album_id, item = editedAlbum)


#Delete an album
@app.route('/artist/<int:artist_id>/album/<int:album_id>/delete', methods = ['GET','POST'])
def deleteAlbum(artist_id,album_id):
    if 'username' not in login_session:
        return redirect('/login')
    artist = session.query(Artist).filter_by(id = artist_id).one()
    albumToDelete = session.query(Album).filter_by(id = album_id).one() 
    if albumToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this album item. Please create your own album in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(albumToDelete)
        session.commit()
        flash('Album Successfully Deleted')
        return redirect(url_for('showAlbums', artist_id = artist_id))
    else:
        return render_template('deleteAlbum.html', album = albumToDelete)

def getUserID(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

def createUser(login_session):
    newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id


if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run()
