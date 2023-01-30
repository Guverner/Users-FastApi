from fastapi import APIRouter, HTTPException, Path, Depends,status, Response
from config import SessionLocal, get_db
from sqlalchemy.orm import Session
import model
from sqlalchemy import func
import schema, utils, oauth2



router = APIRouter()


@router.post("/create/task/" , status_code = status.HTTP_201_CREATED, response_model = schema.Task)
def create_task(new :schema.Task_In, db: Session = Depends(get_db), current_employee : int =Depends(oauth2.get_current_employee)):

   
   new_task = model.Tasks( owner_id = current_employee.id , **new.dict())
   db.add(new_task)
   db.commit()
   db.refresh(new_task)
   return new_task
