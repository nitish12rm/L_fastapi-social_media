from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils,oauth2
from fastapi.security import OAuth2PasswordRequestForm #to create a form to use in post man...isme default username and password field hota hai  which we will use
#we wont send the data in body but forms
router = APIRouter(
    prefix="/login",
    tags=['Authenticaton']
)

@router.post('/',response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db),):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    
    #create token
    access_token =  oauth2.create_access_token(data={"user_id":user.id})

    #return token

    return{"access_token":access_token,"token_type":"bearer"}
    