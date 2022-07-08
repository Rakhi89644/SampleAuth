
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///todos.db")
Base = declarative_base()
SessionLocal=sessionmaker(bind=engine,expire_on_commit=False)


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///.todos.db"

# #create the engine so it can be use other app
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False}
# )

# SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Base = declarative_base()