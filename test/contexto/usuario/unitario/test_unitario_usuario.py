from contexto.usuario.dominio.entidades.usuario import Usuario


# primeiro teste
def test_criacao_de_usuario():

    usuario = Usuario.criar(
        nome="João", email="email@email.com", senha="123456", nivel_de_acesso="USUARIO"
    )

    assert usuario is not None
    assert usuario.nome == "João"
    assert usuario.email == "email@email.com"
    assert usuario.senha == "123456"
    assert usuario.nivel_de_acesso == "USUARIO"


def test_atualizacao_de_usuario():

    usuario = Usuario.criar(
        nome="João", email="email@email", senha="123456", nivel_de_acesso="USUARIO"
    )

    usuario.atualizar(
        nome="João da Silva",
        email="novo@email",
        senha="654321",
        nivel_de_acesso="ADMIN",
    )

    assert usuario.nome == "João da Silva"
    assert usuario.email == "novo@email"
    assert usuario.senha == "654321"
    assert usuario.nivel_de_acesso == "ADMIN"
