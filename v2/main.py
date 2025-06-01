from fastapi import FastAPI
from app.api import natal_chart_router, transit_router

app = FastAPI()

app.include_router(natal_chart_router.router)
app.include_router(transit_router.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
