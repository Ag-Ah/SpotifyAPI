import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import time

if sys.version_info < (3, 0):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

import io
import random
import pandas as pd
from colorthief import ColorThief
from spotipy_random import get_random

#Insertar cid y secret en base a los valores proveídos por la app en la API de Spotify
cid = 'yourcid'
secret = 'yoursecret'

#Conexión a la API y a la librería Spotipy con las credenciales correspondientes
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#Loop para extraer información pertinente a la canción y agregarla a la lista
for i in range(0,1000000):
    #Lista de géneros para la búsqueda que se va a determinar de forma aleatoria con la función get_random()
    random_genre = ["pop","rock","metal","punk","electronic","alternative","dance","folk","indie"]
    #Lista booleana para el tag_hipster de la función get_random()
    random_boolean = [True, False]
    #Se definen las listas para almacenar la información y posteriormente agregarla al dataset
    artist_name = []
    track_name = []
    popularity = []
    track_id = []
    album_name = []
    danceability = []
    key = []
    loudness = []
    mode = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []
    duration = []
    time_signature = []
    genre = []
    release_date = []
    primary_color = []
    color_palette = []
    #Se extrae la información de la canción aleatoria con la función get_random()
    random_pop_song_json: str = get_random(spotify=sp, type="track", limit= 1, tag_hipster = False, genre = random.choice(random_genre), year=random.randrange(1960,2023,1))
    #Una vez extraída la información se agrega a la lista que corresponda
    artist_name.append(random_pop_song_json['artists'][0]['name']) 
    album_name.append(random_pop_song_json['album']['name']) 
    track_name.append(random_pop_song_json['name']) 
    track_id.append(random_pop_song_json['id']) 
    popularity.append(random_pop_song_json['popularity'])
    features: str = sp.audio_features(random_pop_song_json['uri'])
    genres: str = sp.artist(random_pop_song_json['artists'][0]['external_urls']['spotify'])
    album: str = sp.album(random_pop_song_json["album"]["external_urls"]["spotify"])
    release_date.append(album["release_date"])
    genre.append(genres['genres'])
    danceability.append(features[0]['danceability'])
    key.append(features[0]['key'])
    loudness.append(features[0]['loudness'])
    mode.append(features[0]['mode'])
    speechiness.append(features[0]['speechiness'])
    acousticness.append(features[0]['acousticness'])
    instrumentalness.append(features[0]['instrumentalness'])
    liveness.append(features[0]['liveness'])
    valence.append(features[0]['valence'])
    tempo.append(features[0]['tempo'])
    duration.append(features[0]['duration_ms'])
    time_signature.append(features[0]['time_signature'])
    #Se extrae la URL de la tapa del álbum de la canción y se identifica el color primario así como la paleta entera de colores del mismo
    fd = urlopen(random_pop_song_json["album"]["images"][0]["url"])
    f = io.BytesIO(fd.read())
    color_thief = ColorThief(f)
    primary_color.append(color_thief.get_color(quality=1))
    color_palette.append(color_thief.get_palette(quality=1))
    #Se juntan las distintas listas en un solo dataframe que es exportado como CSV posteriormente
    track_dataframe = pd.DataFrame({'artist_name' : artist_name, 'album_name' : album_name, 'track_id' : track_id, 'track_name' : track_name, 'popularity' : popularity, 'danceability' : danceability, 'key' : key,'loudness' : loudness,'mode' : mode,'speechiness' : speechiness,'acousticness' : acousticness,'instrumentalness' : instrumentalness,'liveness' : liveness,'valence' : valence,'tempo' : tempo,'duration' : duration,'time_signature' : time_signature,'genre' : genre,'release_date' : release_date,'primary_color' : primary_color,'color_palette' : color_palette})
    track_dataframe.to_csv('Dataset_Spotify.csv',mode="a", header=False,index=False)