from bs4 import BeautifulSoup
import re
import lyricsgenius
import requests
from pathlib import Path
import pandas as pd

def clean_up(song_title):

    if "Ft" in song_title:
        before_ft_pattern = re.compile(r".*(?=\(Ft)")
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
    client_access_token = 'xTU8eX1Tw9-dBnXKM5_glqmamxXzGgpM4WPFMTFamelJOJkjPT8UJBQbFPUpwF3p'
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
            
            clean_download_lyrics(f"{custom_filename}.txt")
            
        
        else:
            print('No lyrics')
            
            
    # Downloaded lyrics contain extraneous first lines and characters in the final lines.
def clean_download_lyrics(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Remove the first line
    lines = lines[1:]
    # Remove the last 8 characters matching the pattern 2 digits followed by 6 characters
    if lines:
        last_line = lines[-1]
        last_line = last_line[:-7]
        lines[-1] = last_line
    
    with open(file_path, 'w') as file:
        file.writelines(lines)
            
# clean_download_lyrics("Taylor-Swift_Taylor-Swift/Teardrops-On-My-Guitar.txt")
# Exampled
# download_album_lyrics("Taylor Swift", "Taylor Swift")
# download_album_lyrics("Taylor Swift", "Fearless")
# download_album_lyrics("Taylor Swift", "Speak Now")
# download_album_lyrics("Taylor Swift", "Red")
# download_album_lyrics("Taylor Swift", "1989")
# download_album_lyrics("Taylor Swift", "Reputation")
# download_album_lyrics("Taylor Swift", "Lover")
# download_album_lyrics("Taylor Swift", "folklore")
download_album_lyrics("Taylor Swift", "evermore")
download_album_lyrics("Taylor Swift", "Midnights")