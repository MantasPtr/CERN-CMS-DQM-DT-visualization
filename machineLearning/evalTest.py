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

    def testNothing(self):
        matrix = np.random.rand(100,10)
        rez = machineLearning.eval.predict(matrix)
        print(rez)