import requests

class SpotifyAPI:
    def __init__(self, base_url,client_id,client_secret,access_token=None,):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token or self.get_access_token()
        
    def get_access_token(self):
        auth_url = 'https://accounts.spotify.com/api/token'
        data = {
        'grant_type': 'client_credentials',
        'client_id': self.client_id,
        'client_secret': self.client_secret  ,
            }
        auth_response = requests.post(auth_url, data=data)
        print(auth_response.json())
        return auth_response.json()['access_token']


    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}'
        }

    def get_track_features(self, track_id):
        url = f'{self.base_url}/audio-features/{track_id}'
        response = requests.get(url, headers=self.get_headers())
        print(response.json())
        return response.json()

    def get_track_analysis(self, track_id):
        url = f'{self.base_url}/audio-analysis/{track_id}'
        response = requests.get(url, headers=self.get_headers())
        print(response.json())
        return response.json()
    
    def get_albums(self, artist_id):
        url = f'{self.base_url}/artists/{artist_id}/albums'
        response = requests.get(url, headers=self.get_headers())
        print(response.json())
        return response.json()
    
    def get_tracks(self,track_id):
        url = f'{self.base_url}/albums/{track_id}/tracks'
        response = requests.get(url, headers=self.get_headers())
        print(response.json())
        return response.json()

if __name__ == '__main__':
    base_url = 'https://api.spotify.com/v1'
    spotify_api = SpotifyAPI(base_url=base_url,client_id='bfb11db6ff8345c6853009c506c16035',client_secret='2df933fe72084f7bb81d9624499931f6')
    track_id = '6y0igZArWVi6Iz0rj35c1Y'
    
    spotify_api.get_track_features(track_id)
    # spotify_api.get_track_analysis(track_id)