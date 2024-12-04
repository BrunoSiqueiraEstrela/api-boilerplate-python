from datetime import datetime, timedelta
from uuid import uuid4
from contexto.tarefa.dominio.entidades.tarefa import Tarefa
from unittest.mock import MagicMock, patch
from contexto.tarefa.dominio.objeto_de_valor.tarefa import StatusDaTarefa
from contexto.tarefa.repositorios.repo.tarefa import RepositorioTarefas
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalho
from servidor.config import registrar_eventos_e_comandos
from test.contexto.spy.uow import MockUoW
from contexto.tarefa.dominio.comandos.tarefa import (
    AtualizarTarefa,
    CriarTarefa,
    DeletarTarefa,
)
from libs.dominio.barramento import Barramento


class MockRepositorioTarefas:
    def __init__(self, session=None):
        self.session = session

    def adicionar_tarefa(self, tarefa):
        return tarefa

    def atualizar(self, tarefa):
        return tarefa

    def buscar_usuario_por_id(self, usuario):
        return usuario

    def remover(self, id_tarefa):
        return True

    def buscar_por_id_de_usuario_e_id_de_tarefa(*args, **kwargs):
        HORA_INICIO = datetime.now() - timedelta(hours=8)
        HORA_FIM = datetime.now() - timedelta(hours=4)
        return Tarefa.criar(
            id_usuario=uuid4(),
            titulo="titulo antigo",
            descricao="descricao antiga",
            data_de_inicio=HORA_INICIO,
            data_de_fim=HORA_FIM,
            prioridade=10,
            status=StatusDaTarefa.ATRASADO,
        )


# Erro ao criar teste, necessario usar path com with


def test_service_criar_tarefa():

    registrar_eventos_e_comandos()

    HORA_INICIO = datetime.now() - timedelta(hours=8)
    HORA_FIM = datetime.now() - timedelta(hours=4)

    comando = CriarTarefa(
        id_usuario=uuid4(),
        titulo="titulo",
        descricao="descricao",
        data_de_inicio=HORA_INICIO,
        data_de_fim=HORA_FIM,
        prioridade=1,
        status=StatusDaTarefa.PENDENTE,
    )

    uow = MockUoW()
    bus = Barramento()

    with patch(
        "contexto.tarefa.repositorios.repo.tarefa.RepositorioTarefas.adicionar_tarefa",
        MockRepositorioTarefas.adicionar_tarefa,
    ) as mock:

        with patch(
            "contexto.tarefa.repositorios.repo.tarefa.RepositorioTarefas.buscar_usuario_por_id",
            MockRepositorioTarefas.buscar_usuario_por_id,
        ) as mock:
            tarefa = bus.enviar_comando(comando, uow)

            assert tarefa is not None
            assert tarefa.titulo == "titulo"
            assert tarefa.descricao == "descricao"
            assert tarefa.data_de_inicio == HORA_INICIO
            assert tarefa.data_de_fim == HORA_FIM
            assert tarefa.prioridade == 1
            assert tarefa.status == StatusDaTarefa.PENDENTE


def test_service_atualizar_tarefa():

    registrar_eventos_e_comandos()

    HORA_INICIO = datetime.now() - timedelta(hours=8)
    HORA_FIM = datetime.now() - timedelta(hours=4)

    comando = AtualizarTarefa(
        id_usuario=uuid4(),
        id_tarefa=uuid4(),
        titulo="titulo",
        descricao="descricao",
        data_de_inicio=HORA_INICIO,
        data_de_fim=HORA_FIM,
        prioridade=1,
        status=StatusDaTarefa.PENDENTE,
    )

    uow = MockUoW()
    bus = Barramento()
    # import contexto.tarefa.repositorios.repo.tarefa

    with patch(
        "contexto.tarefa.repositorios.repo.tarefa.RepositorioTarefas.buscar_por_id_de_usuario_e_id_de_tarefa",
        MockRepositorioTarefas.buscar_por_id_de_usuario_e_id_de_tarefa,
    ) as mock:

        with patch(
            "contexto.tarefa.repositorios.repo.tarefa.RepositorioTarefas.atualizar_tarefa",
            MockRepositorioTarefas.atualizar,
        ) as mock:

            tarefa = bus.enviar_comando(comando, uow)

            assert tarefa is not None
            assert tarefa.titulo == "titulo"
            assert tarefa.descricao == "descricao"
            assert tarefa.data_de_inicio == HORA_INICIO
            assert tarefa.data_de_fim == HORA_FIM
            assert tarefa.prioridade == 1
            assert tarefa.status == StatusDaTarefa.PENDENTE


def test_service_deletar_tarefa():

    registrar_eventos_e_comandos()

    comando = DeletarTarefa(
        id_usuario=uuid4(),
        id_tarefa=uuid4(),
    )

    uow = MockUoW()

    bus = Barramento()

    with patch(
        "contexto.tarefa.repositorios.repo.tarefa.RepositorioTarefas.buscar_por_id_de_usuario_e_id_de_tarefa",
        MockRepositorioTarefas.buscar_por_id_de_usuario_e_id_de_tarefa,
    ) as mock:

        with patch(
            "contexto.tarefa.repositorios.repo.tarefa.RepositorioTarefas.deletar_tarefa",
            MockRepositorioTarefas.remover,
        ) as mock:

            bus.enviar_comando(comando, uow)

            assert True
