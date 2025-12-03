from typing import List
from .order_item import OrderItem

class Order:
    _next_id = 1  # Статический счетчик ID заказов

    def __init__(self, items: List[OrderItem], payment_method: str, total: float):
        self.id = Order._next_id
        Order._next_id += 1
        self.items = items
        self.payment_method = payment_method
        self.total = total
        self.status = "НОВЫЙ"

    def recalc_subtotal(self) -> float:
        return sum(item.line_total for item in self.items)

    def add_item(self, name: str, price: float, qty: int):
        item = OrderItem(name, price, qty)
        self.items.append(item)

    def summary(self) -> str:
        lines = [f"Заказ №{self.id} — статус: {self.status}"]
        lines.append("Состав заказа:")
        for item in self.items:
            lines.append(f"  • {item}")
        lines.append(f"Итого без скидок/наценок: {self.recalc_subtotal():.2f} $.")
        lines.append(f"Способ оплаты: {self.payment_method}")
        lines.append(f"Сумма к оплате: {self.total:.2f} $.")
        return "\n".join(lines)

    def confirm(self):
        self.status = "ОФОРМЛЕН"