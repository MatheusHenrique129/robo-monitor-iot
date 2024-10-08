from routes.Router import app_router
from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()

app.include_router(app_router)
print("ROn Servidor", app)