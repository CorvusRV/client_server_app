from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.config import Config

Base = declarative_base()

class Database:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.database_url = Config.DB_URL
        self.echo_sql = Config.DB_ECHO
        self.init_db()

    def init_db(self):
        """Инициализация БД"""
        self.engine = create_engine(self.database_url, echo=self.echo_sql)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def get_db(self):
        """Метод получения доступа к БД"""

        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_tables(self):
        """Создание таблицы в БД"""

        Base.metadata.create_all(bind=self.engine)
