import time

from fastapi import FastAPI, Request

from fastapi.responses import RedirectResponse
from libs.database.carregar_orm import carregar_tabelas
from libs.dominio.barramento import Barramento


app = FastAPI()


@app.get("/")
async def docs():
    return RedirectResponse(url="/docs")


## Cadastrar middleware
@app.middleware("tempo_de_resposta")
async def add_tempo_de_resposta(request: Request, call_next):
    timer_inicial = time.time()
    resposta = await call_next(request)
    tempo_de_processamento = time.time() - timer_inicial
    resposta.headers["X-Process-Time"] = str(tempo_de_processamento)
    return resposta


def registrar_rotas():
    from contexto.usuario.pontos_de_entrada.usuario import rota as usuario

    app.include_router(usuario)


def registrar_eventos_e_comandos():
    barramento = Barramento()

    from contexto.usuario.servicos.executores.usuario import (
        criar_usuario,
        atualizar_usuario,
        deletar_usuario,
    )
    from contexto.usuario.servicos.visualizadores.usuario import (
        obter_usuario_por_id,
        listar_usuarios,
    )

    from contexto.usuario.dominio.comandos.usuario import (
        CriarUsuario,
        AtualizarUsuario,
        ObterUsuario,
        ListarUsuarios,
        DeletarUsuario,
    )

    barramento.registrar_comando(CriarUsuario, criar_usuario)
    barramento.registrar_comando(AtualizarUsuario, atualizar_usuario)
    barramento.registrar_comando(DeletarUsuario, deletar_usuario)

    barramento.registrar_comando(ObterUsuario, obter_usuario_por_id)
    barramento.registrar_comando(ListarUsuarios, listar_usuarios)


carregar_tabelas()
registrar_rotas()
registrar_eventos_e_comandos()
app
