from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event: str, payload: any):
        pass