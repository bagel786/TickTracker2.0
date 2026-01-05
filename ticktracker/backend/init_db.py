from database import engine
from models import Base
import models # Make sure models are imported so they are registered with Base

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
