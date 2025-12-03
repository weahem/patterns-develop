# machine/legacy.py - Старая кофемашина (Adaptee)

class LegacyCoffeeMachine:
    """
    Устаревший класс кофемашины. Имеет свой собственный интерфейс.
    Будет адаптирован под новый стандарт.
    """

    def check_supplies(self):
        """Проверяет наличие ингредиентов."""
        print("✅ Проверка запасов... Все ингредиенты в наличии.")
        return True

    def service_required(self):
        """Проверяет, нуждается ли машина в обслуживании."""
        print("✅ Проверка состояния машины... Обслуживание не требуется.")
        return False

    def make_drink(self, code: str, sugar: int = 0, with_milk: bool = False, with_cinnamon: bool = False):
        """
        Готовит напиток по коду и параметрам.
        Это старый интерфейс, который нужно адаптировать.
        """
        drink_names = {"E": "Эспрессо", "L": "Латте", "C": "Капучино"}
        name = drink_names.get(code, "Неизвестный напиток")

        additions = []
        if sugar > 0:
            additions.append(f"{sugar} ложка(и) сахара")
        if with_milk:
            additions.append("молоко")
        if with_cinnamon:
            additions.append("корица")

        additions_str = ", ".join(additions) if additions else "без добавок"
        result = f"☕ Готовлю {name} ({additions_str})..."
        print(result)
        return result