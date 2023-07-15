import spotipy
from flask import Flask, request, url_for, session, redirect
from spotipy.oauth2 import SpotifyOAuth
import time
import pandas as pd

app = Flask(__name__)
app.secret_key = "this will be changed later"
app.config['SESSION_COOKIE_NAME'] = 'Anths cookie'


@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for('getTracks', _external = True))

@app.route('/getTracks')
def getTracks():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/') #will return users to the home page if their account is not authorized
    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    all_songs = []
    it =0
    while True:
        items = sp.current_user_saved_tracks(limit =50, offset =it*50)['items']
        it +=1
        all_songs+= items
        for ind, item in enumerate(items):
            track = item['track']
            val = track['name'] + " - " + track['artists'][0]['name']
            all_songs+= [val]
        if (len(items) <50):
            break
    df = pd.DataFrame(all_songs, columns =['Song Names'])
    df.to_csv('songs.csv',index=False)
    return "done"

def get_token():
    token_valid = False
    token_info = session.get("token_info",{})
    if not (session.get('token_info',False)):
        token_valid = False
        return token_info, token_valid
    now = int(time.time)

    is_expired = token_info('expires_at') - now <60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    token_valid = True
    return token_info,token_valid



