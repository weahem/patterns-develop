# facade/coffee_shop_facade.py - Фасад кофейни (Facade Pattern)

from lab3.order.order import Order
from lab3.machine.adapter import MachineAdapter
from lab3.beverage.base import Beverage
from lab3.condiment.decorators import Sugar, Milk, Cinnamon
from lab3.machine.adapter import MachineAdapter, PreparedResult

class CoffeeShopFacade:
    """
    Фасад кофейни — единая точка взаимодействия для клиента.
    Скрывает сложность системы: заказ, расчёт стоимости, работа с кофемашиной.
    """

    def __init__(self):
        self.order = Order()
        self._adapter = MachineAdapter()  # Адаптер для работы со старой машиной

    def add_drink(self, beverage: Beverage):
        """
        Добавляет напиток в текущий заказ.
        Возвращает строку с описанием и стоимостью.
        """
        self.order.add_item(beverage)
        return f"Добавлено: {beverage.get_description()} - {beverage.cost():.2f} руб."

    def place_order(self):
        """
        Отправляет весь заказ на кофемашину через адаптер.
        Возвращает объект PreparedResult с результатом.
        """
        if not self.order.items:
            return PreparedResult("❌ Заказ пуст. Нечего готовить.")

        for item in self.order.items:
            result = self._adapter.prepare(item)
            if not result.message.startswith("☕"):
                return result  # Возвращаем ошибку, если она произошла

        return PreparedResult("✅ Все напитки успешно приготовлены!")

    def print_receipt(self):
        """
        Генерирует текст чека с детализацией заказа.
        """
        lines = ["ЧЕК", "-" * 30]
        total_cost = 0.0

        for i, item in enumerate(self.order.items, 1):
            line = f"{i}. {item.get_description()} - {item.cost():.2f} руб."
            lines.append(line)
            total_cost += item.cost()

        lines.append("-" * 30)
        lines.append(f"ИТОГО: {total_cost:.2f} руб.")
        return "\n".join(lines)

    def total(self):
        """Возвращает общую стоимость заказа."""
        return sum(item.cost() for item in self.order.items)

    def reset(self):
        """Сбрасывает текущий заказ."""
        self.order = Order()

    # Вспомогательные методы для создания напитков и добавления ингредиентов
    def _create_beverage(self, name: str):
        """Создаёт базовый напиток по имени."""
        from beverage.base import Espresso, Latte, Cappuccino
        if name == "espresso":
            return Espresso()
        elif name == "latte":
            return Latte()
        elif name == "cappuccino":
            return Cappuccino()
        else:
            raise ValueError(f"Неизвестный напиток: {name}")

    def _add_sugar(self, beverage: Beverage, spoons: int = 1):
        """Добавляет сахар в напиток."""
        from condiment.decorators import Sugar
        return Sugar(beverage, spoons)

    def _add_milk(self, beverage: Beverage):
        """Добавляет молоко в напиток."""
        from condiment.decorators import Milk
        return Milk(beverage)

    def _add_cinnamon(self, beverage: Beverage):
        """Добавляет корицу в напиток."""
        from condiment.decorators import Cinnamon
        return Cinnamon(beverage)