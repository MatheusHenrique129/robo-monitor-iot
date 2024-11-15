from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi

class DBConnectionHandler: 
    def __init__(self) -> None:
        self.__url_connection = "mongodb+srv://mhsantos:gwYncyWRLuzFCK3I@robo-monitor-iot.bf2yj.mongodb.net/?retryWrites=true&w=majority&appName=db-robo-monitor-iot"
        self.__client = None
        self.__db_connection = None

    def connect_db(self): 
        try:
            self.__client = MongoClient(self.__url_connection, server_api=ServerApi('1'))
            self.__db_connection = self.__client["db-robo-monitor-iot"]
            print("Conexão estabelecida com sucesso.")
        except errors.ConnectionFailure as e:
            print(f"Falha na conexão com o MongoDB: {e}")
        except errors.ConfigurationError as e:
            print(f"Erro de configuração: {e}")
        except Exception as e:
            print(f"Ocorreu um erro ao tentar conectar ao MongoDB: {e}")

    def get_connect_db(self):
        return self.__db_connection
    
    def get_client_db(self):
        return self.__client
    
    def close_connection(self):
        try:
            if self.__client:
                self.__client.close()
        except Exception as e:
            print(f"Ocorreu um erro ao tentar fechar a conexão: {e}")