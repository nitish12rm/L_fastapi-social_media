from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from ..database import engine, get_db
from .. import models,schemas,utils
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db:Session = Depends(get_db)):
    #jo pass aya h usko pehle hash kardenge fir user.password ko update krdenge
    hashedPass = utils.hash(user.password)
    user.password = hashedPass
    newPost=models.User(**user.model_dump())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost
@router.get('/',response_model=list[schemas.UserOut],status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} was not found!")

    return user
