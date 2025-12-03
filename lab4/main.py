import sys
from strategies.payment_strategy import PaymentStrategy
from models.order import Order
from models.order_item import OrderItem
from strategies.cash_payment import CashPayment
from strategies.card_payment import CardPayment
from strategies.bonus_payment import BonusPayment
from observers.cook import Cook
from observers.delivery_man import DeliveryMan
from observers.manager import Manager
from notification_center import NotificationCenter
from commands.place_order_command import PlaceOrderCommand
from commands.cancel_last_order_command import CancelLastOrderCommand
from commands.command_history import CommandHistory

# Меню пиццерии
MENU = [
    ("Маргарита", 7.50),
    ("Пепперони", 8.90),
    ("Четыре сыра", 9.40),
    ("Гавайская", 8.70),
    ("Овощная", 8.20),
    ("Барбекю", 9.80),
]

class OrderRepository:
    def __init__(self):
        self.orders = {}
        self._next_id = 1

    def next_id(self) -> int:
        id_ = self._next_id
        self._next_id += 1
        return id_

    def add(self, order: Order):
        self.orders[order.id] = order

    def get(self, order_id: int) -> Order:
        return self.orders.get(order_id)

    def remove(self, order_id: int):
        if order_id in self.orders:
            del self.orders[order_id]

    def all(self) -> list:
        return list(self.orders.values())

def build_order() -> Order:
    """Сборка заказа через консоль"""
    items = []
    subtotal = 0.0

    print("--- Сбор заказа ---\nМеню:")
    for i, (name, price) in enumerate(MENU, 1):
        print(f"{i}) {name} — {price:.2f} $.")
    print("0) Завершить заказ")

    while True:
        try:
            choice = int(input("Выберите позицию: "))
            if choice == 0:
                break
            if 1 <= choice <= len(MENU):
                name, price = MENU[choice - 1]
                qty = int(input(f"Количество для {name}: "))
                if qty > 0:
                    items.append(OrderItem(name, price, qty))
                    subtotal += price * qty
                    print(f"Добавлено: {name} x{qty}. Промежуточная сумма: {subtotal:.2f} $.")
                else:
                    print("Количество должно быть больше 0.")
            else:
                print("Неверный выбор.")
        except ValueError:
            print("Введите число.")

    if not items:
        print("Заказ пустой.")
        return None

    return Order(items=items, payment_method="", total=0.0)

def choose_payment_strategy() -> PaymentStrategy:
    """Выбор стратегии оплаты"""
    print("Выберите способ оплаты:")
    print("1) Наличные (скидка 2%)")
    print("2) Картой (+2% комиссия)")
    print("3) Бонусами (-5 $. )")

    while True:
        try:
            choice = int(input("> "))
            if choice == 1:
                return CashPayment()
            elif choice == 2:
                return CardPayment()
            elif choice == 3:
                return BonusPayment(bonus_credits=5.0)
            else:
                print("Неверный выбор.")
        except ValueError:
            print("Введите число.")

def show_all_orders(repo: OrderRepository):
    orders = repo.all()
    if not orders:
        print("Нет заказов.")
        return

    for order in orders:
        print("-" * 40)
        print(order.summary())
    print("-" * 40)

def main():
    # Инициализация компонентов
    repo = OrderRepository()
    notifier = NotificationCenter()
    history = CommandHistory()

    # Создаем наблюдателей
    cook = Cook("Алиса")
    delivery_man = DeliveryMan("Борис")
    manager = Manager("Ева", big_order_threshold=50.0)

    notifier.attach(cook)
    notifier.attach(delivery_man)
    notifier.attach(manager)

    # Главный цикл
    while True:
        print("\n" + "="*20 + " Пиццерия — консольное приложение " + "="*20)
        print("1) Сделать заказ")
        print("2) Отменить последний заказ (Undo)")
        print("3) Показать все заказы")
        print("0) Выход")
        choice = input("> ").strip()

        if choice == "1":
            order = build_order()
            if not order:
                continue

            strategy = choose_payment_strategy()

            # Создаем команду размещения заказа
            cmd = PlaceOrderCommand(repo, order, strategy, notifier)

            # Показываем предварительный просмотр
            print("\n--- Просмотр заказа ---")
            print(order.summary())

            confirm = input("Подтвердить заказ? (д/н): ").strip().lower()
            if confirm in ('д', 'y', 'yes', 'да'):
                cmd.execute()
                history.push(cmd)
            else:
                print("Заказ отменён.")

        elif choice == "2":
            undo_cmd = CancelLastOrderCommand(history)
            undo_cmd.execute()

        elif choice == "3":
            show_all_orders(repo)

        elif choice == "0":
            print("Выход...")
            break

        else:
            print("Неизвестная команда.")

if __name__ == "__main__":
    main()