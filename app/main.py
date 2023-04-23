
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine
from . import models
from .routers import posts,users,auth,vote
from .config import settings


# models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

# my_posts = [
#     {"title": "title of post 1", "comment": "comment of post 1", "id": 1},
#     {"title": "title of post 2", "comment": "comment of post 2", "id": 2},
#     {"title": "title of post 3", "comment": "comment of post 3", "id": 3},
# ]

# CONNECTING TO A DATABASE

# while True:
#     try:
#         conn = psycopg2.connect(host="localhost",
#                                 database="TryApp",
#                                 user="postgres", password="enkasa",
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful!!")
#         break
#     except Exception as error:
#         print('Connection to database failed')
#         print("Error", error)
#         time.sleep(2)



# CREATING USERS

