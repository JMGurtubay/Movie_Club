from typing import List
from app.database.connection import db
from app.models.theater import TheaterDB
from app.schemas.theater import TheaterRequest
from pymongo.errors import PyMongoError
from bson import ObjectId

theaters_collection = db["theaters"]

def get_all_theaters_service() -> List[TheaterDB]:
    try:
        print('Entra al servicio')
        theaters_cursor = theaters_collection.find({})
        print('lista de peliculas')
        theaters = [
            TheaterDB(
                id=str(theater["_id"]),
                name=theater["name"],
                max_capacity=theater["max_capacity"],
                projection=theater["projection"],
                screen_size=theater["screen_size"],
                description=theater["description"],
            )
            for theater in theaters_cursor
        ]
        return theaters
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def get_theater_by_id_service(theater_id: str) -> TheaterDB:
    try:
        theater = theaters_collection.find_one({"_id": ObjectId(theater_id)})
        if not theater:
            return None
        return TheaterDB(
            id=str(theater["_id"]),
            name=theater["name"],
            max_capacity=theater["max_capacity"],
            projection=theater["projection"],
            screen_size=theater["screen_size"],
            description=theater["description"],
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def create_theater_service(theater_data: TheaterRequest):
    try:
        result = theaters_collection.insert_one(theater_data.model_dump(exclude={"id"}))

        created_theater = theaters_collection.find_one({"_id": result.inserted_id})

        return TheaterDB(
            id=str(created_theater["_id"]),
            name=created_theater["name"],
            max_capacity=created_theater["max_capacity"],
            projection=created_theater["projection"],
            screen_size=created_theater["screen_size"],
            description=created_theater["description"],
        )

    except PyMongoError as e:
        print('Mongo')
        raise RuntimeError(f"Database error: {str(e)}")

def update_theater_service(theater_id: str, theater_data: TheaterRequest) -> TheaterDB:
    try:
        # Actualizar el documento en MongoDB
        result = theaters_collection.update_one(
            {"_id": ObjectId(theater_id)},
            {"$set": theater_data.model_dump(exclude={"id"})}
        )

        # Verificar si se modificó algún documento
        if result.matched_count == 0:
            raise ValueError(f"No se encontró ninguna película con el ID proporcionado: {theater_id}")

        # Obtener la película actualizada para regresarla como respuesta
        updated_theater = theaters_collection.find_one({"_id": ObjectId(theater_id)})

        # Convertir el resultado a un objeto TheaterDB
        return TheaterDB(**updated_theater)
        
    except PyMongoError as e:
        print('Mongo')
        raise RuntimeError(f"Database error: {str(e)}")

def delete_theater_service(theater_id: str) -> bool:
    try:

        # Intentar eliminar la película de la base de datos
        result = theaters_collection.delete_one({"_id": ObjectId(theater_id)})

        # Verificar si se eliminó algún documento
        if result.deleted_count == 0:
            raise ValueError(f"No se encontró ninguna película con el ID proporcionado: {theater_id}")

        return True  # Indica que la película fue eliminada exitosamente

    except PyMongoError as e:
        print('Mongo')
        raise RuntimeError(f"Database error: {str(e)}")

