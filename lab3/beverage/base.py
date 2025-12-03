# beverage/base.py - Базовые классы напитков (Component)

class Beverage:
    """
    Абстрактный компонент. Базовый класс для всех напитков.
    Реализует методы get_description и cost.
    """
    def __init__(self):
        self.description = "Неизвестный напиток"

    def get_description(self):
        """Возвращает описание напитка."""
        return self.description

    def cost(self):
        """Возвращает стоимость напитка. Должен быть переопределен."""
        raise NotImplementedError("Метод cost() должен быть реализован")


class Espresso(Beverage):
    """Конкретный компонент: эспрессо."""
    def __init__(self):
        super().__init__()
        self.description = "Эспрессо"

    def cost(self):
        return 50.0


class Latte(Beverage):
    """Конкретный компонент: латте."""
    def __init__(self):
        super().__init__()
        self.description = "Латте"

    def cost(self):
        return 80.0


class Cappuccino(Beverage):
    """Конкретный компонент: капучино."""
    def __init__(self):
        super().__init__()
        self.description = "Капучино"

    def cost(self):
        return 75.0