from datetime import datetime
from typing import Dict, List, Optional
from pymongo.errors import PyMongoError

class LocalStorageRepository:
    def __init__(self, db_connection) -> None:
        self.__collection_name = "data_storage"
        self.__db_connection = db_connection

    def parse_date(self, date_str: str) -> Optional[datetime]:
        date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"]
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue 
        return None 
    
    def insert(self, data: Dict) -> Dict:
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.insert_one(data)
        return data
    
    def insert_all(self, list_data: List[Dict]) -> List[Dict]:
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.insert_many(list_data)
        return list_data 
    
    def select_all(self, start: Optional[str] = None, end: Optional[str] = None) -> List[Dict]:
        try:
            collection = self.__db_connection.get_collection(self.__collection_name)
           
            filter = {}
            if start:
                start_date = self.parse_date(start)
                filter["network_reconnect"] = {"$gte": start_date}

            if end:
                end_date = self.parse_date(end)
                filter["network_disconnect"] = {"$lte": end_date}
            
            data = collection.find(filter)

            response = []
            for elem in data:
                elem["_id"] = str(elem["_id"])
                elem["humidity"] = round(elem["humidity"], 2)
                elem["temperature"] = round(elem["temperature"], 2)

                response.append(elem)
            
            return response
        except PyMongoError as e:
            return f"Ocorreu um erro durante o select all: {e}"
        
    def select_last(self) -> Optional[Dict]:
        try:
            collection = self.__db_connection.get_collection(self.__collection_name)
            data = collection.find_one(sort=[("collection_time", -1)])

            if data:
                data["_id"] = str(data["_id"])
                data["humidity"] = round(data["humidity"], 2)
                data["temperature"] = round(data["temperature"], 2)

            print(data)
            return data
        except PyMongoError as e:
            print(f"Ocorreu um erro durante o select_last: {e}")
            return None

