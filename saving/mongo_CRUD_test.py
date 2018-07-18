import unittest
from saving.mongoWrapper import MongoDbFactory

class MongoCrudTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.dbWrapper = MongoDbFactory('crud_test').getMongoCollectionWrapper('test_collection')

    def setUp(self):
        pass
    
    def tearDown(self):
        self.dbWrapper.deleteAll()

    def test_saveId(self):
        saveObject = {}
        self.dbWrapper.save(saveObject)
        self.assertNotEqual(saveObject.get("_id"), None, "Saved object does not have id")

    def test_saveOneAndFindOne(self):
        saveObject = {"a":"b","c":"d"}

        self.dbWrapper.save(saveObject)
        retrivedObject = self.dbWrapper.findOne()

        self.__assertDict(saveObject, retrivedObject)

    def test_saveFewAndFindOne(self):
        saveObject0 = {"a":"d","c":"d"}
        saveObject1 = {"b":"d","c":"d"}
        saveObject2 = {"a":"e","c":"f"}

        self.dbWrapper.saveAll([saveObject0, saveObject1, saveObject2])
        retrivedObject = self.dbWrapper.find({"a":"e"})[0]
        
        self.__assertDict(saveObject2, retrivedObject)

    def test_count(self):
        
        saveObject0 = {"a":"d","c":"d"}
        saveObject1 = {"b":"d","c":"f"}
        saveObject2 = {"b":"d","c":"d"}
        saveObject3 = {"b":"d","c":"d"}

        self.dbWrapper.saveAll([saveObject0, saveObject1, saveObject2, saveObject3])
        
        self.assertEqual(self.dbWrapper.count({"a":"d"}), 1)
        self.assertEqual(self.dbWrapper.count({"c":"d"}), 3)
        self.assertEqual(self.dbWrapper.count({"c":"a"}), 0)
        self.assertEqual(self.dbWrapper.count({"b":"d"}), 3)
        self.assertEqual(self.dbWrapper.count({}), 4)
        self.assertEqual(self.dbWrapper.count({"b":"d","c":"d"}), 2)
        self.assertEqual(self.dbWrapper.count(saveObject2), 1)
        self.assertEqual(self.dbWrapper.count({"b":"d","c":"d","d":"d"}), 0)


    def __assertDict(self, oldDict:dict, newDict: dict):
        for key in oldDict.keys():
            self.assertEqual(newDict[key], oldDict[key], "cannot find matching value for key" + str(key))
