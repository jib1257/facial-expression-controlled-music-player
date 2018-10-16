import pygame
import random
import time
from os import listdir
from os.path import isfile, join
#import glob

DURATION = 8 # play duration in sec

def m_player(mood,playlist_directory):
#    if mood == 'angry':
     pygame.init()
     pygame.mixer.init()
     onlysongs = [join(playlist_directory,f) for f in listdir(playlist_directory) if isfile(join(playlist_directory,f))]
     print(onlysongs)
#    print(glob.glob(playlist_directory))
     song = random.choice(onlysongs)
#To do: generate a list of files in the playlist folder
     print(song)
     player = pygame.mixer.music
     player.load(song)
     player.play(-1)
     time.sleep(DURATION)
     player.stop()
#    if mood == 'sad':
#        song = random.choice(angry_playlist)
#        player = vlc.MediaPlayer(song)
#       player.play()
#        time.sleep(DURATION)
#        player.pause()
#        player.stop
#    if mood == 'surprise':
#        song = random.choice(angry_playlist)
#        player = vlc.MediaPlayer(song)
#        player.play()
#        time.sleep(DURATION)
#        player.pause()
#        player.stop
#    if mood == 'happy':
#        song = random.choice(angry_playlist)
#        player = vlc.MediaPlayer(song)
#        player.play()
#        time.sleep(DURATION)
#        player.pause()
#        player.stop
#    else:
#        pass

    

