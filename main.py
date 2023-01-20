from fastapi import FastAPI
import model
from config import engine
import routers, auth


model.Base.metadata.create_all(bind= engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(routers.router)
