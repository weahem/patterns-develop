from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def calculate_total(self, subtotal: float) -> float:
        pass