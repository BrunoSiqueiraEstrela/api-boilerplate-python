from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4, UUID
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
    id: UUID
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
            id=uuid4(),
            nome=nome,
            email=email,
            senha=senha,
            nivel_de_acesso=nivel_de_acesso,
            ativo=True,
            criado_em=datetime.now(),
            atualizado_em=datetime.now(),
            deletado_em=None,
        )

    def atualizar(
        self, nome: str, email: str, senha: str, nivel_de_acesso: NivelDeAcesso
    ):
        if nome:
            self.nome = nome
        if email:
            self.email = email
        if senha:
            self.senha = senha
        if nivel_de_acesso:
            self.nivel_de_acesso = nivel_de_acesso

    def __repr__(self) -> str:
        return f"Usuario<(id={self.id}),(nome={self.nome})>"
