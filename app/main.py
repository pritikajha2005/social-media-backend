from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, user, auth



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
 try:
   conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Postgres20@', cursor_factory=RealDictCursor)
   cursor=conn.cursor()
   print("Database connection was successfull")
   break
 except Exception as error:
   print("connection to databse failed")
   print("Error :", error) 
   time.sleep(2) 

my_posts=[{"title": "title of post 1", "content": "content of post 1", "id": 1},
          {"title": "fav food", "content": "I like pizza", "id": 2}]  



def find_post(id):
   for p in my_posts:
     if p["id"]==id:
       return p

def find_index_post(id):
  #we have to iterate both the index and the post and return the index with post having specific id
  for i, p in enumerate(my_posts):
    if p["id"]==id:
     return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)