from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import login_service

router = APIRouter()

@router.post("/")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Maneja la autenticación del usuario, verificando las credenciales y devolviendo un token JWT.

    :param form_data: Datos del formulario (nombre de usuario y contraseña).
    :return: Diccionario con el token de acceso.
    :raises HTTPException: Si las credenciales son incorrectas.
    """
    token = login_service(form_data.username, form_data.password)
    return {"access_token": token}

