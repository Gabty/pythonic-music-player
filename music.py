from pygame import mixer as mx
from mutagen import File

class MusicPlayer:
    def __init__(self):
        mx.init()
        self.folder = None
        self.index = 0
        self.musicList = []
    
    def playByName(self, name):
        mx.music.unload()
        self.index = self.getIndex(name)
        file = self.getFile(self.index)
        print(file)
        mx.music.load(file)
        mx.music.play()
    
    def playByIndex(self, index):
        mx.music.unload()
        mx.music.load(self.getFile(index))
        mx.music.play()

    def pause(self):
        mx.music.pause()
    
    def resume(self):
        mx.music.unpause()

    def get_pos(self):
        return mx.music.get_pos()
    
    def set_pos(self, pos):
        mx.music.set_pos(pos)
    
    def setList(self, songs):
        self.musicList = songs
    
    def setFolder(self, name):
        self.folder = name
    
    def getIndex(self, name):
        return self.musicList.index(name) if name in self.musicList else 0 # 

    def getFile(self,index): # return file path using index
        if index > len(self.musicList) or index < 0:
            return
        self.index = index
        file = self.musicList[self.index]
        return str(self.folder/file)

    def getLength(self):
        audio = File(self.getFile(self.index))
        return int(audio.info.length * 1000)