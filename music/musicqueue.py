import queue
from typing_extensions import Self


class MusicQueue:
    def __init__(self) -> None:
        self.queue = queue()