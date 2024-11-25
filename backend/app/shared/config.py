from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MONGO_URI: str = "mongodb://database:27017"
    MONGO_URI: str = "mongodb://localhost:27017/movie_club"

settings = Settings()
