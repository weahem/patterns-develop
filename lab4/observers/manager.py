from .observer import Observer

class Manager(Observer):
    def __init__(self, name: str, big_order_threshold: float = 50.0):
        self.name = name
        self.big_order_threshold = big_order_threshold

    def update(self, event: str, payload: any):
        if event == "order_placed":
            if payload.total > self.big_order_threshold:
                print(f"[Менеджер {self.name}] Крупный заказ №{payload.id} ({payload.total:.2f} $.). Контролирую выполнение.")