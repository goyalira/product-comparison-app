from database.db import engine
from database import models

models.Base.metadata.create_all(bind=engine)

print("Tables created successfully")