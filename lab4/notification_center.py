from typing import List
from observers.observer import Observer

class NotificationCenter:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event: str, payload: any):
        for observer in self._observers:
            observer.update(event, payload)