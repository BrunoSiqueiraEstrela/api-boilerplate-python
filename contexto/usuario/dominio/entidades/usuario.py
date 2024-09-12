from datetime import datetime
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
