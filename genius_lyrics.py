from bs4 import BeautifulSoup
import re
import lyricsgenius
import requests
from pathlib import Path
import pandas as pd

def clean_up(song_title):

    if "Ft" in song_title:
        before_ft_pattern = re.compile(".*(?=\(Ft)")
        song_title_before_ft = before_ft_pattern.search(song_title).group(0)
        clean_song_title = song_title_before_ft.strip()
        clean_song_title = clean_song_title.replace("/", "-")
    
    else:
        song_title_no_lyrics = song_title.replace("Lyrics", "")
        clean_song_title = song_title_no_lyrics.strip()
        clean_song_title = clean_song_title.replace("/", "-")
    
    return clean_song_title

def get_all_songs_from_album(artist, album_name):
    
    artist = artist.replace(" ", "-")
    album_name = album_name.replace(" ", "-")
    
    response = requests.get(f"https://genius.com/albums/{artist}/{album_name}")
    html_string = response.text
    document = BeautifulSoup(html_string, "html.parser")
    song_title_tags = document.find_all("h3", attrs={"class": "chart_row-content-title"})
    song_titles = [song_title.text for song_title in song_title_tags]
    
    clean_songs = []
    for song_title in song_titles:
        clean_song = clean_up(song_title)
        clean_songs.append(clean_song)
        
    return clean_songs

def download_album_lyrics(artist, album_name): 
    
    # You will need to go to Genius Developers to get your own client access token
    client_access_token = 'insert_your_client_access_token_here'
    LyricsGenius = lyricsgenius.Genius(client_access_token)
    LyricsGenius.remove_section_headers = True
    
    clean_songs = get_all_songs_from_album(artist, album_name)
    
    for song in clean_songs:
        
        song_object = LyricsGenius.search_song(song, artist)
        
        if song_object != None:
            
            artist_title = artist.replace(" ", "-")
            album_title = album_name.replace(" ", "-")
            song_title = song.replace("/", "-")
            song_title = song.replace(" ", "-")
            
            custom_filename=f"{artist_title}_{album_title}/{song_title}"
            

            Path(f"{artist_title}_{album_title}").mkdir(parents=True, exist_ok=True)
            
            song_object.save_lyrics(filename=custom_filename, extension='txt', sanitize=False)
        
        else:
            print('No lyrics')