from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from  . config import settings
SECRET_KEY = 'beeb6ddab58e3119e29f35da6f56d3c3f33e4e952ba23afd757b39c18945ad7a'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth_bearer = OAuth2PasswordBearer(tokenUrl='login')
#create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

#verify access token
def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        return token_data
    except JWTError:
        raise credentials_exception
def get_current_user(token:str = Depends(oauth_bearer),db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credentials",
                                          headers={'WWW-Authenticate':'Bearer'})
    token_data =  verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user
