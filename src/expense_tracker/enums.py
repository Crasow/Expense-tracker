from enum import Enum


class RepetitionType(Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class BalanceChangeType(Enum):
    INCOME = "income"
    EXPENSE = "expense"
    
class CategoryType(Enum):
    EXPENSE = "expense"
    INCOME = "income"