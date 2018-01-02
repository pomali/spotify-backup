#!python3

import requests
import json
import os
import secret

URL = {
        'playlists': 'https://api.spotify.com/v1/me/playlists?limit=50&offset=0',
        }

HEADERS = {
        'Authorization': 'Bearer {}'.format(secret.OAUTH_TOKEN)
        }

def jprint(*x):
    for i in x:
        print(json.dumps(i))

def getPlaylists():
    def getPlaylist(url):
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(r)
            raise Error("not ok!")
        return r.json()
    out = []
    p = getPlaylist(URL['playlists'])
    out.extend(p['items'])
    while (p['next']):
        print('getting playlists {}'.format(p['next']))
        p = getPlaylist(p['next'])
        out.extend(p['items'])
    return out

def getTracks(playlists):
    try:
        os.mkdir('playlists')
    except FileExistsError:
        print('folder exists')
    for p in playlists:
        url = p['tracks']['href']
        print('getting tracks from {}'.format(p['name'], url))
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(r)
            raise Error("not ok!")
        with open('playlists/{name} [{id}].json'.format(**p), 'w') as pfile:
            pfile.write(json.dumps(r.json()))

playlists = getPlaylists()
with open('playlists.json', 'w') as pfile:
    pfile.write(json.dumps(playlists))
getTracks(playlists)


