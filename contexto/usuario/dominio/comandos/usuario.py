from pydantic import EmailStr
from uuid import UUID

from contexto.usuario.dominio.objeto_de_valor.usuario import NivelDeAcesso
from libs.dominio.comando import Comando


class CriarUsuario(Comando):
    nome: str
    email: EmailStr
    senha: str
    nivel_de_acesso: NivelDeAcesso


class AtualizarUsuario(Comando):
    id: UUID
    nome: str
    email: EmailStr
    senha: str
    nivel_de_acesso: NivelDeAcesso


class ObterUsuario(Comando):
    id: UUID


class ListarUsuarios(Comando): ...


class DeletarUsuario(Comando):
    id: UUID
