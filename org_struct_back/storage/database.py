from abc import ABC, abstractmethod
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from org_struct_back.settings.database_settings import DatabaseSettings
from org_struct_back.storage.entities import Base


class Database(ABC):
    @abstractmethod
    def __call__(self) -> Generator[Session, Any]:
        pass


class DatabaseImpl(Database):
    def __init__(self, settings: DatabaseSettings) -> None:
        self._engine = create_engine(settings.connection_string, echo=False)
        self._scoped_session = scoped_session(sessionmaker(bind=self._engine))
        Base.metadata.create_all(self._engine)

    @contextmanager
    def __call__(self) -> Generator[Session, Any]:
        session = self._scoped_session()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
