import youtube_dl
import os
import requests

class YTDLUtils:
    
    @staticmethod
    def search(query):
        with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
            try: 
                requests.get(query)
            except: # Ocurre un error - NO es una URL
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            else: # No ocurre ningún error - Es una URL, reproducir directamente
                info = ydl.extract_info(query, download=False)
                
        return (info, info['formats'][0]['url'])