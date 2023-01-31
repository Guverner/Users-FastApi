from fastapi import APIRouter, HTTPException, Path, Depends,status, Response
from config import SessionLocal, get_db
from sqlalchemy.orm import Session
import model
from sqlalchemy import func
import schema, utils, oauth2



router = APIRouter()


@router.post("/create/task/" , status_code = status.HTTP_201_CREATED, response_model = schema.Task)
async def create_task(new :schema.Task_In, db: Session = Depends(get_db), current_employee : int =Depends(oauth2.get_current_employee)):

   
   new_task = model.Tasks( owner_id = current_employee.id , **new.dict())
   db.add(new_task)
   db.commit()
   db.refresh(new_task)
   return new_task


# Get all tasks from single employee
@router.get("/get/all/tasks", status_code= status.HTTP_200_OK)
async def get_all_tasks(db:Session = Depends(get_db), current_employee : int = Depends(oauth2.get_current_employee)):

   return(model.Tasks).all()


#Get all tasks form single employee where status = False

@router.get('/get/status/of/tasks/', status_code=status.HTTP_200_OK)
async def get_status_tasks(db:Session = Depends(get_db), current_employee : int = Depends(oauth2.get_current_employee)):

   status_task = db.query(model.Tasks).filter(model.Tasks.status == (False)).all()

   return status_task

# Deleting task
@router.delete('/delete/task/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id : int, db:Session = Depends(get_db), current_employee : int = Depends(oauth2.get_current_employee)):
   task_query = db.query(model.Tasks).filter(model.Tasks.id == id)
   task = task_query.first()
   
   
   if task == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} does not exist')

   # If employee is not task owner, raise exception
   if task.owner_id != current_employee.id :
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f'Not authoriyed to perform request action')
   
   task_query.delete(synchronize_session = False)
   db.commit()