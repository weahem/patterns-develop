from .observer import Observer

class Cook(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, event: str, payload: any):
        if event == "order_placed":
            print(f"[Повар {self.name}] Получен заказ №{payload.id}. Начинаю готовку.")