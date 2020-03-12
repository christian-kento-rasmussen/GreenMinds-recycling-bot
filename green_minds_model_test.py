import os
import sys
import unittest
from PIL import Image
from green_minds_model import GreenMindsModel


class TestGreenMindsModel(unittest.TestCase):

    def test_model_load(self):
        """
            Loads a PyTorch model from a path
        """
        green_minds_model = GreenMindsModel(os.path.join(sys.path[0], "assets/model/checkpoint.pth"))
        self.assertTrue(True)

    def test_model_inference(self):
        """
            Tests that the loaded PyTorch model runs inference correctly
        """
        green_minds_model = GreenMindsModel(os.path.join(sys.path[0], "assets/model/checkpoint.pth"))
        self.assertEqual(green_minds_model.predict(Image.open(os.path.join(sys.path[0], "assets/waterbottle_test_image.jpg")), topk=1)[1][0], "WaterBottle")


if __name__ == '__main__':
    unittest.main()
