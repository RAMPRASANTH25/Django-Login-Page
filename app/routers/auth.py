from fastapi import APIRouter,status,Depends,HTTPException,Response
from sqlalchemy.orm import Session
import database,schemas,models,utils
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login",status_code=status.HTTP_200_OK)
def login(user_credentials:schemas.UserLogin,db:Session = Depends(database.get_db),):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    return JSONResponse(content=True)
    