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

    def get_graph_info(self):

        try:

            dblist = self.myclient.list_database_names()
            
            if "mate" in dblist:
            
                mycol = self.mydb["graphs"]

                graph = {"graph_id":"info"}
                


                return mycol.find(graph,{'_id':0})[0]

        except IndexError as e:
            print(e)        
            return 0

    def get_topic_graph(self, id):
        try:

            dblist = self.myclient.list_database_names()
            
            if "mate" in dblist:
            
                mycol = self.mydb["graphs"]

                graph = {"graph_id": str(id)}
                


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


        data['progress'] = {'0':{'0':1,'2':1,'completed':0,'inProgress':1}}

        try:
            mycol = self.mydb["users"]
            mycol.insert_one(data)
            return data
            
        except IndexError as e:
            print(e)        
            return False

    def get_user_level(self, user):
        
        param = {"user":user["user"], "pass": user["pass"]}

        user_data = self.get_user(param)

        return user_data['progress']

    def create_exercise(self, data):

        try:
            mycol = self.mydb["exercises"]
            data = mycol.insert_one(data)
            return True

        except IndexError as e:
            print(e)        
            return False

    def get_exercise(self, params):
        #params representa los parametros con los que se va a filtrar el contenido.
        #Estos deben ser, por ejemplo, el tema del ejercicio o el nombre del curso.

        try:

            dblist = self.myclient.list_database_names()
            if "mate" in dblist:
            
                mycol = self.mydb["exercises"]

                query = params
                
                #Segundo parametro: Exclusion de la columna de id
                #result contiene todos los posibles ejercicios que cumplan con estos parametros de busqueda
                result = list(mycol.find(query,{'_id':0}))

                return result

        except IndexError as e:
            print("ERROR")
            print(e)        
            return False      

    def update_progress(self, params, user):

        filter = {'user': user}

        progress = { "$set": {'progress':params}}

        try:
            
            mycol = self.mydb["users"]
            
            mycol.update_one(filter, progress)

            return True

        except IndexError as e:
            print(e)
            return False
