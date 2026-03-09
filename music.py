import vlc
from mutagen import File

class MusicPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.folder = None
        self.index = 0
        self.musicList = []
        self.file = None
    
    def play(self):
        media = self.instance.media_new(str(self.file))
        self.player.set_media(media)
        media.parse()
        self.player.play()

    def playByName(self, name):
        self.index = self.getIndex(name)
        self.file = self.getFile(self.index)
        self.play()
    
    def playByIndex(self, index):
        self.index = index if index < len(self.musicList) else len(self.musicList) - 1
        self.file = self.getFile(self.index)
        self.play()
        return self.musicList[self.index].replace('.mp3', '')

    def pause(self):
        self.player.pause()
    
    def resume(self):
        self.player.play()

    def get_pos(self): 
        return self.player.get_time() # ms
    
    def set_pos(self, pos): # pos in ms
        self.player.set_time(int(pos))
    
    def setList(self, songs):
        self.musicList = songs
    
    def forward(self, time): # time in ms
        if not self.file:
            return
        ms = min(self.player.get_time() + time, self.getLength())
        self.player.set_time(ms)
    
    def backward(self, time): # time in ms
        if not self.file:
            return
        ms = max(self.player.get_time() - time, 0)
        self.player.set_time(ms)
    
    def next(self):
        self.index = min(self.index + 1, len(self.musicList) - 1)
        self.playByIndex(self.index)
        return self.musicList[self.index].replace('.mp3', '')
    
    def replay(self):
        self.index = max(0, self.index - 1)
        self.playByIndex(self.index)
        return self.musicList[self.index].replace('.mp3', '')
    
    def setFolder(self, name):
        self.folder = name
    
    def getIndex(self, name):
        return self.musicList.index(name) if name in self.musicList else 0 

    def getFile(self,index): # return file path using index
        if index > len(self.musicList) or index < 0:
            return
        self.index = index
        file = self.musicList[self.index]
        return self.folder/file

    def getLength(self): # use mutagen instead vlc because its faster
        audio = File(self.file)
        return int(audio.info.length * 1000)

    def isPlaying(self):
        return self.player.is_playing()