from flask import Flask, request, url_for, session, redirect, send_file
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('secret_key')
app.config['SESSION_COOKIE_NAME'] = 'Ugonna Cookie'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect("getTracks")

@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        return redirect("/")
    sp = spotipy.Spotify(auth=token_info['access_token'])
    artists, aid = get_top_artists(sp)
    tracks, tid = get_top_songs(sp)
    genres, recg = get_top_genres(aid, sp)
    recommendations = get_recommended_songs(recg, tid, sp)
    items = {"artists": artists, "tracks": tracks, "genres": genres, "rtoken": token_info['refresh_token'], "atoken": token_info['access_token'], "recommendations": recommendations}
    jsonFile = open("data.json","w")
    jsonFile.write(json.dumps(items, indent = 4))
    jsonFile.close()
    return send_file("./data.json",as_attachment=True)
    


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    expired = token_info['expires_at'] - now < 60
    if (expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = os.getenv('client_id'),
        client_secret = os.getenv('client_secret'),
        redirect_uri= url_for('redirectPage', _external=True),
        scope = "user-read-playback-state, playlist-modify-private, user-library-read, user-top-read, user-read-private")


def get_recommended_songs(recg, tid, sp):
    """takes list of recommended genres, list of track ids, and a spotipy.Spotify() class and returns list of recommended songs"""
    me = sp.current_user()
    country = me['country']
    l = sp.recommendations(seed_genres = recg, seed_tracks = tid, country = country, limit = 5)
    songs = []
    for i in l['tracks']:
        songs.append(i['name'] + "\n By " + i['artists'][0]['name'])
    return songs



def get_top_songs(sp):
    """
    take Spotify() class and find top songs and their ids
    """
    names = []
    ids = []
    stop = 0
    for i in range(5):
        tracks = sp.current_user_top_tracks(limit = 20, offset = 20*i)
        size = len(tracks['items'])
        for j in range(size):
            if stop < 5:
                names.append(tracks['items'][j]['name'] + '\n By ' + tracks['items'][j]['artists'][0]['name'])
            else:
                break
            if stop < 3:
                ids.append(tracks['items'][j]['id'])
            stop += 1
    return names, ids

def get_top_artists(sp):
    """
    take Spotify() class and return list of top artists and artist ids
    """
    names = []
    ids = []
    stop = 0
    for i in range(5):
        artists = sp.current_user_top_artists(offset = i*20)
        for j in range(len(artists['items'])):
            if stop < 5:
                names.append(artists["items"][j]['name'])
            ids.append(artists["items"][j]['id'])
            stop += 1
    return names, ids

def get_top_genres(aid, sp):
    """
    take artist ids, track ids, and Spotify() class to return most popular genres in a list and genres I can use to recommend tracks
    """
    genres = {}
    size = len(aid)
    artists = []
    offset = 0
    topg = []
    rec = []
    recl = 0
    use = sp.recommendation_genre_seeds()

    while size>offset*50:
        artists.append(sp.artists(aid[50*offset:50*(offset+1):1]))
        offset += 1
    for j in range(len(artists)):
        g = artists[j]['artists']
        for k in g:
            l = k['genres']
            for m in l:
                if m not in genres.keys():
                    genres[m] = 0
                genres[m] += 1
    
    for _ in range(5):
        best = max(genres, key = genres.get)
        topg.append(best)
        del genres[best]
        if best in use['genres'] and recl < 2:
            rec.append(best)
            recl += 1
    
    while recl < 2 and len(genres) != 0:
        best = max(genres, key = genres.get)
        del genres[best]
        if best in use['genres'] and recl < 2:
            rec.append(best)
            recl += 1
    
    return topg, rec

