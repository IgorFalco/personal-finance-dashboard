
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date
from decimal import Decimal
from pydantic import BaseModel


# ===== Domínio =====
@dataclass
class Transaction:
    date: date
    id: str
    value: Decimal
    description: str
    is_expense: bool
    category: str = None

# ===== API / Schema =====


class TransactionOutputSchema(BaseModel):
    date: date
    id: str
    value: Decimal
    description: str
    is_expense: bool
    category: str | None

    @classmethod
    def from_transaction(cls, transaction: Transaction) -> TransactionOutputSchema:
        return cls(**asdict(transaction))
