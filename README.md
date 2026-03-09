# ♫ Pythonic Music Player ♫

## Description
A desktop music player app that is built purely in python.
The playlists are stored in the user's document folder for easy access.
This app allows to import .mp3 and .ogg audio files.

It uses wrapper VLC to play the audio and control.
Then mutagen is used to get the length of the audio since VLC is unrealiable on that part.

Python Mixer Music was dropped because it lacks reliable positioning and seek support.

## Features
- Create and manage playlists
- Import local music files
- Play Audio MP3 and OGG
- Playback Slider

## Tech
- Python 3.12
- CustomTkinter
- Pillow
- JSON
- python-vlc
- mutagen

## Assets
Images from https://www.flaticon.com/

## Status 
Working on progress