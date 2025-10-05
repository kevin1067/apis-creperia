from fastapi import FastAPI
from mangum import Mangum
from .router import router as tiendas_router

app = FastAPI(title="Tiendas API", version="1.0.0")
app.include_router(tiendas_router)
handler = Mangum(app)