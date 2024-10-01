from dataclasses import dataclass
from sqlalchemy.orm.session import Session, sessionmaker
from typing import Any, Optional, Self
from sqlalchemy import create_engine, Engine, text


from libs.variaveis.gerenciador_de_env import ENVS


### REFAZER
def conectar():

    engine: Engine = create_engine(
        ENVS.DB_STRING_CONNECTION, isolation_level="AUTOCOMMIT"
    )
    _session = sessionmaker(bind=engine, expire_on_commit=False)

    return _session()


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
