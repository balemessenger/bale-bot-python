from enum import Enum


class MoneyRequestType(Enum):
    normal = "MoneyRequestNormal"
    bill = "MoneyRequestBill"
    payment = "MoneyRequestPayment"

    def __str__(self):
        return self.value

