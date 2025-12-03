from .payment_strategy import PaymentStrategy

class CashPayment(PaymentStrategy):
    def name(self) -> str:
        return "Наличные"

    def calculate_total(self, subtotal: float) -> float:
        return subtotal * 0.98  # 2% скидка