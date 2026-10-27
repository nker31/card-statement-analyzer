import unittest
from card_statement_analyzer import parse_transactions, classify

class TestCardStatementAnalyzer(unittest.TestCase):
    def test_classify_installments(self):
        cat, is_inst, _ = classify("STUDIO7-CENTRAL LADPRAO 001/010", 549.0)
        self.assertEqual(cat, "Active 0% Installments")
        self.assertTrue(is_inst)

        cat2, is_inst2, _ = classify("2C2P *ASICS BANGKOK 002/003", 884.0)
        self.assertEqual(cat2, "Active 0% Installments")
        self.assertTrue(is_inst2)

    def test_classify_merchants(self):
        self.assertEqual(classify("TMN 7-11 BANGKOK", 100.0)[0], "Groceries & Convenience")
        self.assertEqual(classify("MINI BIG C -AIRBUS HOT", 64.0)[0], "Groceries & Convenience")
        self.assertEqual(classify("BTS VISIONARY PARK", 67.5)[0], "Transport & Commute")
        self.assertEqual(classify("WWW.2C2P.COM*JETTS FIT", 1450.0)[0], "Fitness & Wellness")
        self.assertEqual(classify("FITWHEY BANGKOK", 675.0)[0], "Fitness & Wellness")
        self.assertEqual(classify("OHKAJHU-ONE BANGKOK", 303.0)[0], "Food & Dining")
        self.assertEqual(classify("Spotify Stockholm SE", 249.0)[0], "Subscriptions & Bills")

    def test_reconciliation_and_velocity(self):
        data = [
            {"date": "14 SEP", "desc": "TMN 7-11 BANGKOK", "amt": 50.0},
            {"date": "15 SEP", "desc": "TMN 7-11 BANGKOK", "amt": 50.0},
            {"date": "16 SEP", "desc": "TMN 7-11 BANGKOK", "amt": 50.0},
            {"date": "03 OCT", "desc": "CENTRAL DEPT.(LADPHRO)", "amt": 26624.0},
            {"date": "05 OCT", "desc": "PAYMENT THANK YOU - UOBT", "amt": -5000.0}
        ]
        summary = parse_transactions(data)
        self.assertEqual(summary.total_transactions, 5)
        self.assertEqual(summary.total_debits, 26774.0)
        self.assertEqual(summary.total_credits, 5000.0)
        self.assertEqual(summary.net_billed_amount, 21774.0)
        
        # Verify 7-Eleven micro-spending velocity
        self.assertEqual(len(summary.micro_spending_velocity), 1)
        self.assertEqual(summary.micro_spending_velocity[0].vendor, "TMN 7-11")
        self.assertEqual(summary.micro_spending_velocity[0].count, 3)
        self.assertEqual(summary.micro_spending_velocity[0].avg_ticket_size, 50.0)

        # Verify Big Ticket (> 5,000 THB)
        self.assertEqual(len(summary.big_tickets), 1)
        self.assertEqual(summary.big_tickets[0].description, "CENTRAL DEPT.(LADPHRO)")

if __name__ == "__main__":
    unittest.main()
