from database.db import SessionLocal
from database.models import Platform

db = SessionLocal()

platforms = ["Amazon", "Flipkart", "Myntra"]

for p in platforms:
    existing = db.query(Platform).filter_by(name=p).first()

    if not existing:
        db.add(Platform(name=p))
        print(f"{p} added to database")
    else:
        print(f"{p} already exists")

db.commit()
db.close()

print("Platform seeding completed")