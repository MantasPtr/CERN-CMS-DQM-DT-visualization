import unittest
from saving.mongoWrapper import MongoDbFactory

class MongoCrudTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.mongoDbWrapper = MongoDbFactory('crud_test').getMongoCollectionWrapper('test_collection')

    def setUp(self):
        pass
    
    def tearDown(self):
        self.mongoDbWrapper.deleteAll()

    def test_saveOneAndFindOne(self):
        saveObject = {"a":"b","c":"d"}

        self.mongoDbWrapper.save(saveObject)
        retrivedObject = self.mongoDbWrapper.findOne()

        self.__assertDict(saveObject, retrivedObject)

    def __assertDict(self, oldDict:dict, newDict: dict):
        for key in oldDict.keys():
            self.assertEqual(newDict[key], oldDict[key], "cannot find matching value for key" + str(key))
