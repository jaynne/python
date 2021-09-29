import requests
import base64
from urllib.parse import quote
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from secrets import client_id, client_secret, playlist_id, user_code, redirect_uri

class Connect():
    def __init__(self):
        self.client_id = client_id
        self.playlist = playlist_id
        self.code = user_code
        self.user_token = ""

    def getTokens(self):
        # Encode ids for authorization header
        IDs = "{}:{}".format(client_id,client_secret)
        IDs_bytes = IDs.encode('ascii')
        base64_IDs = base64.b64encode(IDs_bytes)
        encoded_ids = base64_IDs.decode('ascii')
        base_64 = encoded_ids

        # Make a POST request with code previously generated, get user token
        endpoint = "https://accounts.spotify.com/api/token"
        parameters = {'grant_type':'authorization_code', 'code': user_code, 'redirect_uri': redirect_uri}
        response = requests.post(endpoint, 
                data=parameters,
                headers={"Authorization": "Basic {}".format(base_64)})
        JSONresponse = response.json()

        self.user_token = JSONresponse['access_token']
       

    def readSongs(self):
        # Read songs from a playlist
        endpoint = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
        response = requests.get(endpoint,
            headers={"Authorization": "Bearer {}".format(self.user_token)}
        )
        self.playlist = response.json()

        # Put each song information into a list of dicts
        song_list = []
        id_list = []
        song_info = {}

        for song in self.playlist['items']:
            song_name = song['track']['name']
            song_id = song['track']['id']
            id_list.append(song_id)
            song_info[song_id] = song_name
            song_list.append(song_info)

        # Read each song's audio features (max 100 songs)
        queryList = quote(",".join(id_list))
        endpoint = "https://api.spotify.com/v1/audio-features?ids={}".format(queryList)
        response = requests.get(endpoint,
                headers={"Authorization": "Bearer {}".format(self.user_token)
                })

        # Pair each song with its features 
        songFeatures = response.json()
        for song in songFeatures['audio_features']:
            id = song['id']
            name = song_info[id]
            song.update({
                'track_name': name
            })

        # Append to panda's dataframe
        df = pd.DataFrame(songFeatures['audio_features'])
        plt.figure(figsize=(10,10))

        # Create scatterplot
        ax = sns.scatterplot(data=df, x='danceability', y='tempo', hue='track_name', palette='rainbow', size='duration_ms', sizes=(50,1000), alpha=0.7)
        h,labs = ax.get_legend_handles_labels()
        ax.legend(h[1:10], labs[1:10], loc='best', title=None)
        plt.show()

user = Connect()
user.getTokens()
user.readSongs()
