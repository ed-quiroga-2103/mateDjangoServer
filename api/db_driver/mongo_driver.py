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

                query = user
                #Query: Datos del request, Ejm:{'user':'admin@email.com'}
                #Segundo parametro: Exclusion de la columna de id
                #[0]: Primer elemento de la lista, debería ser el único.
                result = mycol.find(query,{'_id':0})[0]

                return result

        except IndexError as e:
            print("ERROR")
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

    def get_user_level(self, user):
        
        param = {"user":user["user"], "pass": user["pass"]}

        userData = self.get_user(param)

        return userData['data']






mongo_driver = MongoDriver("mate")
