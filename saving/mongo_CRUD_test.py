import unittest
from saving.mongoWrapper import MongoDbFactory
import time

class MongoCrudTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.dbWrapper = MongoDbFactory('crud_test').getMongoCollectionWrapper('test_collection')
        cls.dbWrapper.dropCollection()

    def setUp(self):
        pass
    
    def tearDown(self):
        self.dbWrapper.deleteAll()
        self.dbWrapper.dropIndexes()

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

    def test_projection(self):
        saveObject = {"a":"d","c":"d"}
       
        self.dbWrapper.save(saveObject)
        retrivedObject = self.dbWrapper.find({},{"c":1})[0]
        self.assertEqual(retrivedObject.get("c"), saveObject.get("c"))
        self.assertEqual(retrivedObject.get("a"), None)

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

    def test_create_drop_Index(self):
        self.dbWrapper.createIndex("a", "a_index")
        self.dbWrapper.collection.drop_index("a_index")

    @unittest.skip
    def test_without_index(self):
        print("---Test without index---")
        start = time.time()
        saveObjects = [ {"a": x*x, "b": x } for x in range(1000000) ]
        start = self.lapTime(start ,"Created in: ")
        self.dbWrapper.saveAll(saveObjects)
        start = self.lapTime(start ,"Saved in: ")
        result = self.dbWrapper.find({"a": {"$gt": 1000000}})
        start = self.lapTime(start ,"Queried >1000000 in: " )
        result = self.dbWrapper.findOne({"a": 2418025})
        start = self.lapTime(start, "Queried =2418025 in: ")
    
    @unittest.skip
    def test_index(self):
        print("---Test with index---")
        start = time.time()
        self.dbWrapper.createIndex("a", "a_index")
        start = self.lapTime(start ,"Created index in:")
        saveObjects = [ {"a": x*x, "b": x } for x in range(1000000)]
        start = self.lapTime(start ,"Created data in: ")
        self.dbWrapper.saveAll(saveObjects)
        start = self.lapTime(start ,"Saved in: ")
        result = self.dbWrapper.find({"a": {"$gt": 1000000}})
        start = self.lapTime(start ,"Queried >1000000 in: " )
        result = self.dbWrapper.findOne({"a": 2418025})
        start = self.lapTime(start, "Queried =2418025 in: ")
        self.dbWrapper.dropIndex("a_index")
    
    
    @staticmethod
    def lapTime(oldTime, message):
        print("%s %.8f" % (message, (time.time() - oldTime)))
        return time.time()


    def __assertDict(self, oldDict:dict, newDict: dict):
        for key in oldDict.keys():
            self.assertEqual(oldDict.get(key), newDict.get(key), ("cannot find matching value for key" + str(key)))
