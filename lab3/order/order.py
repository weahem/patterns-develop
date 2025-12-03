# order/order.py - Класс заказа

class Order:
    """
    Класс, представляющий заказ клиента.
    Хранит список выбранных напитков.
    """

    def __init__(self):
        self.items = []  # Список объектов Beverage

    def add_item(self, beverage):
        """
        Добавляет напиток в заказ.
        """
        self.items.append(beverage)

    def total(self):
        """
        Возвращает общую стоимость заказа.
        """
        return sum(item.cost() for item in self.items)

    def receipt_text(self):
        """
        Генерирует текст чека.
        """
        lines = ["ЧЕК", "-" * 30]
        for i, item in enumerate(self.items, 1):
            lines.append(f"{i}. {item.get_description()} - {item.cost():.2f} руб.")
        lines.append("-" * 30)
        lines.append(f"ИТОГО: {self.total():.2f} руб.")
        return "\n".join(lines)