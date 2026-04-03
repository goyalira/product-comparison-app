import json
from database.db import SessionLocal
from database import crud

def load_products():

    db = SessionLocal()
    with open("data/products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    for item in products:
        platform = crud.get_platform_by_name(db, item["platform"])

        if not platform:
            print(f"{item['platform']} not found")
            continue

        product = crud.get_or_create_product(
            db=db,
            name=item["name"],
            brand="Unknown",
            category="General"
        )

        listing = crud.get_listing(db, product.id, platform.id)

        if not listing:
            listing = crud.create_listing(
                db=db,
                product_id=product.id,
                platform_id=platform.id,
                url=item["url"]
            )

        crud.add_price_snapshot(
            db=db,
            listing_id=listing.id,
            price=item["price"],
            rating=item["rating"],
            delivery_time=48
        )

        print(f"Inserted: {item['name']}")

    db.close()
    print(" Data loaded successfully")


if __name__ == "__main__":
    load_products()
