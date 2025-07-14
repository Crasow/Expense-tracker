from pydantic import BaseModel
from expense_tracker.enums import BalanceChangeType
from datetime import datetime


class BalanceChangeBase(BaseModel):
    user_id: int
    category_id: int
    amount: float
    description: str
    date: datetime
    type: BalanceChangeType


class BalanceChangeCreate(BalanceChangeBase):
    pass

class BalanceChangeRead(BalanceChangeBase):
    pass

class BalanceChangeUpdate(BalanceChangeBase):
    pass

