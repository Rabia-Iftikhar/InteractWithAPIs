
import song
import numpy as np

class Artist(object):
    
    def __init__(self, genius_id, full_name, songs=None, mean_wordcount=0) -> None:
        self.genius_id = genius_id
        self.full_name = full_name
        self.songs = []
        self.mean_wordcount = 0

    def assign_songs(self, artists_songs: dict) -> None:
        songs_objects = [song.Song(title=artist_song['title']) for artist_song in artists_songs]
        self.songs.extend(songs_objects)

    def calc_mean_wordcount(self) -> None:
        found_word_counts = [found_song.word_count for found_song in self.songs if found_song.lyrics_found]
      
        if len(found_word_counts) > 0:
            mean = int(np.mean(found_word_counts))
            self.mean_wordcount = mean
            print(f"The average word count for {self.full_name} is {self.mean_wordcount}.\n")
        else:
            print(f"No lyrics found for {self.full_name}.")
