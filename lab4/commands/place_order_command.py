from .command import Command
from models.order import Order
from strategies.payment_strategy import PaymentStrategy

class PlaceOrderCommand(Command):
    def __init__(self, repo, order: Order, payment_strategy: PaymentStrategy, notifier):
        self.repo = repo
        self.order = order
        self.payment_strategy = payment_strategy
        self.notifier = notifier
        self.was_executed = False

    @property
    def reversible(self) -> bool:
        return True

    def execute(self):
        # Рассчитываем итоговую сумму
        subtotal = self.order.recalc_subtotal()
        self.order.total = self.payment_strategy.calculate_total(subtotal)
        self.order.payment_method = self.payment_strategy.name()

        # Добавляем в репозиторий
        self.repo.add(order=self.order)

        # Уведомляем наблюдателей
        self.notifier.notify("order_placed", self.order)

        # Подтверждаем заказ
        self.order.confirm()
        print(f"[КОМАНДА] Заказ №{self.order.id} оформлен.")

        self.was_executed = True

    def undo(self):
        if not self.was_executed:
            return

        # Удаляем заказ из репозитория
        self.repo.remove(self.order.id)

        # Уведомляем о отмене
        self.notifier.notify("order_canceled", self.order)

        # Возврат денег (условно — просто сообщение)
        self.notifier.notify("order_refunded", self.order)

        print(f"[КОМАНДА] Заказ №{self.order.id} отменён. Деньги возвращены клиенту.")
        self.was_executed = False