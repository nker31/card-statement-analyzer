from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Transaction:
    trans_date: str
    post_date: str
    description: str
    amount: float
    category: str = "Uncategorized"
    is_installment: bool = False
    is_credit: bool = False

@dataclass
class MicroSpendingVelocity:
    vendor: str
    count: int
    total_amount: float
    avg_ticket_size: float

@dataclass
class StatementSummary:
    total_transactions: int
    total_debits: float
    total_credits: float
    net_billed_amount: float
    categories: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    micro_spending_velocity: List[MicroSpendingVelocity] = field(default_factory=list)
    big_tickets: List[Transaction] = field(default_factory=list)
