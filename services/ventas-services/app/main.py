from fastapi import FastAPI
from .router import router as ventas_router
from mangum import Mangum
app = FastAPI()
app.include_router(ventas_router)
handler = Mangum(app)