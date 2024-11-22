import models,schemas,utils
from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from database import engine,get_db
from typing import Optional,List
from database import get_db
import psycopg2
from psycopg2.extras import RealDictCursor




router = APIRouter(
    prefix="/posts" ,
    tags=['Posts']
)

app = FastAPI()

conn = psycopg2.connect(host = 'localhost' , database = 'postgres' , user = 'postgres', password = 'root' , cursor_factory=RealDictCursor)
cursor = conn.cursor()

@router.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    post = db.query(models.Post).all()
    print(post)
    return{"data ": post}
    
    

@router.get("/",response_model=List[schemas.Post])
def get_post(db:Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    post = db.query(models.Post).all()
    print(post)

    return post

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db:Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s , %s , %s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.Post)
def get_post(id : int,db:Session = Depends(get_db)):
    
    post=db.query(models.Post).filter(models.Post.id == id).all()
    print(post)
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s """, str(id))
    #test_post = cursor.fetchone()
    #print(test_post)
    #"""post = find_post(int(id))"""
    if not post:
        print("Error")
        return{"Message":f"post with id : {id} was not found"}
    else:
        return post
    
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db:Session = Depends(get_db)):
    
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,str(id))
    # deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    # conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    db.delete(deleted_post)
    db.commit()
    return deleted_post
    # return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id : int, post : schemas.PostCreate,db:Session = Depends(get_db)):
    
    cursor.execute(""" UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    update_post = cursor.fetchone()
    """index = find_index_post(int(id))"""
    conn.commit()
    
    # update_post = db.query(models.Post).filter(models.Post.id == id).first()

    
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist") 
    
    # update_post.update({'title':'new update','content':'new content'},synchronize_session= False)
    #db.commit()
    """post_dict = post.dict()
    post_dict['id']=id  
    my_post[update_post]=post_dict"""
    
    return update_post
