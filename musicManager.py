import pyglet
from constants import *
pyglet.lib.load_library('avbin')
pyglet.have_avbin=True

class MusicManager:
    soundEffects={}
    musicPlayer=None
    def __init__(self):
        self.loadSoundEffects()
        self.musicPlayer = pyglet.media.Player()
        self.musicPlayer.eos_action = pyglet.media.Player.EOS_LOOP
    def loadSoundEffects(self):
        for name in SOUNDEFFECTNAMES:
            self.soundEffects[name] = pyglet.media.load(SOUNDFOLDER+SOUNDEFFECTNAMES[name], streaming=False)
    def playSoundEffect(self,name):
        self.soundEffects[name].play()
    def playMusic(self,musicname):
        self.musicPlayer.queue(pyglet.media.load(SOUNDFOLDER+MUSICNAMES[musicname]))
        while len(self.musicPlayer._groups)>1:
            self.musicPlayer.next_source()
        if not self.musicPlayer.playing:
            self.musicPlayer.play()