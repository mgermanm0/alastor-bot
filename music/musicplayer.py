from collections import deque
from turtle import title
from discord.embeds import Embed
class LoopMode:
    NONE = 0
    SONG = 1
    QUEUE = 2

class MusicQueue:
    def __init__(self) -> None:
        self.__queue = deque()    
        self.__loop = LoopMode.NONE
        self.__playing = ""

    def push(self, src):
        self.__queue.append(src)
    
    def pop(self):
        if len(self.__queue) <= 0:
            return None
        next = self.__queue.popleft()
        if self.__loop == LoopMode.SONG:
            self.__queue.appendleft(next)
        if self.__loop == LoopMode.QUEUE:
            self.__queue.append(next)
        self.__playing = next['title']
        return next
    
    def setLoopMode(self, mode):
        self.__loop = mode
    
    def getLoopMode(self):
        return self.__loop

    def getQueue(self):
        embed = Embed(title="Cola de reproducción")
        embed.add_field(name="En reproducción", value=self.__playing)
        desc = ""
        for i, elem in enumerate(self.__queue):
            desc += str(i+1) + ") " + elem['title'] + "\n"
        if desc != "":
            embed.add_field(name="Siguientes", value=desc)
        return embed
    
class MusicPlayer:
    def __init__(self) -> None:
        self.__queues = dict()
    
    def __newQueue(self, id):
        self.__queues[id] = MusicQueue()
        
    def push(self, id, src):
        if id not in self.__queues:
            self.__newQueue(id)
        self.__queues[id].push(src)
        
    def pop(self, id):
        return self.__queues[id].pop()
    
    def setLoopMode(self, id, mode):
        self.__queues[id].setLoop(mode)
    
    def getLoopMode(self, id):
        return self.__queues[id].getLoopMode()
    
    def getQueue(self, id):
        return self.__queues[id].getQueue()
        