

from fastapi import APIRouter, status, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from ..import database
from .. import models, schemas, utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(prefix= "/login",tags= ["auth"])
# LOGGING IN TO THE  APP
@router.post("/")
def authenticate(login_model:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    login_query = db.query(models.ORM_User).filter(
        models.ORM_User.email == login_model.username)
    login_credentials = login_query.first()
    if not login_credentials:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    if not utils.verify_passwords(login_model.password, login_credentials.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
#CREATE THE TOKEN AND RETURN IT HERE 
    access_token = oauth2.create_access_token(data= {"user_id":login_credentials.id})
    return {"access_token": access_token, "token_type":"bearer"}

#TOKEN SENT