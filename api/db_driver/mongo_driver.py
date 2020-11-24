from pymongo import MongoClient

class MongoDriver:

    def __init__(self,db):
        self.myclient = MongoClient(host = ["localhost:27017"])
        self.myclient.server_info()
        self.mydb = self.myclient[db]

    def set_database(self,db):
        try:
            self.mydb = self.myclient[db]
            return 1

        except IndexError as e:
            print(e)
            return 0

    def get_main_graph(self):

        try:

            dblist = self.myclient.list_database_names()
            
            if "mate" in dblist:
            
                mycol = self.mydb["graphs"]

                graph = {"graph_id":"mainGraph"}
                


                return mycol.find(graph,{'_id':0})[0]

        except IndexError as e:
            print(e)        
            return 0

    def get_user(self, user):
        try:

            dblist = self.myclient.list_database_names()
            
            if "mate" in dblist:
            
                mycol = self.mydb["users"]

                graph = {"graph_id":user}

                return mycol.find(graph,{'_id':0})[0]

        except IndexError as e:
            print(e)        
            return False

    def create_user(self, data):

        try:
            mycol = self.mydb["users"]
            data = mycol.insert_one(data)
            return True
            
        except IndexError as e:
            print(e)        
            return False



mongo_driver = MongoDriver("mate")

print(mongo_driver.get_user('user'))