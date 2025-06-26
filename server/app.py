from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from server.schemas import DataEntryCreate, DataEntryOut
from server.database import Database
from server.config import Config
from server.models import DataEntry


class ServerApp:
    """Приложение сервера"""

    def __init__(self, db: Database):
        self.db = db
        self.app = FastAPI(title="Сервер")
        self.setup_middleware()
        self.setup_routes(Config.S_POST_ENDPOINT, Config.S_GET_ENDPOINT)

    def setup_middleware(self):
        """Настройка промежуточного ПО"""

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def setup_routes(self, post_endpoin: str, get_endpoint: str):
        """Настройка маршрутзации"""

        @self.app.on_event("startup")
        def startup():
            self.db.create_tables()

        @self.app.post(post_endpoin, response_model=DataEntryOut)
        def create_data_entry(
            entry: DataEntryCreate,
            db: Session = Depends(self.db.get_db)
        ):
            db_entry = DataEntry(**entry.dict())
            db.add(db_entry)
            db.commit()
            db.refresh(db_entry)
            return db_entry

        @self.app.get(get_endpoint, response_model=List[DataEntryOut])
        def read_data_entries(
            skip: int = Query(0, ge=0),
            limit: int = Query(10, ge=1, le=100),
            db: Session = Depends(self.db.get_db)
        ):
            entries = db.query(DataEntry).offset(skip).limit(limit).all()
            return entries
