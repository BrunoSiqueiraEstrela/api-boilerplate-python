from datetime import datetime
from enum import Enum
from libs.dominio.entidade import Entidade
from libs.tipos.uuid import ID

# Usuario:
# - id
# - nome
# - email
# - senha
# - nivel_de_acesso
# - ativo
# - criado_em
# - atualizado_em
# - deletado_em


class NivelDeAcesso(Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    USUARIO = "USUARIO"


class Usuario(Entidade):
    id: ID
    nome: str
    email: str
    senha: str
    nivel_de_acesso: NivelDeAcesso
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime
    deletado_em: datetime

    @classmethod
    def criar(
        cls, id: ID, nome: str, email: str, senha: str, nivel_de_acesso: NivelDeAcesso
    ) -> "Usuario":
        return cls(
            id=id,
            nome=nome,
            email=email,
            senha=senha,
            nivel_de_acesso=nivel_de_acesso,
            ativo=True,
            criado_em=datetime.now(),
            atualizado_em=datetime.now(),
            deletado_em=None,
        )

    def __repr__(self) -> str:
        return f"Usuario<(id={self.id}),(nome={self.nome})>"
