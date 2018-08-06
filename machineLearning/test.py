import unittest
import machineLearning.transform
from numpy.testing import assert_allclose
import numpy as np
class MongoCrudTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def testEmpty(self):
        matrix = []
        rez = machineLearning.transform.processMatrix(matrix)
        assert_allclose(rez,matrix)

    def testSquare(self):
        matrix = [[1,2],[1,3]]
        rez = machineLearning.transform.processMatrix(matrix)
        assert_allclose(rez, np.array(matrix))

    def testResizing(self):
        matrix = [[1,1,1,1],[1,1,1],[1,1]]
        rez = machineLearning.transform.processMatrix(matrix)
        for x in rez:
            self.assertEqual(len(x), 2)


    def testNothing(self):
        matrix = [[1,123,777], [6,1,6,1,6,1], [1,2,3]]
        rez = machineLearning.transform.processMatrix(matrix)
        print(" rez:", rez)