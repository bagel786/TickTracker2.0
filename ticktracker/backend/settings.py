from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "TickTracker"
    API_V1_STR: str = "/api"
    
    # Database - Use /tmp for reliable write permissions in ephemeral containers
    DATABASE_URL: str = "sqlite:////tmp/ticktracker.db"
    
    # Ticketmaster - Get your keys at https://developer.ticketmaster.com/
    TICKETMASTER_API_KEY: Optional[str] = ""
    TICKETMASTER_SECRET: str = ""
    
    # Eventbrite - Get your keys at https://www.eventbrite.com/platform/api
    EVENTBRITE_API_KEY: str = ""
    EVENTBRITE_CLIENT_SECRET: str = ""
    EVENTBRITE_PRIVATE_TOKEN: str = ""
    EVENTBRITE_PUBLIC_TOKEN: str = ""
    
    # SeatGeek - Sign up at https://platform.seatgeek.com/ to get your client ID
    SEATGEEK_CLIENT_ID: Optional[str] = ""
    SEATGEEK_CLIENT_SECRET: str = ""
    
    # CORS Origins (comma-separated list for production)
    CORS_ORIGINS: str = "*"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
