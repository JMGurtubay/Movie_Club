from app.models.user import UserDB
from pymongo import MongoClient
from app.database.connection import db
from fastapi import HTTPException
from app.shared.utils import encode_token

users_collection = db["users"]

def login_service(username: str, password: str) -> str:
    """
    Verifica las credenciales del usuario y genera un token si son válidas.

    :param username: Nombre de usuario proporcionado.
    :param password: Contraseña proporcionada.
    :return: Token JWT si las credenciales son válidas.
    :raises HTTPException: Si las credenciales son incorrectas.
    """
    user = users_collection.find_one({"username": username})
    if not user or password != user["password"]:
        raise HTTPException(status_code=400, detail="Nombre de usuario o contraseña incorrectos.")
    
    # Generar el token
    token = encode_token({"username":user["username"], "email":user["email"]})
    return token
