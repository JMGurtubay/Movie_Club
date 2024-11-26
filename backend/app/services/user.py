from typing import List
from app.database.connection import db
from app.models.user import UserDB
from app.schemas.user import UserRequest
from pymongo.errors import PyMongoError
from bson import ObjectId

users_collection = db["users"]

def get_all_users_service() -> List[UserDB]:
    try:
        users_cursor = users_collection.find({})
        users = [
            UserDB(
                id=str(user["_id"]),
                username=user["username"],
                password=user["password"],
                email=user["email"]
            )
            for user in users_cursor
        ]
        return users
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def get_user_by_id_service(user_id: str) -> UserDB:
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None
        return UserDB(
            id=str(user["_id"]),
            username=user["username"],
            password=user["password"],
            email=user["email"]

        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def create_user_service(user_data: UserRequest)-> UserDB:
    try:
        result = users_collection.insert_one(user_data.model_dump(exclude={"id"}))

        created_user = users_collection.find_one({"_id": result.inserted_id})

        return UserDB(
            id=str(created_user["_id"]),
            username=created_user["username"],
            password=created_user["password"],
            email=created_user["email"]
            
        )

    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def update_user_service(user_id: str, user_data: UserRequest) -> UserDB:
    try:
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user_data.model_dump(exclude={"id"})}
        )

        if result.matched_count == 0:
            raise ValueError(f"No se encontró ningun usuario con el ID proporcionado: {user_id}")

        updated_user = users_collection.find_one({"_id": ObjectId(user_id)})

        return UserDB(**updated_user)
        
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def delete_user_service(user_id: str) -> bool:
    try:

        result = users_collection.delete_one({"_id": ObjectId(user_id)})

        if result.deleted_count == 0:
            raise ValueError(f"No se encontró ningun usuario con el ID proporcionado: {user_id}")

        return True  

    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

