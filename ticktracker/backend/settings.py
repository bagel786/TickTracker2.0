from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "TickTracker"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = "sqlite:///./ticktracker.db"
    
    # Ticketmaster
    TICKETMASTER_API_KEY: str = "wAuWTTAqVrinFxhiIICRxvBwi9yGITx8"
    TICKETMASTER_SECRET: str = "O6FS15jiQfB0kRS7"
    
    # Eventbrite
    EVENTBRITE_API_KEY: str = "QLG3DZ2MCKEKDPPJ2F"
    EVENTBRITE_CLIENT_SECRET: str = "PBT7A4BOO6JP62LBW6NBLVMKDNVUFQ5GNXURBL7IUHQOXALLRK"
    EVENTBRITE_PRIVATE_TOKEN: str = "CGNUNTMTDEFCPGVZMORP"
    EVENTBRITE_PUBLIC_TOKEN: str = "ZDSNSVD4JID5ZI24DXEV"
    
    # SeatGeek - Sign up at https://platform.seatgeek.com/ to get your client ID
    SEATGEEK_CLIENT_ID: str = "NTQ1NDE0ODN8MTc2Mzg0NTI3OC43MjQ0OTE4"
    SEATGEEK_CLIENT_SECRET: str = "e81000383a0cb87a6d01f008b34d7e3dfea876c973ddbab5c1f2543edacac2c9"
    
    class Config:
        env_file = ".env"

settings = Settings()
