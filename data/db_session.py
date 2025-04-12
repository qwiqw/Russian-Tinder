from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

DATABASE_URL = "sqlite:///db/users.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Определите Enum для пола
class Gender(enum.Enum):
    MALE = "Мужской"
    FEMALE = "Женский"


class EducationLevel(enum.Enum):
    SCHOOL = "Школьное"
    SECONDARY = "Среднее"
    HIGHER = "Высшее"
    DOCTOR = "Доктор наук"
    NONE = "Отсутствует"


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String)  # 
    gender = Column(Enum(Gender))
    age = Column(Integer)
    education = Column(Enum(EducationLevel))
    profession = Column(String)


Base.metadata.create_all(bind=engine)  # Создает таблицы в базе данных


# Функция для получения сессии базы данных (для использования в Flask)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
