from fastapi import FastAPI, Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models,schemas,utils
from database import engine
from routers import post,user,auth




models.Base.metadata.create_all(bind = engine)

app = FastAPI()



"""my_post =[{"title" : "Paper" , "content" : "news" , "id" : 1} , {"title" : "magazine" , "content" : "puzzle" , "id" : 2}]

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p"""
        
while  True:
    
    try:
        conn = psycopg2.connect(host = 'localhost' , database = 'postgres' , user = 'postgres', password = 'root' , cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was Successfull !")
        break
    except Exception as error:
        print("Connectiong the database failed")
        print("Error: ",error)
        time.sleep(2)

"""def find_index_post(id):
    for i,p in enumerate(my_post):
        if p['id'] == id:
            return i"""
        


    
    

# Normal post

"""@app.get("/")
async def root():
    return {"message" : "Hello World!!"}"""
    



"""
@app.post("/createposts")
def create_posts(post: Post):
    print(post)
    return{'data':post}
    

@app.post("/createposts")
def create_posts(post: Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,100000)
    my_post.append(post_dict)
    return{"Data":post_dict}

@app.post("/posts1",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,100000)
    my_post.append(post_dict)
    return{"Data":post_dict}


# {id}

@app.get("/posts/{id}")
def get_post(id : int):
    print(id)
    return {"post_details" : f"post id - {id}"}

@app.get("/posts/{id}")
def get_post(id : int):
    print(type(id))
    post = find_post(int(id))
    print(post)
    return {"post_details" : post}

@app.get("/posts/{id}")
def get_post(id : int, response: Response):
    
    post = find_post(int(id))
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        print("Error")
        return{"Message":f"post with id : {id} was not found"}
    return {"post_details" : post}


@app.get("/posts/{id}")
def get_post(id : int, response: Response):
    
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} not found ")
    return {"post_details" : post}



#latest

@app.get("/posts/latest")
def get_latest_post():
    post = my_post(len(my_post)-1)
    return {"Recenty added post is" : post}



#delete

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    index = find_index_post(int(id))
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#update

@app.put("/posts/{id}")
def update_post(id : int, post : Post):
    index = find_index_post(int(id))
    
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist") 
    post_dict = post.dict()
    post_dict['id']=id
    my_post[index]=post_dict
    return {'data': post_dict}

"""

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

