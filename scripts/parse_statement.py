#!/usr/bin/env python3
"""
Credit Card Statement Parser & Analyzer Helper
Supports standard formats from Thai banks (ttb, UOB, KBank, SCB, etc.)
"""

import sys
import re
import json
from collections import defaultdict
from datetime import datetime

# Common merchant keyword rules for Thai credit cards
CATEGORY_RULES = {
    "Transport & Commute": [
        r"BTS", r"MRT", r"BEM", r"ARL\b", r"GRAB", r"EXPRESSWAY",
        r"TOLLWAY", r"DON MUANG TOLLWAY", r"BANGCHAK", r"BSRC",
        r"PTT\b", r"SHELL", r"CALTEX", r"SUSCO"
    ],
    "Groceries & Convenience": [
        r"7-11", r"TMN 7-11", r"MINI BIG C", r"BIG C", r"TOPS",
        r"LOTUS", r"SUPER TURTLE", r"GO WHOLESALE", r"MAKRO",
        r"VILLA MARKET", r"GOURMET MARKET", r"MAXVALU", r"FOODLAND"
    ],
    "Food & Dining": [
        r"MCDONALD", r"MCD-", r"KFC", r"OHKAJHU", r"BEARHOUSE",
        r"LPE\*BEARHOUSE", r"YAMAZAKI", r"STARBUCKS", r"AMAZON\b",
        r"KAMU", r"HAMASUSHI", r"JOJO RESTAURANT", r"B AND B FOOD",
        r"SHABUSHI", r"MK RESTAURANT", r"BONCHON", r"SWENSEN",
        r"RESTAURANT", r"CAFE", r"BAKERY", r"FOOD"
    ],
    "Subscriptions & Bills": [
        r"SPOTIFY", r"YOUTUBE", r"NETFLIX", r"GOOGLE", r"APPLE\.COM",
        r"AIS\b", r"TRUE\b", r"DTAC", r"NT BROADBAND", r"3BB",
        r"PRIME VIDEO", r"DISNEY"
    ],
    "Fitness & Wellness": [
        r"JETTS", r"FITWHEY", r"DECATHLON", r"FITNESS FIRST",
        r"VIRGIN ACTIVE", r"SUPERSPORTS", r"CRC SPORTS"
    ],
    "Shopping & Retail": [
        r"CENTRAL DEPT", r"ROBINSON", r"THE MALL", r"EMQUARTIER",
        r"EMPORIUM", r"EMSPHERE", r"SIAM PARAGON", r"UNIQLO",
        r"ZARA", r"H&M", r"B2S", r"STUDIO7", r"ISTUDIO",
        r"POWER BUY", r"HOMEPRO", r"CMG\b", r"CENTRAL TRADI",
        r"SHOPEE", r"LAZADA", r"TIKTOK SHOP"
    ],
    "Installments (0%)": [
        r"\d{3}/\d{3}"  # matches 001/010, 002/003, etc.
    ],
    "Payments & Credits": [
        r"PAYMENT", r"THANK YOU", r"\bCR\b", r"^CB\s+", r"CASHBACK"
    ]
}

def classify_transaction(desc: str, amount: float) -> str:
    upper_desc = desc.upper()
    
    # Check payments & cashbacks first
    if amount < 0 and ("PAYMENT" in upper_desc or "THANK YOU" in upper_desc):
        return "Payments & Credits"
    if upper_desc.startswith("CB ") or "CASHBACK" in upper_desc:
        return "Payments & Credits"
    
    # Check 0% Installment counters like 001/010 or 002/003
    if re.search(r"\d{3}/\d{3}", upper_desc):
        return "Installments (0%)"
    
    # Check other categories
    for cat, patterns in CATEGORY_RULES.items():
        if cat in ["Installments (0%)", "Payments & Credits"]:
            continue
        for pat in patterns:
            if re.search(pat, upper_desc, re.IGNORECASE):
                return cat
                
    return "Other / Miscellaneous"

def analyze_statement_data(transactions: list) -> dict:
    """
    transactions: list of dicts:
      {'trans_date': str, 'post_date': str, 'desc': str, 'amt': float}
    """
    total_debits = 0.0
    total_credits = 0.0
    categories = defaultdict(lambda: {"count": 0, "total": 0.0, "items": []})
    micro_spends = defaultdict(list)
    big_tickets = []

    for tx in transactions:
        desc = tx["desc"]
        amt = float(tx["amt"])
        
        # Determine category
        cat = classify_transaction(desc, amt)
        
        # Debits vs credits tracking
        if amt < 0 or "CR" in desc.upper() or cat == "Payments & Credits":
            total_credits += abs(amt)
        else:
            total_debits += amt

        categories[cat]["count"] += 1
        categories[cat]["total"] += amt
        categories[cat]["items"].append(tx)

        # Micro-spending tracker (under 200 THB)
        if 0 < amt <= 200:
            vendor_clean = re.sub(r"\s+(BANGKOK|TH|BRANCH).*$", "", desc, flags=re.IGNORECASE).strip()
            micro_spends[vendor_clean].append(amt)

        # Big tickets (> 5,000 THB positive and not installment)
        if amt >= 5000 and not re.search(r"\d{3}/\d{3}", desc):
            big_tickets.append(tx)

    net_balance = sum(tx["amt"] for tx in transactions)

    # Calculate micro-spending velocity
    velocity_stats = []
    for vendor, amounts in micro_spends.items():
        if len(amounts) >= 3:
            velocity_stats.append({
                "vendor": vendor,
                "count": len(amounts),
                "total": sum(amounts),
                "avg": sum(amounts) / len(amounts)
            })
    velocity_stats.sort(key=lambda x: x["count"], reverse=True)

    return {
        "summary": {
            "transaction_count": len(transactions),
            "total_debits": total_debits,
            "total_credits": total_credits,
            "net_balance": net_balance
        },
        "categories": dict(categories),
        "micro_spending_velocity": velocity_stats,
        "big_tickets": big_tickets
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
            result = analyze_statement_data(data)
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Usage: python3 parse_statement.py [transactions.json]")
