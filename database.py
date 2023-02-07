from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


'''
The create_engine() function produces an Engine object based on a URL
'''
DB_URL="mysql+mysqlconnector://root:Kiet9211@127.0.0.1:3306/wobotTodo"
engine=create_engine(DB_URL)



'''
declarative_base() is a factory function that constructs a base class for
declarative class definitions (which is assigned to the Base variable in your example).
'''
Base=declarative_base()



'''
A configurable Session factory.
'''
SessionLocal=sessionmaker(autocommit=False,bind=engine)


