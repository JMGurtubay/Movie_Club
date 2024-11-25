# services/reservation_service.py
from datetime import datetime
from typing import List
from app.shared.utils import convert_time_to_datetime
from pymongo.errors import PyMongoError
from bson import ObjectId
from app.models.reservation import ReservationDB
from app.schemas.reservation import ReservationRequest
from app.database.connection import db

reservations_collection = db["reservations"]

def get_all_reservations_service() -> List[ReservationDB]:
    try:
        reservations_cursor = reservations_collection.find({})
        reservations = [
            ReservationDB(
                id=str(reservation["_id"]),
                user_id=reservation["user_id"],
                theater_id=str(reservation["theater_id"]),
                movie_id=str(reservation["movie_id"]),
                is_private=reservation["is_private"],
                start_time=reservation["start_time"],
                end_time=reservation["end_time"],
                reservation_date=reservation["reservation_date"],
                status=reservation["status"],
            )
            for reservation in reservations_cursor
        ]
        return reservations
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def get_reservation_by_id_service(reservation_id: str) -> ReservationDB:
    try:
        reservation = reservations_collection.find_one({"_id": ObjectId(reservation_id)})
        if not reservation:
            return None
        return ReservationDB(
            id=str(reservation["_id"]),
            user_id=reservation["user_id"],
            theater_id=str(reservation["theater_id"]),
            movie_id=str(reservation["movie_id"]),
            is_private=reservation["is_private"],
            start_time=reservation["start_time"],
            end_time=reservation["end_time"],
            reservation_date=reservation["reservation_date"],
            status=reservation["status"],
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def create_reservation_service(reservation_data: ReservationRequest) -> ReservationDB:
    try:
        # Validar y convertir ObjectId
        reservation_data.validate_fields()

        # Preparar los datos para la inserción
        reservation_dict = reservation_data.model_dump(exclude={"id"})
        reservation_dict["theater_id"] = ObjectId(reservation_dict["theater_id"])
        reservation_dict["movie_id"] = ObjectId(reservation_dict["movie_id"])
        reservation_dict["start_time"]= datetime.combine(reservation_dict["reservation_date"].date(), reservation_dict["start_time"].time())
        reservation_dict["end_time"]= datetime.combine(reservation_dict["reservation_date"].date(), reservation_dict["end_time"].time())

        # Insertar reservación
        result = reservations_collection.insert_one(reservation_dict)

        # Recuperar la reservación creada
        created_reservation = reservations_collection.find_one({"_id": result.inserted_id})

        return ReservationDB(
            id=str(created_reservation["_id"]),
            user_id=created_reservation["user_id"],
            theater_id=str(created_reservation["theater_id"]),
            movie_id=str(created_reservation["movie_id"]),
            is_private=created_reservation["is_private"],
            start_time=created_reservation["start_time"],  # Solo hora
            end_time=created_reservation["end_time"],      # Solo hora
            reservation_date=created_reservation["reservation_date"].strftime("%Y-%m-%d"),  # Solo fecha
            status=created_reservation["status"],
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def update_reservation_service(reservation_id: str, reservation_data: ReservationRequest) -> ReservationDB:
    try:
        reservation_data.validate_fields()
        reservation_dict = reservation_data.model_dump()
        reservation_dict["theater_id"] = ObjectId(reservation_dict["theater_id"])
        reservation_dict["movie_id"] = ObjectId(reservation_dict["movie_id"])
        # Actualizar el documento en MongoDB

        result = reservations_collection.update_one(
            {"_id": ObjectId(reservation_id)},
            {"$set": reservation_data.model_dump()}
        )

        # Verificar si se modificó algún documento
        if result.matched_count == 0:
            raise ValueError(f"No se encontró ninguna película con el ID proporcionado: {reservation_id}")

        # Obtener la película actualizada para regresarla como respuesta
        updated_reservation = reservations_collection.find_one({"_id": ObjectId(reservation_id)})
        # Convertir los campos para que sean válidos en el modelo ReservationDB
        formatted_reservation = {
            "user_id": updated_reservation["user_id"],
            "theater_id": str(updated_reservation["theater_id"]),  # Convertir ObjectId a str
            "movie_id": str(updated_reservation["movie_id"]),      # Convertir ObjectId a str
            "is_private": updated_reservation["is_private"],
            "start_time": updated_reservation["start_time"],
            "end_time": updated_reservation["end_time"],
            "reservation_date": updated_reservation["reservation_date"],
            "status": updated_reservation["status"],
        }
        # Crear y devolver el modelo
        return ReservationDB(**formatted_reservation)

        
    except PyMongoError as e:
        print('Mongo')
        raise RuntimeError(f"Database error: {str(e)}")

def delete_reservation_service(reservation_id: str) -> bool:
    try:

        # Intentar eliminar la película de la base de datos
        result = reservations_collection.delete_one({"_id": ObjectId(reservation_id)})

        # Verificar si se eliminó algún documento
        if result.deleted_count == 0:
            raise ValueError(f"No se encontró ninguna película con el ID proporcionado: {reservation_id}")

        return True  # Indica que la película fue eliminada exitosamente

    except PyMongoError as e:
        print('Mongo')
        raise RuntimeError(f"Database error: {str(e)}")
