from typing import Optional
from fastapi import APIRouter
from src.services.ClimateService import ClimateService
from src.models.ClimateDataModel import ClimateDataModel

app_router = APIRouter(prefix='/v1')

@app_router.get('/dados', status_code=200)   
async def find_all(start:str | None = None, end:str | None = None):
    print(start, "e", end)
    return await ClimateService.find_all(start, end)

@app_router.get('/status', status_code=200)   
async def find_status():
    return await ClimateService.find_status()

@app_router.post('/save', status_code=200)   
async def save(climateData: ClimateDataModel):
  return await ClimateService.save(climateData)

