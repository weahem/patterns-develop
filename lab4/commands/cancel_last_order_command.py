from .command import Command

class CancelLastOrderCommand(Command):
    def __init__(self, history):
        self.history = history

    @property
    def reversible(self) -> bool:
        return False  # Отмена отмены не поддерживается в этом примере

    def execute(self):
        last_cmd = self.history.pop()
        if last_cmd and last_cmd.reversible:
            last_cmd.undo()
        else:
            print("[КОМАНДА] Нет команды для отмены или последняя команда необратима.")

    def undo(self):
        raise NotImplementedError("Отмена отмены не поддерживается.")