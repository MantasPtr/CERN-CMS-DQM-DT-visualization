import unittest
import machineLearning.eval
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

    def testPrediction(self):
        matrix = np.random.rand(100,47)
        rez = machineLearning.eval.predict(matrix)
        self.assertEqual(len(rez), 100)