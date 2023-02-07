from database import Base
from sqlalchemy import Column,Integer,String,Boolean
from passlib.hash import bcrypt


class todo_list(Base):
    '''
    :create table name as todoList 
    :create column id that Store int type data and unique(means uniquely identify the row)
    :create column name as taskName that store string type data
    :create is_complete column that take boolean type tada 

    '''
    __tablename__="todoList"
    id=Column(Integer,primary_key=True,index=True)
    taskName=Column(String(200))
    is_complete=Column(Boolean,default=False)
    
    