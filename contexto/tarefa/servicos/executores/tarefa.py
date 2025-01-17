from typing import Optional

from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalhoAbastrato
from contexto.tarefa.dominio.comandos.tarefa import (
    AtualizarTarefa,
    CriarTarefa,
    DeletarTarefa,
)
from contexto.tarefa.erros.tarefa import (
    ErroAoAtualizarTarefa,
    ErroAoCriarTarefa,
    ErroAoDeletarTarefa,
)
from contexto.tarefa.dominio.entidades.tarefa import Tarefa
from contexto.tarefa.repositorios.repo.tarefa import RepositorioTarefas


# TODO: Retornar ID apenas
def criar_tarefa(comando: CriarTarefa, uow: UnidadeDeTrabalhoAbastrato):
    tarefa: Tarefa = Tarefa.criar(
        id_usuario=comando.id_usuario,
        titulo=comando.titulo,
        descricao=comando.descricao,
        data_de_inicio=comando.data_de_inicio,
        data_de_fim=comando.data_de_fim,
        prioridade=comando.prioridade,
        status=comando.status,
    )

    with uow:
        repositorio = RepositorioTarefas(uow.session)

        usuario = repositorio.buscar_usuario_por_id(comando.id_usuario)

        if not usuario:
            raise ErroAoCriarTarefa(detail="Usuário não encontrado", status_code=404)

        repositorio.adicionar_tarefa(tarefa)

        uow.commit()

    return tarefa


def atualizar_tarefa(
    comando: AtualizarTarefa, uow: UnidadeDeTrabalhoAbastrato
) -> Optional[Tarefa]:

    with uow:
        repositorio = RepositorioTarefas(uow.session)

        tarefa: Optional[Tarefa] = repositorio.buscar_por_id_de_usuario_e_id_de_tarefa(
            id_tarefa=comando.id_tarefa, id_usuario=comando.id_usuario
        )

        if not tarefa:
            raise ErroAoAtualizarTarefa(detail="Tarefa não encontrada", status_code=404)

        tarefa.atualizar(
            titulo=comando.titulo,
            descricao=comando.descricao,
            data_de_inicio=comando.data_de_inicio,
            data_de_fim=comando.data_de_fim,
            prioridade=comando.prioridade,
            status=comando.status,
        )

        repositorio.atualizar_tarefa(tarefa)

        uow.commit()

    return tarefa


# TODO: Retornar ID apenas
def deletar_tarefa(comando: DeletarTarefa, uow: UnidadeDeTrabalhoAbastrato) -> None:
    with uow:
        repo = RepositorioTarefas(uow.session)

        tarefa: Optional[Tarefa] = repo.buscar_por_id_de_usuario_e_id_de_tarefa(
            id_tarefa=comando.id_tarefa, id_usuario=comando.id_usuario
        )
        if not tarefa:
            raise ErroAoDeletarTarefa(detail="Tarefa não encontrada", status_code=404)

        repo.deletar_tarefa(comando.id_tarefa)

        uow.commit()
