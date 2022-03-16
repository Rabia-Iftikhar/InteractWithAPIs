# InteractWithAPIs

 The program will produce the average(mean) number of words in their songs, when given the name of an artist.

## Instructions
- Written in Python 3.10
- To install all dependancies, run `py -m pip install -r config/requirements.txt`.
- To start the application, run `py main.py` from the command line.

## Structure
- This app makes three sets of API calls, the first two to Genius through RapidAPI to search for the artist and then find the lists of songs for that artist, and the third API call to Lyrics.ovh to get the lyrics for that song. The data taken in as a dict and parsed from there.

- User Interface
  - I decided the keep the user interface relatively simple. The user can continuously search for artists unitl they have satisfied their need.

  
