# main.py - Главный файл приложения кофейни

from lab3.facade.coffee_shop_facade import CoffeeShopFacade

def main():
    """
    Точка входа. Запускает консольное меню кофейни.
    """
    print("Добро пожаловать в нашу кофейню!")
    print("=" * 40)

    # Создаем фасад — единая точка взаимодействия
    coffee_shop = CoffeeShopFacade()

    while True:
        print("\nМеню:")
        print("1) Добавить напиток")
        print("2) Показать чек")
        print("3) Отправить заказ на приготовление")
        print("4) Новый заказ")
        print("0) Выход")
        command = input("Команда: ").strip()

        if command == "0":
            print("До свидания!")
            break
        elif command == "1":
            add_drink(coffee_shop)
        elif command == "2":
            show_receipt(coffee_shop)
        elif command == "3":
            send_order(coffee_shop)
        elif command == "4":
            coffee_shop.reset()
            print("✅ Новый заказ создан.")
        else:
            print("Неверная команда. Попробуйте снова.")


def add_drink(coffee_shop):
    """Добавляет напиток в заказ."""
    print("\nВыберите напиток:")
    print("1) Эспрессо")
    print("2) Латте")
    print("3) Капучино")
    print("0) Назад")
    choice = input("Ваш выбор: ").strip()

    if choice == "0":
        return

    base_drink = None
    if choice == "1":
        base_drink = coffee_shop._create_beverage("espresso")
    elif choice == "2":
        base_drink = coffee_shop._create_beverage("latte")
    elif choice == "3":
        base_drink = coffee_shop._create_beverage("cappuccino")
    else:
        print("Неверный выбор.")
        return

    current_drink = base_drink

    # Сахар
    sugar_input = input("Сколько ложек сахара? (0..10, Enter=0): ").strip()
    sugar_spoons = int(sugar_input) if sugar_input.isdigit() else 0
    if sugar_spoons > 0:
        current_drink = coffee_shop._add_sugar(current_drink, sugar_spoons)

    # Молоко
    milk_choice = input("Добавить молоко? [y/N]: ").strip().lower()
    if milk_choice in ['y', 'yes', 'да']:
        current_drink = coffee_shop._add_milk(current_drink)

    # Корица
    cinnamon_choice = input("Добавить корицу? (по четвергам скидка) [y/N]: ").strip().lower()
    if cinnamon_choice in ['y', 'yes', 'да']:
        current_drink = coffee_shop._add_cinnamon(current_drink)

    # Добавляем в заказ
    result = coffee_shop.add_drink(current_drink)
    print(f"✅ {result}")


def show_receipt(coffee_shop):
    """Показывает чек."""
    if not coffee_shop.order.items:
        print("Чек пуст.")
        return

    print("\nЧЕК")
    for i, item in enumerate(coffee_shop.order.items, 1):
        print(f"{i}. {item.get_description()} — {item.cost():.2f} $")

    print("-" * 30)
    total = coffee_shop.total()
    print(f"Итого: {total:.2f} $")


def send_order(coffee_shop):
    """Отправляет заказ на приготовление."""
    if not coffee_shop.order.items:
        print("Заказ пуст. Нечего готовить.")
        return

    print("\nРЕЗУЛЬТАТ ПРИГОТОВЛЕНИЯ:")
    try:
        prepared_result = coffee_shop.place_order()
        print(f"✅ {prepared_result.message}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

    total = coffee_shop.total()
    print(f"\nИТОГО К ОПЛАТЕ: {total:.2f} $")


if __name__ == "__main__":
    main()