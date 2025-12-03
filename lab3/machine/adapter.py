from .legacy import LegacyCoffeeMachine
from lab3.beverage.base import Espresso, Latte, Cappuccino
from lab3.condiment.decorators import CondimentDecorator, Sugar, Milk, Cinnamon

class NewCoffeeMachineInterface:
    """
    Новый стандартный интерфейс для кофемашины.
    Определяет метод prepare, который будет использоваться фасадом.
    """
    def prepare(self, beverage):
        """
        Подготавливает напиток.
        Принимает объект напитка (Beverage) и возвращает результат.
        """
        raise NotImplementedError("Метод prepare() должен быть реализован")


class MachineAdapter(NewCoffeeMachineInterface):
    """
    Адаптер, преобразующий вызовы нового интерфейса в вызовы старой машины.
    Реализует паттерн Adapter.
    """
    def __init__(self):
        self._legacy_machine = LegacyCoffeeMachine()

    def prepare(self, beverage):
        """
        Адаптирует вызов prepare() к старому интерфейсу make_drink().
        Анализирует объект напитка и его декораторы, чтобы определить параметры.
        """
        # Проверяем состояние машины перед приготовлением
        if not self._legacy_machine.check_supplies():
            return PreparedResult("❌ Ошибка: Недостаточно ингредиентов.")

        if self._legacy_machine.service_required():
            return PreparedResult("❌ Ошибка: Требуется обслуживание машины.")

        # Определяем базовый напиток и ингредиенты
        base_code = None
        sugar_spoons = 0
        with_milk = False
        with_cinnamon = False

        # Рекурсивно обходим цепочку декораторов
        current = beverage
        while isinstance(current, CondimentDecorator):
            if isinstance(current, Sugar):
                sugar_spoons = current.spoons
            elif isinstance(current, Milk):
                with_milk = True
            elif isinstance(current, Cinnamon):
                with_cinnamon = True
            current = current._beverage

        # Определяем код напитка
        if isinstance(current, Espresso):
            base_code = "E"
        elif isinstance(current, Latte):
            base_code = "L"
        elif isinstance(current, Cappuccino):
            base_code = "C"
        else:
            return PreparedResult("❌ Ошибка: Неизвестный тип напитка.")

        # Готовим через старый интерфейс
        result_message = self._legacy_machine.make_drink(
            code=base_code,
            sugar=sugar_spoons,
            with_milk=with_milk,
            with_cinnamon=with_cinnamon
        )

        return PreparedResult(result_message)


class PreparedResult:
    """
    Класс результата приготовления напитка.
    """
    def __init__(self, message: str):
        self.message = message