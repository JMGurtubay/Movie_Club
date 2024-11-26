from fastapi import APIRouter, HTTPException
from app.services.user import get_all_users_service, get_user_by_id_service, create_user_service, update_user_service, delete_user_service
from app.schemas.user import UserRequest, UserResponse
from app.shared.utils import validate_object_id, validate_user_unique
from app.shared.exceptions import BusinessLogicError

router = APIRouter()

@router.get("/", response_model=UserResponse)
def get_users():
    """
    Obtiene la lista de todos los usuarios.

    Parámetros:
        - Ninguno.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Lista de usuarios obtenidos.
    """
    try:
        users = get_all_users_service()
        return UserResponse(
            code=200,
            message="Usuarios obtenidos con éxito.",
            description="Se obtuvo correctamente la lista de usuarios.",
            data=users
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    """
    Obtiene un usuario específica por su ID.

    Parámetros:
        - user_id (str): ID del usuario a buscar.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Datos del usuario encontrado.
    """
    try:
        validate_object_id(user_id)  # Validar que el ID sea un ObjectId válido
        user = get_user_by_id_service(user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail={
                    "message": "Usuario no encontrado.",
                    "description": "No se encontró un usuario con el ID proporcionado."
                }
            )
        return UserResponse(
            code=200,
            message="Usuario obtenido con éxito.",
            description="Se obtuvo correctamente el usuario solicitado.",
            data=user
        )
    except HTTPException:
        raise
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error en la base de datos.",
                "description": str(e)
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error inesperado en el servidor.",
                "description": str(e)
            }
        )


@router.post("/", response_model=UserResponse)
def create_user(user: UserRequest):
    """
    Crea una nuevo usuario en la base de datos.

    Parámetros:
        - user (UserRequest): Objeto con los datos del usuario a crear.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Objeto con los datos del usuario creado.
    """
    try:
        validate_user_unique(user.username, user.email)
        created_user = create_user_service(user)

        return UserResponse(
            code=200,
            message="El usuario ha sido creada exitosamente.",
            description="El usuario ha sido añadida correctamente a la base de datos.",
            data=created_user
        )
    except ValueError as e:
        error_data = e.args[0]
        raise BusinessLogicError(
            message=error_data["message"],
            description=error_data["description"],
            data=error_data["data"]
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user: UserRequest):
    """
    Actualiza un usuario existente en la base de datos.

    Parámetros:
        - user_id (str): ID de el usuario a actualizar.
        - user (UserRequest): Objeto con los datos actualizados del usuario.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Objeto con los datos del usuario actualizada.
    """
    try:
        validate_object_id(user_id)
        validate_user_unique(user.username, user.email)
        updated_user = update_user_service(user_id, user)
        return UserResponse(
            code=200,
            message="El usuario ha sido actualizado exitosamente.",
            description="Los datos de el usuario se han modificado correctamente.",
            data=updated_user
        )
    except ValueError as e:
        error_data = e.args[0]
        raise BusinessLogicError(
            message=error_data["message"],
            description=error_data["description"],
            data=error_data["data"]
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: str):
    """
    Elimina un usuario de la base de datos por su ID.

    Parámetros:
        - user_id (str): ID de el usuario a eliminar.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Ninguno.
    """
    try:
        validate_object_id(user_id)
        delete_user_service(user_id)
        return UserResponse(
            code=200,
            message="El usuario ha sido eliminada exitosamente.",
            description="Se eliminó correctamente el usuario de la base de datos.",
            data=None
        )
    except HTTPException:
        raise
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error en la base de datos.",
                "description": str(e)
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error inesperado en el servidor.",
                "description": str(e)
            }
        )
