# TODO: Implementar rotas de usuário
# CREATED USUARIO

from typing import List
from uuid import UUID
from fastapi import APIRouter

from contexto.usuario.dominio.comandos.usuario import (
    CriarUsuario,
    ObterUsuario,
    ListarUsuarios,
    AtualizarUsuario,
    DeletarUsuario,
)
from contexto.usuario.dominio.entidades.usuario import Usuario
from contexto.usuario.dominio.modelos.usuario import (
    CriarUsuarioEntrada,
    AtualizarUsuarioEntrada,
    SaidaUsuario,
)
from libs.dominio.barramento import Barramento
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalho
from libs.tipos.retorno import RetornoApenasId, RetornoDeDados


rota = APIRouter(tags=["Usuarios"])


# GET USUARIO
@rota.get("/usuario/one/{id}", status_code=200)
def obter_usuario(id: UUID) -> RetornoDeDados[SaidaUsuario]:
    unidadeDeTrabalho = UnidadeDeTrabalho()
    barramento = Barramento()

    comando = ObterUsuario(id=id)
    retorno_comando: Usuario = barramento.enviar_comando(comando, unidadeDeTrabalho)

    return RetornoDeDados(
        dado=SaidaUsuario(
            id=retorno_comando.id,
            nome=retorno_comando.nome,
            email=retorno_comando.email,
            nivel_de_acesso=retorno_comando.nivel_de_acesso,
            criado_em=retorno_comando.criado_em,
            atualizado_em=retorno_comando.atualizado_em,
        )
    )


# QUERY USUARIO
# LISTAR USUARIOS
@rota.get("/usuario/listar/", status_code=200)
def listar_usuarios() -> RetornoDeDados[List[SaidaUsuario]]:
    unidadeDeTrabalho = UnidadeDeTrabalho()
    barrramento = Barramento()

    comando = ListarUsuarios()
    retorno_usuarios: List[Usuario] = barrramento.enviar_comando(
        comando, unidadeDeTrabalho
    )

    # retorna a lista de usuarios
    return RetornoDeDados(
        dado=[
            SaidaUsuario(
                id=usuario.id,
                nome=usuario.nome,
                email=usuario.email,
                nivel_de_acesso=usuario.nivel_de_acesso,
                criado_em=usuario.criado_em,
                atualizado_em=usuario.atualizado_em,
            )
            for usuario in retorno_usuarios
        ]
    )


# POST USUARIO
@rota.post("/usuario", status_code=201)
def criar_usuario(entrada: CriarUsuarioEntrada) -> RetornoApenasId[UUID]:
    unidadeDeTrabalho = UnidadeDeTrabalho()
    barrramento = Barramento()

    comando = CriarUsuario(
        nome=entrada.nome,
        email=entrada.email,
        senha=entrada.senha,
        nivel_de_acesso=entrada.nivel_de_acesso,
    )
    retorno_comando: Usuario = barrramento.enviar_comando(comando, unidadeDeTrabalho)

    return RetornoApenasId(id=retorno_comando.id)


# UPDATE USUARIO
@rota.put("/usuario/{id}", status_code=200)
def atualizar_usuario(
    id: UUID, entrada: AtualizarUsuarioEntrada
) -> RetornoApenasId[UUID]:
    unidadeDeTrabalho = UnidadeDeTrabalho()
    barrramento = Barramento()

    comando = AtualizarUsuario(
        id=id,
        nome=entrada.nome,
        email=entrada.email,
        senha=entrada.senha,
        nivel_de_acesso=entrada.nivel_de_acesso,
    )
    retorno_comando: Usuario = barrramento.enviar_comando(comando, unidadeDeTrabalho)

    return RetornoApenasId(id=retorno_comando.id)


# DELETE USUARIO
@rota.delete("/usuario/{id}", status_code=204)
def deletar_usuario(id: UUID) -> None:
    unidadeDeTrabalho = UnidadeDeTrabalho()
    barrramento = Barramento()

    comando = DeletarUsuario(id=id)

    barrramento.enviar_comando(comando, unidadeDeTrabalho)
    return None
