from dataclasses import dataclass
from sqlalchemy.orm.session import Session
from typing import Any, Optional, Self
from sqlalchemy import text

from libs.database.config import conectar


@dataclass
class UnidadeDeTrabalho:

    schema: str = "public"
    session: Optional[Session] = None

    def __enter__(self) -> Self:
        if not self.session:
            self.session = conectar()

        self.session.execute(text(f"SET search_path TO '{self.schema}'"))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def adicionar(self, obj: Any):
        self.session.add(obj)
