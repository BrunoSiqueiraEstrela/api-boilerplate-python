from datetime import datetime
from contexto.usuario.dominio.entidades.usuario import Usuario
from libs.dominio.repositorio import Repositorio
from sqlalchemy.orm.session import Session
from typing import List, Optional
from uuid import UUID


class RepositorioDoUsuario(Repositorio):

    def __init__(self, session: Session):
        self.session = session

    # POST
    def salvar(self, usuario: Usuario) -> Optional[Usuario]:
        return self.session.add(usuario)

    # GET ONE
    def buscar_por_id(self, id: UUID) -> Optional[Usuario]:
        return (
            self.session.query(Usuario).filter(Usuario.id == id, Usuario.ativo).first()
        )

    # GET ALL
    def listar(self) -> Optional[List[Usuario]]:
        return self.session.query(Usuario).filter(Usuario.ativo).all()

    # PUT
    def atualizar(self, entidade: Usuario) -> Optional[Usuario]:
        return self.session.merge(entidade)

    # DELETE
    def remover_por_softdelete(self, id: UUID) -> Optional[UUID]:
        return (
            self.session.query(Usuario)
            .filter(Usuario.id == id)
            .update({Usuario.deletado_em: datetime.now(), Usuario.ativo: False})
        )

    def remover_permanentemente(self, id: UUID) -> Optional[UUID]:
        return self.session.query(Usuario).filter(Usuario.id == id).delete()

    def ativar(self, id: UUID) -> Optional[Usuario]:
        return (
            self.session.query(Usuario)
            .filter(Usuario.id == id)
            .update({Usuario.ativo: True})
        )
