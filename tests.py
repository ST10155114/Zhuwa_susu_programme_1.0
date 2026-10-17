import unittest
from decimal import Decimal
from Zhuwa_susu_programme_1 import SusuGroup

class TestSusuGroup(unittest.TestCase):

    def test_invalid_weekly_contribution(self):
        with self.assertRaises(ValueError):
            SusuGroup("TestGroup", 0)

    def test_add_member_and_duplicates(self):
        group = SusuGroup("TestGroup", 50)
        res1 = group.add_member("Alice", "A1")
        res2 = group.add_member("Alice Duplicate", "A1")
        self.assertIn("Success", res1)
        self.assertIn("Error", res2)

    def test_record_contribution_overpayment(self):
        group = SusuGroup("TestGroup", 50)
        group.add_member("Bob", "B1")
        group.record_contribution("B1", 1, 30)
        res = group.record_contribution("B1", 1, 30)
        self.assertIn("Error", res)

    def test_close_week_fails_with_partial_payment(self):
        group = SusuGroup("TestGroup", 50)
        group.add_member("Charlie", "C1")
        group.add_member("Diana", "D2")
        group.record_contribution("C1", 1, 50)
        group.record_contribution("D2", 1, 20)
        result = group.close_week()
        self.assertIn("could not be closed", result)
        self.assertIn("Diana", result)
        self.assertEqual(group.current_week, 1)

    def test_close_week_success_and_payout(self):
        group = SusuGroup("TestGroup", 50)
        group.add_member("Charlie", "C1")
        group.add_member("Diana", "D2")
        group.record_contribution("C1", 1, 50)
        group.record_contribution("D2", 1, 50)
        result = group.close_week()
        self.assertIn("closed!", result)
        self.assertIn("Charlie", result)
        self.assertEqual(group.current_week, 2)
        self.assertEqual(len(group.payout_history), 1)

    def test_add_member_after_week_started(self):
        group = SusuGroup("TestGroup", 50)
        group.add_member("Charlie", "C1")
        group.record_contribution("C1", 1, 50)
        group.close_week()
        res = group.add_member("NewGuy", "N1")
        self.assertIn("Error", res)

    def test_record_negative_or_zero_contribution(self):
        group = SusuGroup("TestGroup", 50)
        group.add_member("Alice", "A1")
        res_zero = group.record_contribution("A1", 1, 0)
        res_neg = group.record_contribution("A1", 1, -10)
        self.assertIn("Error", res_zero)
        self.assertIn("Error", res_neg)

    def test_record_unknown_member(self):
        group = SusuGroup("TestGroup", 50)
        res = group.record_contribution("UNKNOWN", 1, 50)
        self.assertIn("Error", res)

    def test_record_future_week(self):
        group = SusuGroup("TestGroup", 50)
        group.add_member("Alice", "A1")
        res = group.record_contribution("A1", 5, 50)
        self.assertIn("Error", res)

    def test_multiple_week_payout_rotation(self):
        group = SusuGroup("TestGroup", 50)
        group.add_member("Alice", "A1")
        group.add_member("Bob", "B1")
        
        group.record_contribution("A1", 1, 50)
        group.record_contribution("B1", 1, 50)
        group.close_week()
        
        self.assertEqual(group.payout_history[0]["recipient"], "Alice")
        self.assertEqual(group.current_week, 2)
        
        group.record_contribution("A1", 2, 50)
        group.record_contribution("B1", 2, 50)
        group.close_week()
        
        self.assertEqual(group.payout_history[1]["recipient"], "Bob")
        self.assertEqual(group.current_week, 3)

if __name__ == "__main__":
    unittest.main()