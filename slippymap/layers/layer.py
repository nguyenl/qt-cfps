from abc import ABCMeta, abstractmethod


class Layer(metaclass=ABCMeta):
    def __init__(self, parent):
        self._enabled = True
        self.parent = parent
    
    @abstractmethod
    def paint(self):
        pass

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
