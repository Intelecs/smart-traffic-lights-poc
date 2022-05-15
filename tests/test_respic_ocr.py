import unittest
from inference.respic.respic_detect_ocr import plate_ocr

class TestRespicOCR(unittest.TestCase):

    model_path = "models/respik.pt"
    image_path = "images/27.jpeg"

    def test_ocr(self):
        plate_ocr(self.image_path, self.model_path)