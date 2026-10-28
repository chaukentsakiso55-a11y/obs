import pathlib
import sys
import tempfile
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"obsidian"))
from eden_runtime import EdenRuntime
from security_events import check_path,event_record,append_audit

class RuntimeTests(unittest.TestCase):
    def test_reject_external_endpoint(self):
        with self.assertRaises(ValueError): EdenRuntime(endpoint="http://example.com")
    def test_blank_message(self):
        r=EdenRuntime().chat("  ")
        self.assertFalse(r.available)
    def test_oversized_message(self):
        r=EdenRuntime().chat("a"*12001)
        self.assertFalse(r.available)
    def test_security_triage(self):
        self.assertEqual(event_record("usb","unknown device",False,9)["decision"],"BLOCK")
    def test_file_inspection(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(check_path(d)["exists"])
    def test_audit(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/"audit.jsonl"
            append_audit(p,event_record("file","test",True,1))
            self.assertIn('"decision": "ALLOW"',p.read_text())
if __name__=="__main__":unittest.main()
