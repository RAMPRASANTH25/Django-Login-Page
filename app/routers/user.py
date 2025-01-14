import models,schemas,utils
from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from database import engine,get_db

router = APIRouter()

router = APIRouter(
    prefix="/collegehub" ,
    tags=['CollegeHub']
)



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def CreateUser(hub:schemas.UserCreate,db:Session = Depends(get_db)):
    #hash
    hashed = utils.hash(hub.password)
    hub.password = hashed
    new_user = models.User(**hub.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id :int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id: {id} does not exist")
    return user
    
    