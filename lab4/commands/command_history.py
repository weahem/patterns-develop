from typing import List
from .command import Command

class CommandHistory:
    def __init__(self):
        self._stack: List[Command] = []

    def push(self, cmd: Command):
        self._stack.append(cmd)

    def pop(self) -> Command:
        if self._stack:
            return self._stack.pop()
        return None

    def list(self) -> List[Command]:
        return self._stack.copy()