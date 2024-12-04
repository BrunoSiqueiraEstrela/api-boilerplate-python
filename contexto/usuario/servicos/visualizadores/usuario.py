from typing import Optional

from contexto.usuario.dominio.entidades.usuario import Usuario
from contexto.usuario.dominio.objeto_de_valor.usuario import NivelDeAcesso
from contexto.usuario.erros.usuario import ErroAoObterUsuario
from contexto.usuario.repositorios.repo.usuario import RepositorioUsuario
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalho
from contexto.usuario.dominio.comandos.usuario import (
    ListarUsuarios,
    ObterPerfilUsuario,
    ObterUsuario,
)


# ADMIN
def obter_usuario_por_id(comando: ObterUsuario, uow: UnidadeDeTrabalho) -> Usuario:
    with uow:
        repositorio = RepositorioUsuario(uow.session)

        admin = repositorio.buscar_por_id(comando.id_admin)

        if not admin:
            raise ErroAoObterUsuario(detail="Usuário não encontrado", status_code=404)

        if admin.nivel_de_acesso != NivelDeAcesso.ADMINISTRADOR:
            raise ErroAoObterUsuario(detail="Usuário não autorizado", status_code=401)

        usuario: Optional[Usuario] = repositorio.buscar_por_id(comando.id)

        if not usuario:
            raise ErroAoObterUsuario(detail="Usuário não encontrado", status_code=404)

    return usuario


# TODO: ADD PAGINAÇÂO
def listar_todos_usuarios(
    comando: ListarUsuarios, uow: UnidadeDeTrabalho
) -> list[Usuario]:
    with uow:
        repositorio = RepositorioUsuario(uow.session)

        admin = repositorio.buscar_por_id(comando.id_admin)

        if not admin:
            raise ErroAoObterUsuario(detail="Usuário não encontrado", status_code=404)

        if admin.nivel_de_acesso != NivelDeAcesso.ADMINISTRADOR:
            raise ErroAoObterUsuario(detail="Usuário não autorizado", status_code=401)

        usuarios: list[Usuario] | None = repositorio.listar()

    return usuarios


# USUARIO
def obter_usuario_logado(
    comando: ObterPerfilUsuario, uow: UnidadeDeTrabalho
) -> Usuario:
    with uow:
        repositorio = RepositorioUsuario(uow.session)
        usuario: Optional[Usuario] = repositorio.buscar_por_id(comando.id_usuario)

        if not usuario:
            raise ErroAoObterUsuario(detail="Usuário não encontrado", status_code=404)

    return usuario
