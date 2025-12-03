from abc import ABC, abstractmethod

class Command(ABC):
    @property
    @abstractmethod
    def reversible(self) -> bool:
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass