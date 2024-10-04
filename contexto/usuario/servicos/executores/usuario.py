from contexto.usuario.dominio.comandos.usuario import (
    AtualizarUsuario,
    CriarUsuario,
    DeletarUsuario,
)
from contexto.usuario.dominio.entidades.usuario import Usuario
from contexto.usuario.erros.usuario import ErroAoCriarUsuario, ErroAoDeletarUsuario
from contexto.usuario.repositorios.repo.usuario import RepositorioDoUsuario
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalho


def criar_usuario(comando: CriarUsuario, unidadeDeTrabalho: UnidadeDeTrabalho):
    usuario = Usuario.criar(
        nome=comando.nome,
        email=comando.email,
        senha=comando.senha,
        nivel_de_acesso=comando.nivel_de_acesso,
    )

    with unidadeDeTrabalho:
        repositorio = RepositorioDoUsuario(unidadeDeTrabalho.session)

        try:
            repositorio.salvar(usuario)
            unidadeDeTrabalho.commit()

        except Exception as error:
            unidadeDeTrabalho.rollback()
            msg = f"Erro ao criar usuário: {str(error)}"
            raise ErroAoCriarUsuario(detail=msg, status_code=500)

    return usuario


def atualizar_usuario(comando: AtualizarUsuario, unidadeDeTrabalho: UnidadeDeTrabalho):

    with unidadeDeTrabalho:

        repositorio = RepositorioDoUsuario(unidadeDeTrabalho.session)

        usuario = repositorio.buscar_por_id(comando.id)

        if not usuario:
            raise ErroAoCriarUsuario(detail="Usuário não encontrado", status_code=404)

        usuario.atualizar(
            nome=comando.nome,
            email=comando.email,
            senha=comando.senha,
            nivel_de_acesso=comando.nivel_de_acesso,
        )

        try:
            repositorio.salvar(usuario)
            unidadeDeTrabalho.commit()

        except Exception as error:
            unidadeDeTrabalho.rollback()
            msg = f"Erro ao atualizar usuário: {str(error)}"
            raise ErroAoCriarUsuario(detail=msg, status_code=500)

    return usuario


def deletar_usuario(comando: DeletarUsuario, unidadeDeTrabalho: UnidadeDeTrabalho):

    with unidadeDeTrabalho:

        repositorio = RepositorioDoUsuario(unidadeDeTrabalho.session)

        usuario = repositorio.buscar_por_id(comando.id)

        if not usuario:
            raise ErroAoDeletarUsuario(detail="Usuário não encontrado", status_code=404)

        try:
            repositorio.remover_por_softdelete(comando.id)
            unidadeDeTrabalho.commit()

        except Exception as error:
            unidadeDeTrabalho.rollback()
            msg = f"Erro ao deletar usuário: {str(error)}"
            raise ErroAoDeletarUsuario(detail=msg, status_code=500)

    return usuario
