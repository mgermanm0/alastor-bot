import pafy
import vlc
import time
import threading
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import youtube_dl

# No hace falta generar una nueva
DEVELOPER_KEY = 'AIzaSyAQc7OKxUDZIX01RsA4gAU3r4WTPOphSkQ'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

class AlastorPlayer:
    def __init__(self) -> None:
        self.t = None
        self.skip = False
        self.queue = []
        self.playing = False
        instance = vlc.Instance()
        self.player = instance.media_player_new()
        pass
    
    def ytsearch(self, query, max_res=3):
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

        # Realizar consulta
        search_response = youtube.search().list(q=query, part='id,snippet', maxResults=max_res).execute()

        # Obtener resultados
        videos = []
        playlists = []
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                videos.append('%s' % (search_result['id']['videoId']))
            elif search_result['id']['kind'] == 'youtube#playlist':
                playlists.append('%s' % (search_result['id']['playlistId']))

        if videos:
            print('Videos:{0}'.format(videos))
        elif playlists:
            print('Playlists:{0}'.format(playlists))
        
        return [self.pafy_video(x) for x in videos]

# Buscar y reproducir en YT
def youtube_search_play(self, query, max_res=3):
    res = self.ytsearch(query, max_res)
    # Si hay video, reproducirlo. Simular una pausa y esperar hasta el final.
    self.play(res[0])