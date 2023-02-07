from fastapi import FastAPI, HTTPException,Depends,status
from pydantic import BaseModel
from typing import List, Optional
from database import Base, SessionLocal,engine
from models import todo_list
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



'''
The usual way to issue CREATE is to use create_all() on the MetaData object.
This method will issue queries that first check for the existence of each individual table, and if not found will issue
the CREATE statements.
'''
Base.metadata.create_all(bind=engine)

class TodoSchema(BaseModel):
    '''
    Declare examples of the data that app can receive.
    :id take a integer type number
    :taskName take a string type data
    :is_complete take boolean type data -true or false

    '''
    id:int
    taskName:str
    is_complete:str
    class Config:
        orm_mode=True



class todoCreateSchema(BaseModel):
    '''
    Declare examples of the data that app can receive.
    
    :taskName take a string type data
    
    '''
    taskName:str
    class Config:
        orm_mode=True



class todoCompleteTask(BaseModel):
    '''
    Declare examples of the data that app can receive.
    
    :is_complete take boolean type data -true or false
    
    '''
    is_complete:bool
    class Config:
        orm_mode=True
   

    
'''
creating new instance of FastAPI class to be used in a program
'''
app=FastAPI(title="TODO List API")




'''
The oauth2_scheme variable is an instance of OAuth2PasswordBearer
'''
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@app.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Get the token
    """
    return {'access_token' : form_data.username + 'token'}


async def get_db():
    """
    Create the Session for the databse.
    The yield keyword use for creating a single session for each request.
    """
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()



@app.get('/')
async def home(token: str = Depends(oauth2_scheme)):
    """
    If user is authenticated then show this message otherwise show User is not authorized
    """
    return {"Hello":"WobotAI Dev."}


@app.get("/todo",response_model=List[TodoSchema])
async def get_all_Tasks(db:Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    """
    If user is authenticated, then Fetch all tasks from the databse.
    """
    return db.query(todo_list).all()


@app.get("/todo/Completed",response_model=List[todoCreateSchema])
async def get_All_Completed_Tasks(db:Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    """
    Fetch the all Copleted task of the user
    """
    try:
        u=db.query(todo_list).filter(todo_list.is_complete==True).all()
        return u
    except:
        return HTTPException(status_code=404,detail="Task not found")
    
@app.get("/todo/Uncompleted",response_model=List[todoCreateSchema])
async def get_All_Uncompleted_Tasks(db:Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    """
    Fetch all the Uncompleted task from the databse
    """
    try:
        u=db.query(todo_list).filter(todo_list.is_complete==False).all()
        return u
    except:
        return HTTPException(status_code=404,detail="Task not found")


@app.get("/todo/{id}",response_class=JSONResponse)
async def get_Task_By_Id(id:int,db:Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    """
    Fetch the specific task from the database by using the id of the task
    """
    try:
        u=db.query(todo_list).filter(todo_list.id==id).first()
        return u
    except:
        return HTTPException(status_code=404,detail="Task not found")



@app.post("/todo",response_model=TodoSchema)
async def create_Task(todo:todoCreateSchema,db:Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    """
    Create the task and save in database
    """
    u=todo_list(taskName=todo.taskName)
    db.add(u)
    db.commit()
    return u


@app.put("/todo/{id}",response_model=todoCreateSchema)
async def update_Task(id:int,todo:todoCreateSchema,db:Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    """
    This function use for update the specific task by using the id of task and then save in databse(update)
    """
    try:
        u=db.query(todo_list).filter(todo_list.id==id).first()
        u.taskName=todo.taskName
        db.add(u)
        db.commit()
        return u
    except:
        return HTTPException(status_code=404,detail="Task not found")
    

@app.put("/todo/complete/{id}",response_model=todoCompleteTask)
async def Mark_A_Task_Complete(id:int,todo:todoCompleteTask,db:Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    """
    If task is completed ,then to mark it Completed and save in database
    """
    try:
        u=db.query(todo_list).filter(todo_list.id==id).first()
        u.is_complete=todo.is_complete
        db.add(u)
        db.commit()
        return u
    except:
        return HTTPException(status_code=404,detail="Task not found")


@app.delete("/todo/{id}",response_class=JSONResponse)
async def delete_Task(id:int,db:Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    """
    If task is coppleted or not completed and user want to delete it ,then task is deleted from database
    """
    try:
        u=db.query(todo_list).filter(todo_list.id==id).first()
        db.delete(u)
        db.commit()
        return {f"Task of id {id} has been deleted":True}
    except:
        return HTTPException(status_code=404,detail="Task not found")






