from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import List, Optional, Dict, Union
from app.models.user import UserDB


from pydantic import BaseModel, Field, EmailStr, root_validator
import re

from pydantic import BaseModel, Field, EmailStr, model_validator
import re

class UserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="El nombre de usuario debe tener entre 3 y 50 caracteres.")
    password: str
    email: str

    @model_validator(mode="before")
    @classmethod
    def validate_password_and_email(cls, values):
        password = values.get("password")
        email = values.get("email")

        # Validación de la contraseña
        password_pattern = (
            r'^(?=.*[a-z])'        # Al menos una letra minúscula
            r'(?=.*[A-Z])'         # Al menos una letra mayúscula
            r'(?=.*\d)'            # Al menos un número
            r'(?=.*[@$!%*?&#])'    # Al menos un símbolo especial
            r'[A-Za-z\d@$!%*?&#]{8,}$'  # Mínimo 8 caracteres
        )
        if not re.match(password_pattern, password):
            raise ValueError("La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula, un número y un símbolo especial.")

        # Validación del correo electrónico
        email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
        if not re.match(email_pattern, email):
            raise ValueError("El correo electrónico debe ser válido, incluyendo un '@' y un dominio como '.com'.")

        return values

    model_config = ConfigDict(
        json_schema_extra= {
            "example": {
                "username": "user123",
                "password": "Pa$$w0rd",
                "email": "user123@example.com"
            }
        }
    )



class UserResponse(BaseModel):
    code: int
    message: str
    description: str
    data: Optional[Union[UserDB, Dict, List[UserDB]]] = None