import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"obsidian"))
from eden import evaluate_event, answer

class EdenPolicyTests(unittest.TestCase):
    def test_unauthorized_block(self):
        self.assertEqual(evaluate_event("usb", False, 0).action,"BLOCK")
    def test_high_severity_review(self):
        self.assertEqual(evaluate_event("network", True, 8).action,"REVIEW")
    def test_low_severity_allow(self):
        self.assertEqual(evaluate_event("network", True, 1).action,"ALLOW")
    def test_no_fake_inference(self):
        self.assertIn("not configured",answer("hello"))
if __name__=="__main__":
    unittest.main()
