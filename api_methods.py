from concurrent.futures import ThreadPoolExecutor
import requests
import artist
import song


def make_request(url: str, params=None, headers=None) -> requests.request or None:
   
    try:
        response = requests.request("GET", url, headers=headers, params=params)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError:
        pass


def find_artist_genius(entered_name: str) -> artist.Artist or None:
  
    #Search for the artist
    base_url = "https://genius.p.rapidapi.com/search"

    params = {"q": entered_name}

    headers = {
        'x-rapidapi-host': "genius.p.rapidapi.com",
        'x-rapidapi-key': "d7ad286703msh16c7e9d16008c8dp1f165djsn0673935389b2"
        }

    response = make_request(base_url, params=params, headers=headers)

    json_data = response.json()
    try:
        artist_id = json_data['response']['hits'][0]['result']['primary_artist']['id']
        artist_name = json_data['response']['hits'][0]['result']['primary_artist']['name']
        artist_obj = artist.Artist(genius_id=artist_id, full_name=artist_name)
        return artist_obj
    except IndexError:
        print('This artist does not exist in the Genius database')
        return None


def find_artist_songs_genius(artist_obj: artist.Artist) -> None:

 
    page_number = 1

    while type(page_number) == int:
        # Songs from the artist ID
        url = f"https://genius.p.rapidapi.com/artists/{artist_obj.genius_id}/songs?"
      
        querystring = {"page": page_number,
                       "per_page": "50"}
        headers = {
            'x-rapidapi-host': "genius.p.rapidapi.com",
            'x-rapidapi-key': "d7ad286703msh16c7e9d16008c8dp1f165djsn0673935389b2"
            }

        genius_songs_response = make_request(url, headers=headers, params=querystring)
        songs = genius_songs_response.json()['response']['songs']
        artist_obj.assign_songs(songs)
        
        page_number = genius_songs_response.json()['response']['next_page']


def make_lyrics_request(url: str, song_obj: song.Song) -> None:

    lyrics_response = make_request(url)
    if lyrics_response:
        lyrics = lyrics_response.json()['lyrics']
      
        song_obj.assign_lyrics_and_wordcount(lyrics)


def find_lyrics_for_songs(artist_obj: artist.Artist) -> None:  
    threads = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for song_obj in artist_obj.songs:
          
            url = f"https://api.lyrics.ovh/v1/{artist_obj.full_name}/{song_obj.title}"
            threads.append(executor.submit(make_lyrics_request, url, song_obj))
            
    artist_obj.calc_mean_wordcount()
