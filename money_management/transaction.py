from datetime import date
from enum import Enum
from dataclasses import dataclass

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


# 一日のお金が動いた記録
@dataclass
class Transaction:
    transaction_date: date  # 日付
    amount: int             # 金額

    transaction_type: str   # income or expense
    category: str           # 食費、給料など
    memo: str= ""           # めも

    def __str__(self):
        return (f"{self.transaction_date} | "
                f"{self.transaction_type.value} | "
                f"{self.category} | "
                f"{self.amount}円"
                )
    
    def is_income(self):
        return self.transaction_type == TransactionType.INCOME
    def is_expense(self):
        return self.transaction_type == TransactionType.EXPENSE
    
    def get_signed_amount(self):
        if self.transaction_type == TransactionType.INCOME:
            return self.amount
        return self.amount*-1
    
    def to_dict(self):
        return{
            "date":self.transaction_date.isoformat(),
            "amount":self.amount,
            "type":self.transaction_type.value,
            "category":self.category,
            "memo":self.memo
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            transaction_date = date.fromisoformat(data["date"]),
            amount = data["amount"],
            transaction_type = TransactionType(data["type"]),
            category = data["category"],
            memo = data["memo"]
        )