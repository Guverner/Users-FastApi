from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from routers import get_db
from fastapi.security  import OAuth2PasswordRequestForm
import oauth2
from os import access
from sqlalchemy import func
from config import get_db


import config, schema, model, utils

router = APIRouter(tags= ['Authentication'])



@router.post('/login', response_model=schema.Token)
async def login_or(employee_credentials: OAuth2PasswordRequestForm= Depends(), db:Session = Depends(get_db)):
    employee = db.query(model.Employee).filter(model.Employee.email == employee_credentials.username).one_or_none()
    
    
    
    if not employee:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail= ' Invalid Credentials')
    

    
    if not utils.verify(employee_credentials.password,employee.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= 'Invalit Credentials')

    accees_token = oauth2.create_access_token(data = {"employee.id" : employee.id})

    return {"acces_token" : accees_token, "token_type" : "bearer"}
    from passlib.context import CryptContext


    