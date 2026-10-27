import sys
import json
import argparse
from .parser import parse_transactions

def format_markdown(summary) -> str:
    lines = []
    lines.append("# 📊 Credit Card Statement Analysis")
    lines.append(f"**Total Transactions:** {summary.total_transactions} | **Net Total:** {summary.net_billed_amount:,.2f} THB")
    lines.append("")
    lines.append("### 1. Category Summary")
    lines.append("| Category | Count | Total (THB) | Notes |")
    lines.append("| :--- | :---: | :---: | :--- |")
    
    for cat, data in sorted(summary.categories.items(), key=lambda x: x[1]["total"], reverse=True):
        lines.append(f"| {cat} | {data['count']} | {data['total']:,.2f} | - |")
        
    lines.append(f"| **Net Billed Amount** | **{summary.total_transactions}** | **{summary.net_billed_amount:,.2f}** | - |")
    lines.append("")
    
    if summary.micro_spending_velocity:
        lines.append("### 2. Micro-Spending Velocity (High Frequency)")
        for v in summary.micro_spending_velocity:
            lines.append(f"- **{v.vendor}:** {v.count} visits | Total: `{v.total_amount:,.2f} THB` | Avg: `{v.avg_ticket_size:,.2f} THB/visit`")
        lines.append("")
        
    if summary.big_tickets:
        lines.append("### 3. Big Ticket Outliers (>= 5,000 THB)")
        for tx in summary.big_tickets:
            lines.append(f"- `{tx.trans_date}` — **{tx.description}**: `{tx.amount:,.2f} THB` ⚠️ *(Check 0% installment conversion)*")
        lines.append("")
        
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Analyze Thai credit card statement transactions.")
    parser.add_argument("input_file", help="Path to JSON file containing parsed transactions array.")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of Markdown.")
    
    args = parser.parse_args()
    
    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        summary = parse_transactions(data)
        
        if args.json:
            out = {
                "total_transactions": summary.total_transactions,
                "total_debits": summary.total_debits,
                "total_credits": summary.total_credits,
                "net_billed_amount": summary.net_billed_amount,
                "categories": summary.categories,
                "micro_spending_velocity": [
                    {"vendor": v.vendor, "count": v.count, "total": v.total_amount, "avg": v.avg_ticket_size}
                    for v in summary.micro_spending_velocity
                ],
                "big_tickets": [
                    {"date": t.trans_date, "desc": t.description, "amt": t.amount}
                    for t in summary.big_tickets
                ]
            }
            print(json.dumps(out, indent=2, ensure_ascii=False))
        else:
            print(format_markdown(summary))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
