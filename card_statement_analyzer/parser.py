import re
from collections import defaultdict
from typing import List, Dict, Any
from .models import Transaction, MicroSpendingVelocity, StatementSummary
from .categorizer import classify

def parse_transactions(raw_items: List[Dict[str, Any]]) -> StatementSummary:
    """
    Parses a list of transaction dictionaries:
    [{'trans_date': ..., 'post_date': ..., 'desc': ..., 'amt': ...}]
    """
    transactions: List[Transaction] = []
    total_debits = 0.0
    total_credits = 0.0
    category_map = defaultdict(lambda: {"count": 0, "total": 0.0, "items": []})
    micro_spends = defaultdict(list)
    big_tickets: List[Transaction] = []

    for item in raw_items:
        desc = item.get("desc", item.get("description", ""))
        amt = float(item.get("amt", item.get("amount", 0.0)))
        t_date = item.get("trans_date", item.get("date", ""))
        p_date = item.get("post_date", item.get("post", ""))

        category, is_inst, is_cred = classify(desc, amt)

        tx = Transaction(
            trans_date=t_date,
            post_date=p_date,
            description=desc,
            amount=amt,
            category=category,
            is_installment=is_inst,
            is_credit=is_cred
        )
        transactions.append(tx)

        if amt < 0 or is_cred:
            total_credits += abs(amt)
        else:
            total_debits += amt

        category_map[category]["count"] += 1
        category_map[category]["total"] += amt
        category_map[category]["items"].append({
            "trans_date": t_date,
            "post_date": p_date,
            "description": desc,
            "amount": amt
        })

        # Micro spending velocity (< 200 THB)
        if 0 < amt <= 200:
            clean_name = re.sub(r"\s+(BANGKOK|TH|BRANCH).*$", "", desc, flags=re.IGNORECASE).strip()
            micro_spends[clean_name].append(amt)

        # Big tickets (>= 5,000 THB and not installment)
        if amt >= 5000 and not is_inst:
            big_tickets.append(tx)

    velocity: List[MicroSpendingVelocity] = []
    for vendor, amounts in micro_spends.items():
        if len(amounts) >= 3:
            velocity.append(MicroSpendingVelocity(
                vendor=vendor,
                count=len(amounts),
                total_amount=sum(amounts),
                avg_ticket_size=sum(amounts) / len(amounts)
            ))
    velocity.sort(key=lambda x: x.count, reverse=True)

    net_billed = sum(tx.amount for tx in transactions)

    return StatementSummary(
        total_transactions=len(transactions),
        total_debits=total_debits,
        total_credits=total_credits,
        net_billed_amount=net_billed,
        categories=dict(category_map),
        micro_spending_velocity=velocity,
        big_tickets=big_tickets
    )
