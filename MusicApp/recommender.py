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
                     language='rus')

song_cluster_pipeline = load('blobs/song_cluster')
data = pd.read_csv("blobs/data.csv")


def find_song(name, year):
    song_data = defaultdict()
    results = sp.search(q='track: {} year: {}'.format(name, year), limit=1)
    if not results['tracks']['items']:
        return None

    results = results['tracks']['items'][0]
    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]

    song_data['name'] = [name]
    song_data['year'] = [year]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]

    for key, value in audio_features.items():
        song_data[key] = value

    return pd.DataFrame(song_data)


number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
               'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']


def get_song_data(song, spotify_data):
    try:
        song_data = spotify_data[(spotify_data['name'] == song['name'])
                                 & (spotify_data['year'] == song['year'])].iloc[0]
        return song_data

    except IndexError:
        return find_song(song['name'], song['year'])


def find_song_by_id(spotify_id):
    song_data = defaultdict()
    results = sp.track(spotify_id)
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


def get_song_data_by_id(spotify_id, spotify_data):
    try:
        song_data = spotify_data[(spotify_data['id'] == spotify_id)].iloc[0]
        return song_data

    except IndexError:
        return find_song_by_id(spotify_id)


def get_mean_vector(song_list, spotify_data):
    song_vectors = []

    for song in song_list:
        song_data = get_song_data(song, spotify_data)
        if song_data is None:
            print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
            continue
        song_vector = song_data[number_cols].values
        song_vectors.append(song_vector)

    song_matrix = np.array(list(song_vectors))
    return np.mean(song_matrix, axis=0)


def flatten_dict_list(dict_list):
    flattened_dict = defaultdict()
    for key in dict_list[0].keys():
        flattened_dict[key] = []

    for dictionary in dict_list:
        for key, value in dictionary.items():
            flattened_dict[key].append(value)

    return flattened_dict


def recommend_songs(song_list, spotify_data, n_songs=10):
    metadata_cols = ['name', 'year', 'artists']
    song_dict = flatten_dict_list(song_list)

    song_center = get_mean_vector(song_list, spotify_data)
    scaler = song_cluster_pipeline.steps[0][1]
    scaled_data = scaler.transform(spotify_data[number_cols])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))
    distances = cdist(scaled_song_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:, :n_songs][0])

    rec_songs = spotify_data.iloc[index]
    rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
    return rec_songs[metadata_cols].to_dict(orient='records')


def search_songs(song):
    return sp.search(q='track: {}'.format(song), limit=20)


def get_songs(songs):
    result = []
    for song in songs:
        result.append(sp.track(song))
    return result


if __name__ == '__main__':
    recommendation = recommend_songs([
        {
            'name': "We Don't Talk Anymore (feat. Selena Gomez)",
            'year': 2016
        }, {
            "name": "Scared to Be Lonely",
            "year": 2017
        },
        {
            "name": "In My Feelings",
            "year": 2018
        }
    ], data, n_songs=20)
    print(json.dumps(recommendation, indent=4))
