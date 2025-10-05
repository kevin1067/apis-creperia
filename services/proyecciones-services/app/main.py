from fastapi import FastAPI
from app.routes.proyecciones import router as proyecciones_router
from mangum import Mangum
app = FastAPI()

app.include_router(proyecciones_router)
handler = Mangum(app)