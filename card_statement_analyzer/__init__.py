"""
Card Statement Analyzer
Universal parser and categorization engine for Thai bank credit card statements.
"""

from .models import Transaction, StatementSummary, MicroSpendingVelocity
from .parser import parse_transactions
from .categorizer import classify

__version__ = "0.1.0"
__all__ = ["Transaction", "StatementSummary", "MicroSpendingVelocity", "parse_transactions", "classify"]
