import unittest
import machineLearning.transform
from numpy.testing import assert_allclose
import numpy as np
class NetTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def testEmpty(self):
        matrix = []
        rez = machineLearning.transform.resizeMatrix(matrix)
        assert_allclose(rez,matrix)

    def testResizing(self):
        matrix = [[240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253]]
        rez = machineLearning.transform.resizeMatrix(matrix)
        for x in rez:
            self.assertEqual(len(x), 47)