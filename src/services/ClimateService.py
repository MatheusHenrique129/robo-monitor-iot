import io
import pandas as pd
from typing import Optional, List
from fastapi import UploadFile, HTTPException
from src.models.ClimateDataModel import ClimateDataModel
from src.db.mongodb.Connection import DBConnectionHandler
from src.repositories.LocalStorageRepository import LocalStorageRepository

db_handle = DBConnectionHandler()
db_handle.connect_db()
conn = db_handle.get_connect_db()

class ClimateService:
    async def find_all(start: Optional[str] = None, end: Optional[str] = None)  -> List[ClimateDataModel]:
        reposirory = LocalStorageRepository(conn)
        res = reposirory.select_all(start, end)
        return res
    
    async def find_status() -> ClimateDataModel:
        reposirory = LocalStorageRepository(conn)
        res = reposirory.select_last()
        return res

    async def save(data: ClimateDataModel) -> str:
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

    async def save_csv(file: UploadFile) -> str:
        try:
            contents = await file.read()
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

            body_list = []
            for _, row in df.iterrows():
                body = {
                    "humidity": row['humidity'],
                    "temperature": row['temperature'],
                    "collection_time": row['collection_time'],
                    "network_reconnect": row['network_reconnect'],
                    "network_disconnect": row['network_disconnect']
                }
                body_list.append(body)

            print(body_list)
            repository = LocalStorageRepository(conn)
            repository.insert_all(body_list)
            return "success"

        except HTTPException as error:
            raise HTTPException(400, detail=str(error))
        
        except Exception as error:
            raise HTTPException(500, detail=f"An error occurred while processing the CSV file. {error}")

