from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ClimateDataModel(BaseModel):
    humidity: float
    temperature: float
    collection_time: datetime
    network_reconnect: Optional[datetime]
    network_disconnect: Optional[datetime]