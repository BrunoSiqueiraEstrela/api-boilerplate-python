import os
from jose import JWTError, jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

SECRET_KEY = os.environ.get("SECRET_KEY", "senha-secreta")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE", 120))


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme"
                )

            dados_token = self.verificar_jwt(credentials.credentials)
            if not dados_token:
                raise HTTPException(status_code=403, detail="Invalid token")

            from contexto.usuario.dominio.entidades.usuario import Usuario
            from libs.database.config import conectar

            db = conectar()
            usuario = (
                db.query(Usuario)
                .filter(Usuario.id == (dados_token.get("sub", "sem-id-no-sub?")))
                .first()
            )
            if not usuario:
                raise HTTPException(status_code=403, detail="Invalid token")

            usuario: Usuario
            if not usuario.ativo:
                raise HTTPException(status_code=403, detail="Usuario desativado")

            if usuario.deletado_em:
                raise HTTPException(status_code=403, detail="Usuario deletado")

            return usuario
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code")

    def verificar_jwt(self, jwt_token: str):
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return False
