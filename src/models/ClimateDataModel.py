from pydantic import BaseModel

class ClimateDataModel(BaseModel):
    temperature: float
    humidity: float
    collection_time: datetime
    network_disconnect: Optional[datetime]
    network_reconnect: Optional[datetime]