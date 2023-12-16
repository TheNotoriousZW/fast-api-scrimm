from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.schemas import UserLogin
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_creds.username).first()

    if not user:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="wrong credentials")
    
    if not utils.hash_valid(user_creds.password, user.password):
        return HTTPException(detail="wrong credentials", status_code=status.HTTP_403_FORBIDDEN)
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    token_type = 'bearer'
        
    return {"access_token":access_token, "token_type": token_type}
    


