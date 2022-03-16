
class Song:
  

    def __init__(self, title, lyrics=None, lyrics_found=False, word_count=0) -> None:
        self.title = title
        self.lyrics = None
        self.lyrics_found = False
        self.word_count = 0

    def assign_lyrics_and_wordcount(self, lyrics: str) -> None:
        self.lyrics = lyrics
        self.lyrics_found = True
     
        word_count = len(lyrics.split())
        self.word_count = word_count
