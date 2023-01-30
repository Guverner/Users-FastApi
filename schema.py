from typing import List, Optional, Generic, TypeVar, Union
from pydantic import  BaseModel, Field , EmailStr
from pydantic.generics import GenericModel
from datetime import datetime


class Create_Employee (BaseModel):
    name : str
    last_name : str
    username : str
    email : Union [str]
    password : str
    status : str
    join_date  : datetime
    salary : int


  

#Class that send data back to employee
class Employee_Out(BaseModel):
    id : int
    name : str
    last_name : str
    username : str
    email : Union[str]
    status : str
    salary : int
    #config class to convert to regular pydantic model
    class Config:
        orm_mode = True



class Employee_Login(BaseModel):
    email: Union [str]
    password : str


class Update_emp(Create_Employee):
    pass


class Employee (Create_Employee):
    id : int

    class Config:
        orm_mode = True




class Token(BaseModel):
    acces_token: str 
    token_type : str


class TokenData(BaseModel):
    id: Optional[str] = None
    


#  TASK SHEMAS :

class Task_In(BaseModel):
    task_name : str
    task_content : str
    status : bool = False
    createt_at : datetime

class Task_Out(Task_In):
    pass

    class Config :
        orm_mode = True
    
class Task(Task_In):
    id : int
    owner_id : int
    

    class Config:
        orm_mode = True

