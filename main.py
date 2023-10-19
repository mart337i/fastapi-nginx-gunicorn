# Create hello world FastAPI app
from fastapi import FastAPI
from database import database_con 

app = FastAPI()


@app.get("/")
def read_root():
    
    return {"message": "It's working!"}

@app.get("/facility/{id}")
def get_facility(id : int ):
    return {"Facility" : ""}
    