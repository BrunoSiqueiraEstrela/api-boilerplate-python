from dataclasses import dataclass
from datetime import datetime
import uuid
from contexto.usuario.dominio.objeto_de_valor.usuario import NivelDeAcesso, UsuarioID
from libs.dominio.entidade import Entidade

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


@dataclass
class Usuario(Entidade):
    id: UsuarioID
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
        cls, nome: str, email: str, senha: str, nivel_de_acesso: NivelDeAcesso
    ) -> "Usuario":
        return cls(
            id=uuid.uuid4(),
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
