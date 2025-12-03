from .payment_strategy import PaymentStrategy

class CardPayment(PaymentStrategy):
    def name(self) -> str:
        return "Карта"

    def calculate_total(self, subtotal: float) -> float:
        return subtotal * 1.02  # +2% комиссия