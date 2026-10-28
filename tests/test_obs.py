import json
import pathlib
import tempfile
import unittest
import sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"tools"))
from obs import manifest, build

class PackageTests(unittest.TestCase):
    def test_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp)
            (root/"main.py").write_text("print(1)")
            (root/"obs.json").write_text(json.dumps({"id":"org.test.demo","name":"Demo","version":"1.0","entry":"main.py"}))
            self.assertEqual(manifest(root)["name"],"Demo")
    def test_reject_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp)
            (root/"obs.json").write_text(json.dumps({"id":"org.test.demo","name":"Demo","version":"1.0","entry":"../main.py"}))
            with self.assertRaises(ValueError):manifest(root)
if __name__=="__main__":unittest.main()
