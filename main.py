import shutil
import sys
import api_methods
import time
import datetime
import artist
from time import sleep


class Main:

    def __init__(self):
        self.entered_name = None

    def initial_input(self) -> None:

        
        cols, rows = shutil.get_terminal_size()
        print('\n')
       
        
        # Input from user
        print(u'Artist Averag Word Count!')
        print("\n")
        print('Please Enter Artist Name:')
        self.entered_name = input()

    def another_artist_input(self) -> artist.Artist or None:

        sleep(0.5)
        print('Would you like to enter another Artists name (Y/N)?')
        while True:
            another_artist_bool = input()
            if another_artist_bool not in ['Y', 'N', 'y', 'n']:
                print('Please enter Y or N')
                continue
            else:
                print('\n')
                break
        if another_artist_bool in ['N', 'n']:
            sys.exit()
        else:
            sleep(0.5)
            print('Please enter another Artists name:')
            self.entered_name = input()

# First search for the artist using the Genius API
    def artist_selection(self) -> artist.Artist or None:
        artist_obj = api_methods.find_artist_genius(self.entered_name)

        if artist_obj:
            print(f"You have chosen {artist_obj.full_name}, is this correct? ")
            while True:
                correct_input = input()
                if correct_input not in ['Y', 'N', 'y', 'n']:
                    print('Please enter Y or N')
                    continue
                else:
                    print('\n')
                    break

            validated_artist = artist_obj
            if correct_input in ['N', 'n']:
                print("The artist wasn't found, please try again")
                validated_artist = None
            return validated_artist

    @staticmethod
    def get_songs_and_lyrics(artist_obj) -> float:

        song_start_time = time.time()
        print(f'Finding songs for {artist_obj.full_name}')
      
        api_methods.find_artist_songs_genius(artist_obj)

        print(f"{len(artist_obj.songs)} songs found for {artist_obj.full_name}")
        song_end_time = time.time()
        song_time_taken = round((song_end_time - song_start_time), 2)
      
        lyric_approx_time = datetime.timedelta(seconds=int(song_time_taken * 1.5))
        print(f'Collecting Lyrics will take approx {lyric_approx_time}')
        lyric_start_time = time.time()
        
        print('Collecting lyrics...\n')
        api_methods.find_lyrics_for_songs(artist_obj)
        lyric_end_time = time.time()
        
        lyric_time_taken = round((lyric_end_time-lyric_start_time), 2)
        return lyric_time_taken + song_time_taken

    def run(self) -> None:
        artist_obj = None
        self.initial_input()
        while not artist_obj:
            artist_obj = self.artist_selection()
            if artist_obj:
                time_taken = self.get_songs_and_lyrics(artist_obj)
                print(f'It took {datetime.timedelta(seconds=int(time_taken))}'
                      f' seconds to process your request.')
               
                # Enter another Artist
                self.another_artist_input()
                artist_obj = None
            else:
                self.another_artist_input()


if __name__ == "__main__":
    Main().run()
