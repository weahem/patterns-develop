# Модель элемента заказа
class OrderItem:
    def __init__(self, name: str, price: float, qty: int):
        self.name = name
        self.price = price
        self.qty = qty

    @property
    def line_total(self) -> float:
        return self.price * self.qty

    def __str__(self):
        return f"{self.name} x{self.qty} @ {self.price:.2f} = {self.line_total:.2f} $."