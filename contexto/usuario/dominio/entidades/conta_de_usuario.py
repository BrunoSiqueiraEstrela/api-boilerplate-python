from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4, UUID
from contexto.usuario.dominio.objeto_de_valor.conta_de_usuario import NivelDeAcesso
from libs.dominio.entidade import Entidade
from libs.fastapi.crypt import verificar_senha_hash


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
        self,
        nome: str = None,
        email: str = None,
        senha: str = None,
        nivel_de_acesso: NivelDeAcesso = None,
    ):
        if nome:
            self.nome = nome
        if email:
            self.email = email
        if senha:
            self.senha = senha
        if nivel_de_acesso:
            self.nivel_de_acesso = nivel_de_acesso

    def verificar_senha(self, senha: str) -> bool:
        return verificar_senha_hash(senha, self.senha)

    def deletar(self):
        self.ativo = False
        self.deletado_em = datetime.now()

    def desativar(self):
        self.ativo = False

    def ativar(self):
        self.ativo = True

    def __repr__(self) -> str:
        return f"Usuario<(id={self.id}),(nome={self.nome})>"
