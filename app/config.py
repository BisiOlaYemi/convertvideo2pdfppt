from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "video_converter"
    TEMP_DIR: str = "temp"
    FRAMES_DIR: str = "temp/frames"

settings = Settings()