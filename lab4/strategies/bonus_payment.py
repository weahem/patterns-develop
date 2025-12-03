from .payment_strategy import PaymentStrategy

class BonusPayment(PaymentStrategy):
    def __init__(self, bonus_credits: float = 5.0):
        self.bonus_credits = bonus_credits

    def name(self) -> str:
        return "Бонусами"

    def calculate_total(self, subtotal: float) -> float:
        return max(0, subtotal - self.bonus_credits)