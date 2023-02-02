from fastapi import APIRouter, HTTPException, Path, Depends,status, Response
from config import SessionLocal, get_db
from sqlalchemy.orm import Session
import model
from sqlalchemy import func
import schema, utils, oauth2



router  = APIRouter()

#db instance


# Creating new employee  
# Two ways to create new employee
"""  
@router.post('/create/new/employee/', tags=['employee'])
async def create_new_employee(request:schema.Create_Employee,db:Session = Depends(get_db)):
   create_new= model.Employee(name = request.name, last_name = request.last_name, status = request.status, 
   join_date = request.join_date, salary = request.salary)
   db.add(create_new)
   db.commit()#
   db.refresh(create_new)
   return create_new

    """
@router.post('/create/employee/', status_code=status.HTTP_201_CREATED,response_model=schema.Employee_Out, tags = ['employee'])
async def create_new (new_emp:schema.Create_Employee, db : Session = Depends(get_db), get_current_employee : int =Depends(oauth2.get_current_employee)):
    ## (**new_emp.dict()) converting and unpacking basemodel to dict

    hashed_password = utils.hash(new_emp.password)
    new_emp.password = hashed_password

    new_employee = model.Employee(**new_emp.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    
    return new_employee






#Get one employee by id

@router.get('/one/employee/{id}/',status_code=status.HTTP_200_OK , tags = ['employee'])
async def get_one_user(id: int, db:Session = Depends(get_db),get_current_employee : int =Depends(oauth2.get_current_employee)):
    # Creating query on model to filer employee with uniqe id
    employee = db.query(model.Employee).filter(model.Employee.id == id)

    #If there is no employee with disered id, raise 404
    if employee == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail= f'Employee with {id} not founded')
    else:
        return employee.first()


    #return db.query(model.Employee).filter(model.Employee.id == id).first()

#Get all employees
@router.get('/get/all/employees',tags=['employee'])
async  def get_all_user(db : Session = Depends(get_db),get_current_employee : int =Depends(oauth2.get_current_employee)):
    #Creating db query on model employee and calling all.
    return db.query(model.Employee).all()



    
#Now we can update employee, if we need to change salary or status for some reason.
@router.put('/update/employee/{id}', response_model=schema.Employee, tags= ['employee'])
async def update_one(id:int, update_emp : schema.Update_emp, db:Session = Depends(get_db),get_current_employee : int =Depends(oauth2.get_current_employee)):

    query_update = db.query(model.Employee).filter(model.Employee.id == id)

    update = query_update.first()
    #If there is no employee with disered id, raise 404
    if update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Employee with {id} not found')
    
    else:
        query_update.update(update_emp.dict(),synchronize_session=False)
        db.commit()
        return query_update.first()




#Delete employee
#Using simular code as updating

@router.delete('/delete/employee/{id}',status_code=status.HTTP_204_NO_CONTENT , tags=['employee'])
async def delete_user(id: int, db:Session = Depends(get_db ),get_current_employee : int =Depends(oauth2.get_current_employee)):

    query_delete = db.query(model.Employee).filter(model.Employee.id == id)

    delete = query_delete.first()

    if delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Employee with {id} not found')
    

    query_delete.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT, detail = f'task with {id} deleted')
        


    