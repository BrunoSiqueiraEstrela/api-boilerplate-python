from typing import Optional

from contexto.usuario.dominio.entidades.usuario import Usuario
from contexto.usuario.erros.usuario import ErroAoObterUsuario
from contexto.usuario.repositorios.repo.usuario import RepositorioDoUsuario
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalho
from contexto.usuario.dominio.comandos.usuario import ListarUsuarios, ObterUsuario


def obter_usuario_por_id(
    comando: ObterUsuario, unidadeDeTrabalho: UnidadeDeTrabalho
) -> Usuario:
    with unidadeDeTrabalho:
        repositorio = RepositorioDoUsuario(unidadeDeTrabalho.session)
        usuario: Optional[Usuario] = repositorio.buscar_por_id(comando.id)

        if not usuario:
            raise ErroAoObterUsuario(detail="Usuário não encontrado", status_code=404)

    return usuario


def listar_usuarios(
    comando: ListarUsuarios, unidadeDeTrabalho: UnidadeDeTrabalho
) -> list[Usuario]:
    with unidadeDeTrabalho:
        repositorio = RepositorioDoUsuario(unidadeDeTrabalho.session)
        usuarios = repositorio.listar()

    return usuarios
