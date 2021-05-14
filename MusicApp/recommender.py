import json
import os
import warnings
from collections import defaultdict

import numpy as np
import pandas as pd
import spotipy
from dotenv import load_dotenv
from joblib import load
from scipy.spatial.distance import cdist
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

warnings.filterwarnings("ignore")
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ["SPOTIFY_CLIENT_ID"],
                                                           client_secret=os.environ["SPOTIFY_CLIENT_SECRET"]),
                     language='RU')
market = 'RU'

song_cluster_pipeline = load('blobs/song_cluster')
data = pd.read_csv("blobs/data.csv")

number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
               'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']


def get_song_data_by_id(spotify_id, spotify_data):
    try:
        song_data = spotify_data[(spotify_data['id'] == spotify_id)].iloc[0]
        return song_data

    except IndexError:
        return find_song_by_id(spotify_id)


def find_song_by_id(spotify_id):
    song_data = defaultdict()
    results = sp.track(spotify_id, market=market)
    if not results:
        return None

    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]

    song_data['name'] = [results['name']]
    song_data['year'] = [int(results['album']['release_date'][:4])]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]

    for key, value in audio_features.items():
        song_data[key] = value

    return pd.DataFrame(song_data)


def get_mean_vector(song_list, spotify_data):
    song_vectors = []
    for song in song_list:
        song_data = get_song_data_by_id(song, spotify_data)
        if song_data is None:
            print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
            continue
        song_vector = song_data[number_cols].values
        song_vectors.append(song_vector)

    song_matrix = np.array(list(song_vectors))
    return np.mean(song_matrix, axis=0)


def recommend(song_list):
    return recommend_songs(song_list, data, n_songs=21)


def recommend_songs(song_list, spotify_data, n_songs=10):
    metadata_cols = ['id']
    song_center = get_mean_vector(song_list, spotify_data)
    scaler = song_cluster_pipeline.steps[0][1]
    scaled_data = scaler.transform(spotify_data[number_cols])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))
    distances = cdist(scaled_song_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:, :n_songs][0])

    rec_songs = spotify_data.iloc[index]
    rec_songs = rec_songs[~rec_songs['id'].isin(song_list)]
    recsongsdict = rec_songs[metadata_cols].to_dict(orient='records')
    return [song['id'] for song in recsongsdict]


def search_songs(song):
    return sp.search(q='track: {}'.format(song), limit=20)


def get_songs(songs):
    if len(songs) > 0:
        return sp.tracks(songs, market=market)
    else:
        return []


if __name__ == '__main__':
    song_cluster_pipeline = load('../blobs/song_cluster')
    data = pd.read_csv("../blobs/data.csv")
    recommendation = recommend_songs([
        "37FXw5QGFN7uwwsLy8uAc0",
        "3ebXMykcMXOcLeJ9xZ17XH",
        "2G7V7zsVDxg1yRsu7Ew9RJ"
    ], data, n_songs=20)
    print(json.dumps(recommendation, indent=4))
