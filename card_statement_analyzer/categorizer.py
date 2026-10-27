import re
from typing import Tuple

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
    "Active 0% Installments": [
        r"\d{3}/\d{3}"  # matches 001/010, 002/003, etc.
    ],
    "Payments & Credits": [
        r"PAYMENT", r"THANK YOU", r"\bCR\b", r"^CB\s+", r"CASHBACK"
    ]
}

def classify(description: str, amount: float) -> Tuple[str, bool, bool]:
    """
    Returns (category, is_installment, is_credit)
    """
    upper_desc = description.upper()
    
    # Check payments & cashbacks
    if amount < 0 and ("PAYMENT" in upper_desc or "THANK YOU" in upper_desc):
        return ("Payments & Credits", False, True)
    if upper_desc.startswith("CB ") or "CASHBACK" in upper_desc or amount < 0:
        if "PAYMENT" in upper_desc or "THANK YOU" in upper_desc:
            return ("Payments & Credits", False, True)
        # Note: some transit discounts are negative amounts (e.g. BTS Lat Phrao -15)
        # They will be categorized as Transport & Commute with is_credit=True
    
    # Check 0% Installment counters
    if re.search(r"\d{3}/\d{3}", upper_desc):
        return ("Active 0% Installments", True, False)
        
    for cat, patterns in CATEGORY_RULES.items():
        if cat in ["Active 0% Installments", "Payments & Credits"]:
            continue
        for pat in patterns:
            if re.search(pat, upper_desc, re.IGNORECASE):
                return (cat, False, amount < 0)
                
    if amount < 0:
        return ("Payments & Credits", False, True)
        
    return ("Shopping & Retail" if any(w in upper_desc for w in ["STORE", "SHOP", "MARKET"]) else "Other / Miscellaneous", False, False)
