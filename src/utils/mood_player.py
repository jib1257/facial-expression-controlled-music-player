import vlc
import time
import random


def mood_player(mood):
    if mood == 'angry':
        song = random.choice(angry_playlist)
        player = vlc.MediaPlayer(song)
        player.play()
        time.sleep(DURATION)
        player.pause()
        player.stop
    if mood == 'sad':
        song = random.choice(angry_playlist)
        player = vlc.MediaPlayer(song)
        player.play()
        time.sleep(DURATION)
        player.pause()
        player.stop
    if mood == 'surprise':
        song = random.choice(angry_playlist)
        player = vlc.MediaPlayer(song)
        player.play()
        time.sleep(DURATION)
        player.pause()
        player.stop
    if mood == 'happy':
        song = random.choice(angry_playlist)
        player = vlc.MediaPlayer(song)
        player.play()
        time.sleep(DURATION)
        player.pause()
        player.stop
    else:
        pass

    

