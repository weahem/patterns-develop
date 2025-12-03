# condiment/decorators.py - Декораторы для ингредиентов (Concrete Decorators)

from abc import ABC, abstractmethod
from lab3.beverage.base import Beverage

class CondimentDecorator(Beverage, ABC):
    """
    Абстрактный декоратор. Наследуется от Beverage,
    чтобы можно было оборачивать как напитки, так и другие декораторы.
    """
    def __init__(self, beverage):
        super().__init__()
        self._beverage = beverage  # Оборачиваемый объект

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def cost(self):
        pass


class Sugar(CondimentDecorator):
    """Конкретный декоратор: сахар."""
    def __init__(self, beverage, spoons=1):
        super().__init__(beverage)
        self.spoons = spoons
        self.description = f"{beverage.get_description()}, {spoons} ложка(и) сахара"

    def get_description(self):
        return self.description

    def cost(self):
        return self._beverage.cost() + (self.spoons * 5.0)  # 5 руб. за ложку


class Milk(CondimentDecorator):
    """Конкретный декоратор: молоко."""
    def __init__(self, beverage):
        super().__init__(beverage)
        self.description = f"{beverage.get_description()}, молоко"

    def get_description(self):
        return self.description

    def cost(self):
        return self._beverage.cost() + 10.0  # 10 руб. за порцию


class Cinnamon(CondimentDecorator):
    """Конкретный декоратор: корица."""
    def __init__(self, beverage):
        super().__init__(beverage)
        self.description = f"{beverage.get_description()}, корица"

    def get_description(self):
        return self.description

    def cost(self):
        return self._beverage.cost() + 8.0  # 8 руб. за порцию