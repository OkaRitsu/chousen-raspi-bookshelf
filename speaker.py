import time
import signal
import sys

import pygame.mixer


class Speaker:
    def __init__(self, play_volume=100):
        self.play_volume = play_volume
        pygame.mixer.init()
        pygame.mixer.music.set_volume( play_volume/100 )

    def stop(self):
        self.goriyou()
        pygame.mixer.music.stop()

    def speak(self, voice_file):
        pygame.mixer.music.load(voice_file)
        pygame.mixer.music.play(loops=0)
        while True:
            if(pygame.mixer.music.get_busy() != True):
                break
            time.sleep( 0.2 )

    def hajimemashite(self):
        self.speak("./voice/hajimemashite.mp3")
        self.speak("./voice/hajimemashite2.mp3")

    def goriyou(self):
        self.speak("./voice/goriyou_arigatou.mp3")
    
    def dengen(self):
        self.speak("./voice/dengen_kitte.mp3.mp3")
    
    def honwodashimasu(self):
        self.speak("./voice/honwodashimasu.mp3")

    def mamechishiki(self):
        self.speak("./voice/mamechishiki.mp3")

    def honwotottekudasai(self):
        self.speak("./voice/honwotottekudasai.mp3")

if __name__ == '__main__':
    speaker = Speaker()
    speaker.hajimemashite()
    speaker.goriyou()
    speaker.dengen()
    speaker.mamechishiki()
    speaker.honwodashimasu()
    speaker.stop()
