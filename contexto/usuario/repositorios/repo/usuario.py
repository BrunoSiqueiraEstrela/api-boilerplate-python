from datetime import datetime
from contexto.usuario.dominio.entidades.usuario import Usuario
from libs.dominio.repositorio import Repositorio
from sqlalchemy.orm.session import Session
from typing import List, Optional
from uuid import UUID


class RepositorioUsuario(Repositorio):

    def __init__(self, session: Session):
        self.session = session

    # POST
    def salvar(self, usuario: Usuario) -> Optional[Usuario]:
        usuario_salvo = self.session.add(usuario)
        return usuario_salvo

    # GET ONE
    def buscar_por_id(self, id: UUID) -> Optional[Usuario]:

        consulta = self.session.query(Usuario)
        consulta = consulta.filter(Usuario.id == id, Usuario.ativo)
        usuario = consulta.first()
        return usuario

    def buscar_por_email(self, email: str) -> Optional[Usuario]:

        consulta = self.session.query(Usuario)
        consulta = consulta.filter(Usuario.email == email, Usuario.ativo)
        usuario = consulta.first()
        return usuario

    # GET ALL
    def listar(self) -> Optional[list[Usuario]]:
        consulta = self.session.query(Usuario)
        consulta = consulta.filter(Usuario.ativo)
        usuarios = consulta.all()
        return usuarios

    # PUT
    def atualizar(self, entidade: Usuario) -> Optional[Usuario]:
        self.session.merge(entidade)
        return entidade

    # DELETE
    # def remover_por_softdelete(self, id: UUID) -> Optional[UUID]:
    # return (
    # self.session.query(Usuario)
    # .filter(Usuario.id == id)
    # .update({Usuario.deletado_em: datetime.now(), Usuario.ativo: False})
    # )
    #
    # def remover_permanentemente(self, id: UUID) -> Optional[UUID]:
    # return self.session.query(Usuario).filter(Usuario.id == id).delete()
    #
    # def ativar(self, id: UUID) -> Optional[Usuario]:
    # return (
    # self.session.query(Usuario)
    # .filter(Usuario.id == id)
    # .update({Usuario.ativo: True})
    # )
    #
