# 💳 Card Statement Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill%20Ready-green.svg)](https://github.com)

A privacy-first, bank-agnostic statement parser, categorizer, and audit tool for Thai credit cards (**ttb, UOB, KBank, SCB, Citi, etc.**). 

Works seamlessly as a standalone **Python CLI/Library** and as a native **Google Antigravity Skill (`SKILL.md`)**.

---

## 🌟 Key Features

- **🔒 100% Privacy & Offline Execution:** No cloud uploads, no third-party APIs. Your financial transaction data never leaves your machine.
- **🏦 Multi-Bank Layout Engine:** 
  - Supports **ttb** debit/negative transactions (`-15.00 THB`, `-4,242.00 THB`).
  - Supports **UOB** statement layouts, `CR` indicators, and points summary blocks.
- **🔄 Automatic 0% Installment Tracking:** Detects installment counters (e.g., `001/010`, `002/003`) and categorizes them automatically.
- **⚡ Micro-Spending Velocity:** Identifies high-frequency leakage patterns (e.g., *7-Eleven: 44 visits, avg 53.20 THB/visit*).
- **⚠️ Big-Ticket Outlier Alerts:** Automatically flags single purchases $\ge 5,000\text{ THB}$ so you can evaluate 0% installment conversions (Smart Pay / Call for Cash) before the payment due date.
- **📊 Standard Universal Taxonomy:** Classifies transactions into 8 standardized financial buckets (Transport, Groceries, Dining, Subscriptions, Fitness, Retail, 0% Installments, Payments & Credits).

---

## 🚀 Quick Start

### 1. Use as an Antigravity Skill

Simply clone or copy this repository into your workspace's `.agents/skills/` directory:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/nker31/card-statement-analyzer.git ~/.agents/skills/card-statement-analyzer
```

Your Antigravity agent will automatically discover the skill and trigger whenever you ask to parse or audit a statement!

### 2. Standalone CLI Usage

```bash
# Clone the repository
git clone https://github.com/nker31/card-statement-analyzer.git
cd card-statement-analyzer

# Run the analyzer on transaction data
python3 -m card_statement_analyzer.cli sample_transactions.json

# Or output structured JSON
python3 -m card_statement_analyzer.cli sample_transactions.json --json
```

### 3. Python Library Usage

```python
from card_statement_analyzer import parse_transactions

transactions = [
    {"date": "14 SEP", "desc": "TMN 7-11 BANGKOK", "amt": 100.0},
    {"date": "16 SEP", "desc": "BTS VISIONARY PARK", "amt": 67.50},
    {"date": "01 OCT", "desc": "STUDIO7-CENTRAL 001/010", "amt": 549.0},
    {"date": "05 OCT", "desc": "PAYMENT THANK YOU - UOBT", "amt": -5000.0}
]

summary = parse_transactions(transactions)
print(f"Net Amount: {summary.net_billed_amount:,.2f} THB")
print(f"Categories: {summary.categories}")
```

---

## 📁 Repository Structure

```text
card-statement-analyzer/
├── SKILL.md                          # Antigravity Skill definition & runbook
├── card_statement_analyzer/          # Core Python package
│   ├── __init__.py
│   ├── models.py                     # Dataclasses & types
│   ├── categorizer.py                # Thai merchant taxonomy & regex rules
│   ├── parser.py                     # Parsing & reconciliation engine
│   └── cli.py                        # Terminal CLI entry point
├── scripts/
│   └── parse_statement.py            # Standalone runner script
├── references/
│   └── thai_merchants.md             # Thai merchant abbreviations & bank format guide
├── tests/
│   └── test_parser.py                # Automated unit tests
├── pyproject.toml                    # Package build configuration
└── LICENSE                           # MIT License
```

---

## 🧪 Testing

Run the test suite using Python's built-in `unittest`:

```bash
python3 -m unittest discover -s tests
```

---

## 🛡️ Security & Privacy Guarantee

Credit card statements contain sensitive financial data. This project is intentionally built with:
- Zero telemetry or network tracking.
- Strict `.gitignore` rules preventing `.pdf`, `.csv`, and personal exports from ever being committed.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
