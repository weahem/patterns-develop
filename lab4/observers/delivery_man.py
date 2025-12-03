from .observer import Observer

class DeliveryMan(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, event: str, payload: any):
        if event == "order_ready":
            print(f"[Курьер {self.name}] Заказ №{payload.id} готов к доставке.")