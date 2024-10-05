from datetime import datetime
from uuid import UUID
from pydantic import EmailStr

from contexto.usuario.dominio.objeto_de_valor.usuario import NivelDeAcesso
from libs.fastapi.entrada_e_saida import Modelo


class CriarUsuarioEntrada(Modelo):
    nome: str
    email: EmailStr
    senha: str
    nivel_de_acesso: NivelDeAcesso

    # @field_validator("CAMPO")
    # def check_cpf(cls, value):
    #    if not validate(value):
    #        raise ValueError("CAMPO inválido")
    #    return value


class AtualizarUsuarioEntrada(Modelo):
    nome: str
    email: EmailStr
    senha: str
    nivel_de_acesso: NivelDeAcesso


class SaidaUsuario(Modelo):
    id: UUID
    nome: str
    email: EmailStr
    nivel_de_acesso: NivelDeAcesso
    criado_em: datetime
    atualizado_em: datetime
