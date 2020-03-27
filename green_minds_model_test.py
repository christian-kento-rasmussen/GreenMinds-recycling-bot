import os
import sys
import unittest
from PIL import Image
from green_minds_model import GreenMindsModel


class TestGreenMindsModel(unittest.TestCase):
    """Runs tests for the GreenMindsModel.py class
    """

    def test_model_load(self):
        """
            Loads a PyTorch model from a path
        """
        green_minds_model = GreenMindsModel(os.path.join(sys.path[0], "assets/model/checkpoint.pth"))
        self.assertIsNot(green_minds_model, None)

    def test_model_inference(self):
        """
            Tests that the loaded PyTorch model runs inference correctly
        """
        green_minds_model = GreenMindsModel(os.path.join(sys.path[0], "assets/model/checkpoint.pth"))
        self.assertEqual(green_minds_model.predict(Image.open(os.path.join(sys.path[0], "assets/test_image_grassmilk.jpg")), topk=1)[1][0], "carton-grassmilk")


if __name__ == '__main__':
    unittest.main()
