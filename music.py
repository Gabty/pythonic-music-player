from pygame import mixer as mx
from pathlib import Path

class MusicPlayer:
    def __init__(self):
        mx.init()
        self.folder = None
        self.index = 0
        self.musicList = []
    
    def play(self, name):
        self.index = self.getIndex(name)
        mx.music.load()
        mx.music.play()

    def stop(self):
        mx.music.stop()

    def pause(self):
        mx.music.pause()
    
    def resume(self):
        mx.music.unpause()

    def get_pos(self):
        return mx.music.get_pos()
    
    def set_pos(self, pos):
        mx.music.set_pos(pos=pos)
    
    def setList(self, songs):
        self.musicList = songs
    
    def setFolder(self, name):
        self.folder = name
    
    def getIndex(self, name):
        return self.musicList.index(name) if name in self.musicList else 0

    def concat(self,index):
        file = self.musicList[index]
        return str(self.folder/file)
