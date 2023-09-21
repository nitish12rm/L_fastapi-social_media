from fastapi import FastAPI, Response, status, HTTPException,Depends,COR
from typing import Any
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . database import engine
from apps import models
from . routers import posts,users,auth,votes
from  .config import settings
from fastapi.middleware.cors import CORSMiddleware
# from passlib.context import CryptContext

#creates dependency--> that it creates all the tables and columns defined 
#but now that we have added alembic migration tool we no longer need this
#cz alembic will take care of it
# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
#initializing the passlib to crypt the password. using brcrypt algo
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#CORS--> cross origin resource sharing
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print(settings.database_password)
while True:
    try:
        #connect to a database
        conn = psycopg2.connect(host='localhost',database='fastapi-proj1',user='postgres',password='nkgisgreat',cursor_factory=RealDictCursor)
        #open a cursor to perform db opn
        cursor = conn.cursor()
        print('database connnection was successfull')
        break
    except Exception as error:
        print("Cpnnecting to DB failed")
        print("Error: ",error)
        #har 2 sec bad exevute
        time.sleep(2)

         


@app.get("/")
def root():
    return {"message":"hello this is my first api!!!!!!!!"}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)





     


