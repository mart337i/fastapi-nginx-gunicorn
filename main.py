# Create hello world FastAPI app
from fastapi import FastAPI
from database import database_con
from model import facility 
import logging 

database = database_con.MariaDB
cr = database.get_curser

logging.basicConfig(filename='logs/application.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "It's working!"}

@app.get("/facility")
def get_facility():
    res = database.execute(cr, facility.Facility.get_facility())
    return {"Facility" : f"{res}"}
    