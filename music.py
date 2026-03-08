from pygame import mixer as mx

class MusicPlayer:
    def __init__(self, master):
        mx.init()
        self.master = master
        self.current_music = None
    
    def play(self, path):
        mx.music.load(path)
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
