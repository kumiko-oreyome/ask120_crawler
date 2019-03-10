from pymongo import MongoClient
from pymongo.collection import Collection


class MongoConnector():
    def __init__(self,host,username,password,db_name):
        self.uri = "mongodb://%s:%s@%s/%s"%(username,password,host,db_name)
        self.conn = MongoClient(host)
        self.db = self.conn[db_name]

    def create_collect(self,collect_name):
         self.db.create_collection(collect_name)

    def get_collect(self,collect_name):
        return self.db[collect_name]
    
#class Ask120Repsitory():
#    def __init__(self,conn):
#        self.conn = conn
        
    


#uri = "mongodb://uabharuhi:jojo1234@192.168.99.101:27017/ask123"
host = '192.168.99.101'
client = MongoClient(host)
#client.ask123.authenticate("uabharuhi", "jojo1234")
#client.ask123.authenticate("uabharuhi", "jojo1234", mechanism='MONGODB-CR')
db = client['ask123']
collect = db['faq']
print(collect)
print(list(collect.find()))