import unittest
import machineLearning.model as model
from machineLearning.model import MATRIX_DIM
from numpy.testing import assert_allclose
import numpy as np

BAD_THRESHOLD = 0.8
GOOD_THRESHOLD = 0.2

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
        rez = model._predict_badness(matrix)
        self.assertEqual(len(rez), 100)

    def testLongLine(self):
        matrix = [[240, 229, 251, 262, 277, 262, 282, 299, 269, 253, 260, 267, 291, 243, 283, 266, 249, 252, 274, 282, 240, 248, 253, 254, 252, 253, 242, 252, 244, 236, 267, 228, 218, 240, 254, 237, 213, 234, 253, 256, 240, 236, 241, 203, 241, 222, 244, 254, 185, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 250, 244, 240, 252, 254, 247, 260, 256, 288, 245, 263, 276, 277, 288, 254, 253, 262, 264, 251, 261, 267, 245, 277, 229, 258, 242, 256, 239, 260, 251, 250, 247, 219, 202, 250, 245, 194, 220, 216, 230, 256, 230, 237, 223, 218, 246, 231, 243, 232, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 243, 231, 213, 0, 1, 240, 287, 277, 252, 244, 296, 246, 254, 255, 264, 239, 247, 249, 258, 253, 251, 245, 257, 242, 274, 204, 260, 255, 252, 235, 264, 215, 229, 232, 227, 235, 223, 202, 240, 241, 221, 231, 243, 198, 244, 236, 228, 223, 183, -1, -1, -1, -1, -1,-1, -1, -1, -1, -1, -1, 204, 196, 250, 254, 237, 236, 253, 279, 230, 246, 283, 258, 286, 272, 263, 255, 251, 241, 273, 248, 270, 246, 235, 258, 249, 230, 231, 251, 241, 243, 232, 220, 210, 228, 229, 201, 222, 244, 213, 231, 238, 219, 237, 232, 222, 237, 217, 196, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 123, 131, 134, 145, 136, 151, 144, 168, 175, 167, 190, 164, 177, 202, 194, 206, 235, 0, 0, 243, 253, 249, 234, 273, 240, 260, 264, 274, 333, 474, 314, 247, 239, 230, 244, 217, 214, 220, 209, 189, 158, 188, 173, 185, 158, 149, 177, 172, 140, 140, 140, 146, 145, 133, 113, 104, 98, -1, -1, 102, 125, 124, 135, 128, 146, 153, 177, 175, 181, 157, 166, 167, 199, 198, 198, 229, 219, 226, 235, 229, 235, 242, 243, 248, 280, 254, 267, 243, 281, 260, 279, 233, 228, 221, 227, 202, 250, 204, 222, 184, 173, 181, 170, 181, 157, 167, 175, 174, 137, 161, 137, 134, 131, 116, 119, 107, -1, -1, 117, 116, 127, 141, 133, 160, 185, 146, 186, 171, 166, 161, 180, 181, 200, 229, 215, 228, 236, 222, 217, 252, 260, 262, 244, 251, 269, 259, 257, 269, 277, 233, 219, 238, 203, 217, 183, 237, 188, 193, 178, 182, 165, 177, 178, 177, 167, 169, 144, 134, 159, 120, 134, 138, 107, 105, 102, -1, -1, -1, 118, 102, 122, 137, 154, 169, 137, 166, 176, 171, 171, 177, 195, 182, 198, 206, 213, 232, 257, 234, 207, 248, 254, 246, 269, 256, 261, 255, 259, 281, 257, 225, 246, 210, 234, 215, 226, 191, 205, 191, 188, 173, 146, 187, 198, 175, 185, 155, 142, 147, 138, 119, 117, 125, 84, 107, -1, -1, 185, 190, 186, 226, 212, 214, 215, 243, 236, 224, 240, 229, 258, 199, 215, 252, 216, 233, 218, 226, 227, 246, 211,222, 222, 198, 228, 205, 225, 208, 197, 189, 186, 207, 227, 206, 197, 211, 219, 229, 200, 203, 201, 205, 176, 187, 180, 194, 183, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 215, 195, 172, 217, 208, 206, 224, 209, 240, 207, 261, 230, 232, 225, 194, 225, 236, 203, 205, 235, 230, 243, 250, 221, 234, 180, 213, 242, 237, 205, 223, 180, 203, 5, 214, 219, 187, 223, 210, 188, 209, 188, 198, 213, 190, 180, 166, 180, 162, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 204, 223, 188, 207, 221, 227, 198, 213, 238, 211, 230, 258, 245, 210, 217, 254, 200, 217, 241, 232, 213, 258, 219, 235, 207, 0, 203, 211, 206, 208, 189, 183, 225, 201, 211, 218, 188, 215, 243, 201, 187, 186, 184, 212, 177, 154, 172, 186, 162, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 194, 164, 174, 193, 208, 220, 217, 219, 196, 236, 260, 246, 236, 194, 222, 236, 219, 248, 212, 238, 206, 218, 228, 240, 192, 222, 229, 203, 186, 176, 168, 200, 216, 222, 226, 199, 195, 222, 211, 175, 187, 241, 178, 186, 164, 179, 191, 190, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
        rez = model.get_network_score(matrix)
        self.assertEqual(len(rez), 1)
    
    def testKnowMinimumGood(self):
        matrix = [[0,0]]
        rez = model.get_network_score(matrix)
        self.assertLess(rez[0], GOOD_THRESHOLD)
    
    def testKnownMaximumGood(self):
        matrix = [[1,1]]
        rez = model.get_network_score(matrix)
        self.assertLess(rez[0], GOOD_THRESHOLD)
        
    def testKnownOrdersGood(self):
        matrix = [[1,1],[0,0],[1,0],[0,1]]
        rez = model.get_network_score(matrix)
        self.assertLess(rez[0], GOOD_THRESHOLD)
        self.assertLess(rez[1], GOOD_THRESHOLD)
        self.assertGreater(rez[2], BAD_THRESHOLD)
        self.assertGreater(rez[3], BAD_THRESHOLD)
    
    def testLinearBad(self):
        matrix = [[5,4,3,2,1,0]]
        
        rez = model.get_network_score(matrix)
        self.assertGreater(rez[0], BAD_THRESHOLD)
    
    def testDipBad(self):
        matrix = [[1,0,1]]
        rez = model.get_network_score(matrix)
        self.assertGreater(rez[0], BAD_THRESHOLD)
    
    def testMountain(self):
        matrix = [[0,1,0]]
        rez = model.get_network_score(matrix)
        self.assertGreater(rez[0], BAD_THRESHOLD)
        
    def test2DMatrix(self):
        matrix = [[ i*a for i in range(MATRIX_DIM)] for a in range(88)]
        rez =  model.get_network_score(matrix)
        self.assertEqual(len(rez), 88)

    def testSaliencyConstant(self):
        matrix = [[5,4,3,2,1,0], [5,4,3,2,1,0]]
        rez =  model.get_saliency_map(matrix)
        np.testing.assert_array_almost_equal(rez[1],rez[0])

    
    def testSaliencyNegative(self):
        matrix = [[-1,-1,-1,-1]]
        rez =  model.get_saliency_map(matrix)
        np.testing.assert_array_almost_equal(matrix,rez)