from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL_LIBRARY = {
    "recommendation_history": "sqlite:///./recommendation_history.db",
    "structured_data_history": "sqlite:///./structured_data_history.db"
}
DATABASE_URL = DATABASE_URL_LIBRARY["recommendation_history"]
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
