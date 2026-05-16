from fastapi import FastAPI

from app.db import Base, engine

from app.routes import auth_routes, file_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cloud Silos", version="1.0")

app.include_router(auth_routes.router)
app.include_router(file_routes.router)


@app.get("/")
def home():
    return {"message": "Cloud Silos API Running"}
