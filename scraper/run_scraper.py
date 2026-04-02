from database.db import SessionLocal
from database import crud
from scraper.amazon_scraper import scrape_amazon

# Dummy data for Flipkart
FLIPKART_DUMMY_PRODUCTS = [
    {"name": "iPhone 15", "price": 97000, "rating": 4.5, "brand": "Apple", "category": "Electronics", "url": "https://www.flipkart.com/iphone-15"},
    {"name": "Samsung Galaxy S23", "price": 75000, "rating": 4.4, "brand": "Samsung", "category": "Electronics", "url": "https://www.flipkart.com/samsung-galaxy-s23"},
    {"name": "Gaming Laptop XYZ", "price": 120000, "rating": 4.6, "brand": "Dell", "category": "Electronics", "url": "https://www.flipkart.com/gaming-laptop-xyz"},
]

def run_scraper():
    db = SessionLocal()

    # Platform names in DB
    platform_names = ["Amazon", "Flipkart"]

    # Queries to demo
    queries = ["iphone", "samsung phone", "gaming laptop", "nike shoes"]

    for platform_name in platform_names:
        platform = crud.get_platform_by_name(db, platform_name)
        if not platform:
            print(f"{platform_name} not found in DB. Seed platforms first.")
            continue

        if platform_name == "Amazon":
            # LIVE scraping for Amazon
            for query in queries:
                print(f"\nScraping {platform_name} for: {query}")
                scraped_products = scrape_amazon(query)

                for item in scraped_products:
                    # 1️⃣ Get or create product
                    product = crud.get_or_create_product(
                        db=db,
                        name=item.get("name"),
                        brand=item.get("brand", "Unknown"),
                        category=item.get("category", "General")
                    )

                    # 2️⃣ Get or create listing with actual URL
                    listing = crud.get_listing(
                        db=db,
                        product_id=product.id,
                        platform_id=platform.id
                    )
                    if not listing:
                        listing = crud.create_listing(
                            db=db,
                            product_id=product.id,
                            platform_id=platform.id,
                            url=item.get("url")  # use actual Amazon URL
                        )

                    # 3️⃣ Add price snapshot
                    crud.add_price_snapshot(
                        db=db,
                        listing_id=listing.id,
                        price=item.get("price"),
                        rating=item.get("rating"),
                        delivery_time=48  # placeholder
                    )

                    print(f"Inserted: {item.get('name')} ({platform_name})")

        elif platform_name == "Flipkart":
            # INSERT dummy data for Flipkart
            print(f"\nAdding dummy data for {platform_name}")
            for item in FLIPKART_DUMMY_PRODUCTS:
                product = crud.get_or_create_product(
                    db=db,
                    name=item.get("name"),
                    brand=item.get("brand"),
                    category=item.get("category")
                )
                listing = crud.get_listing(db, product.id, platform.id)
                if not listing:
                    listing = crud.create_listing(
                        db=db,
                        product_id=product.id,
                        platform_id=platform.id,
                        url=item.get("url")  # use dummy Flipkart URL
                    )
                crud.add_price_snapshot(
                    db=db,
                    listing_id=listing.id,
                    price=item.get("price"),
                    rating=item.get("rating"),
                    delivery_time=72  # placeholder for Flipkart
                )
                print(f"Inserted: {item.get('name')} ({platform_name})")

    db.close()


if __name__ == "__main__":
    run_scraper()