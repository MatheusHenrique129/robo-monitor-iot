from typing import Optional
from fastapi import HTTPException
from src.models.ClimateDataModel import ClimateDataModel
from src.db.mongodb.Connection import DBConnectionHandler
from src.repositories.LocalStorageRepository import LocalStorageRepository

db_handle = DBConnectionHandler()
db_handle.connect_db()
conn = db_handle.get_connect_db()

class ClimateService:
    async def find_all(start: Optional[str] = None, end: Optional[str] = None):
        reposirory = LocalStorageRepository(conn)
        res = reposirory.select_all(start, end)
        return res
    
    async def find_status():
        reposirory = LocalStorageRepository(conn)
        res = reposirory.select_last()
        return res

    async def save(data: ClimateDataModel):
        try:
            reposirory = LocalStorageRepository(conn)

            body = {
                "humidity": data.humidity,
                "temperature": data.temperature,
                "collection_time": data.collection_time,
                "network_reconnect": data.network_reconnect,
                "network_disconnect": data.network_disconnect
            }
            print(body)

            reposirory.insert(body)
            return "success"

        except HTTPException as error:
            raise HTTPException(400, detail=str(error))


