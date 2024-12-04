from uuid import uuid4
from unittest.mock import patch

from contexto.usuario.dominio.entidades.usuario import Usuario
from contexto.usuario.dominio.modelos.usuario import Token
from contexto.usuario.dominio.objeto_de_valor.usuario import NivelDeAcesso
from contexto.usuario.dominio.comandos.usuario import (
    AtualizarNivelDeAcesso,
    AtualizarUsuario,
    CriarUsuario,
    DeletarUsuario,
    LoginUsuario,
)

from servidor.config import registrar_eventos_e_comandos
from libs.dominio.barramento import Barramento
from test.contexto.spy.uow import MockUoW


class MockRepositorio:
    def __init__(self, session=None):
        self.session = session

    def buscar_por_email_sem_retorno(self, email):
        return None

    def buscar_por_email_com_retorno(self, email):
        return Usuario.criar(
            nome="Nome",
            email=email,
            senha="senha",
            nivel_de_acesso=NivelDeAcesso.USUARIO,
        )

    def buscar_por_id(self, id):
        usuario = Usuario.criar(
            nome="Nome",
            email="example@email.com",
            senha="senha",
            nivel_de_acesso=NivelDeAcesso.USUARIO,
        )
        usuario.id = id
        return usuario

    def buscar_por_id_com_retorno_de_usuario_administrador(self, id):
        usuario = Usuario.criar(
            nome="Nome",
            email="email@email.com",
            senha="senha",
            nivel_de_acesso=NivelDeAcesso.ADMINISTRADOR,
        )
        usuario.id = id
        return usuario

    def salvar(self, usuario):
        return usuario

    def atualizar(self, usuario):
        return usuario

    def deletar(self, id_usuario):
        return None


def test_criar_usuario():

    registrar_eventos_e_comandos()

    comando = CriarUsuario(nome="Nome", email="email@example.com", senha="senha")

    uow = MockUoW()
    bus = Barramento()

    with patch(
        "contexto.usuario.servicos.executores.usuario.RepositorioUsuario.buscar_por_email",
        MockRepositorio.buscar_por_email_sem_retorno,
    ):

        with patch(
            "contexto.usuario.servicos.executores.usuario.RepositorioUsuario.salvar",
            MockRepositorio.salvar,
        ):

            usuario = bus.enviar_comando(comando, uow)

            assert usuario
            assert usuario.nome == "Nome"
            assert usuario.email == "email@example.com"
            assert usuario.nivel_de_acesso == NivelDeAcesso.USUARIO


def test_atualizar_usuario():

    registrar_eventos_e_comandos()

    uow = MockUoW()
    bus = Barramento()

    comando = AtualizarUsuario(
        id=uuid4(),
        nome="Novo Nome",
        email="novoemail@email.com",
        senha="NOVA SENHA",
    )

    with patch(
        "contexto.usuario.servicos.executores.usuario.RepositorioUsuario.buscar_por_id",
        MockRepositorio.buscar_por_id_com_retorno_de_usuario_administrador,
    ):

        with patch(
            "contexto.usuario.servicos.executores.usuario.RepositorioUsuario.atualizar",
            MockRepositorio.atualizar,
        ):

            retorno_comando: Usuario = bus.enviar_comando(comando, uow)

            assert retorno_comando is not None
            assert retorno_comando.nome == "Novo Nome"
            assert retorno_comando.email == "novoemail@email.com"
            assert retorno_comando.verificar_senha("NOVA SENHA") is True


def test_login_de_usuario():

    registrar_eventos_e_comandos()

    uow = MockUoW()
    bus = Barramento()

    comando = LoginUsuario(email="email@example.com", senha="senha")

    with patch(
        "contexto.usuario.servicos.executores.usuario.RepositorioUsuario.buscar_por_email",
        MockRepositorio.buscar_por_email_com_retorno,
    ):
        with patch.object(Usuario, "verificar_senha", return_value=True):

            token: Token = bus.enviar_comando(comando, uow)

            assert token is not None
            assert isinstance(token, Token)


def test_atualizar_nivel_de_acesso():

    registrar_eventos_e_comandos()

    uow = MockUoW()
    bus = Barramento()

    nivel_de_admin = NivelDeAcesso.ADMINISTRADOR

    comando = AtualizarNivelDeAcesso(
        id_usuario=uuid4(), id_admin=uuid4(), nivel_de_acesso=nivel_de_admin
    )

    with patch(
        "contexto.usuario.servicos.executores.usuario.RepositorioUsuario.buscar_por_id",
        MockRepositorio.buscar_por_id_com_retorno_de_usuario_administrador,
    ):

        with patch(
            "contexto.usuario.servicos.executores.usuario.RepositorioUsuario.atualizar",
            MockRepositorio.atualizar,
        ):

            usuario: Usuario = bus.enviar_comando(comando, uow)

            assert usuario is not None
            assert usuario.nivel_de_acesso == NivelDeAcesso.ADMINISTRADOR


def test_deletar_usuario():

    registrar_eventos_e_comandos()

    uow = MockUoW()
    bus = Barramento()

    comando = DeletarUsuario(id_admin=uuid4(), id_usuario=uuid4())

    with patch(
        "contexto.usuario.servicos.executores.usuario.RepositorioUsuario.buscar_por_id",
        MockRepositorio.buscar_por_id_com_retorno_de_usuario_administrador,
    ):

        with patch(
            "contexto.usuario.servicos.executores.usuario.RepositorioUsuario.atualizar",
            MockRepositorio.atualizar,
        ):

            resultado: Usuario = bus.enviar_comando(comando, uow)

            assert resultado.id == comando.id_usuario
            assert resultado.deletado_em is not None
            assert resultado is not None
