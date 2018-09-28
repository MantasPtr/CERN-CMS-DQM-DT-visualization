import unittest
import machineLearning.transform
from machineLearning.model import MATRIX_DIM
from numpy.testing import assert_allclose
import utils.numpyUtils as npUtils
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
        rez = machineLearning.transform.resizeMatrix(matrix, MATRIX_DIM)
        assert_allclose(rez,matrix)

    def testResizing(self):
        matrix = [[240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253]]
        rez = machineLearning.transform.resizeMatrix(matrix, MATRIX_DIM)
        for x in rez:
            self.assertEqual(len(x), MATRIX_DIM)

    def testNegativeDeletion(self):
        matrix = [[-1,0,1,2,-10,3,4,5,-1]]
        rez = machineLearning.transform.remove_negatives(matrix)
        self.assertListEqual(rez, [[0,1,2,3,4,5]])

    def testScaling(self):
        matrix = [np.array([-1,0,1]),np.array([-2,-1,0]),np.array([-5,0,10]),np.array([1,10,100])]
        rez = machineLearning.transform.scaleMatrix(matrix)
        self.assertListEqual(npUtils.to_python_matrix(rez), [[-1,0,1],[-1,-0.5,0],[-0.5,0,1],[0.01,0.1,1] ])