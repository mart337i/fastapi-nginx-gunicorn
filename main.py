# Create hello world FastAPI app
from fastapi import FastAPI
from database import database_con

database = database_con.MariaDB
cr = database.get_curser

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "It's working!"}

@app.get("/facility")
def get_facility(id : int ):
    res = database.execute(cr,get_facility_query)
    return {"Facility" : f"{res}"}
    
def get_facility_query():
    return """
        Select * facility;
    """