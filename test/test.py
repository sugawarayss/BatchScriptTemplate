import sys
import os
import unittest

app_home = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(os.path.join(app_home, "lib"))
from models.my_model import MyModel


class TestMyModel(unittest.TestCase):
    def test_get_hoge(self):
        ml = MyModel()
        self.assertEqual("hoge", ml.get_hoge())


if __name__ == "__main__":
    unittest.main()