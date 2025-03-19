import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

class SuperAdminCreds:
    USERNAME = os.getenv('SUPER_ADMIN_USERNAME')
    PASSWORD = os.getenv('SUPER_ADMIN_PASSWORD')

class DbCreds:
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    USERNAME = os.getenv('USERNAME_DB')
    PASSWORD = os.getenv('PASSWORD_DB')

    Base = declarative_base()

    engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}") # Создаем движок (engine) для подключения к базе данных
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Создаем фабрику сессий
