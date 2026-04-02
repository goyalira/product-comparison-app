from sqlalchemy.orm import Session
from .models import Product, Platform, Listing, PriceSnapshot


def get_or_create_product(db: Session, name: str, brand: str, category: str):

    product = db.query(Product).filter_by(
        name=name,
        brand=brand
    ).first()

    if product:
        return product

    product = Product(
        name=name,
        brand=brand,
        category=category
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_listing(db: Session, product_id: int, platform_id: int):

    return db.query(Listing).filter_by(
        product_id=product_id,
        platform_id=platform_id
    ).first()


def get_platform_by_name(db: Session, name: str):

    return db.query(Platform).filter_by(
        name=name
    ).first()


def create_listing(db: Session, product_id: int, platform_id: int, url: str):

    listing = Listing(
        product_id=product_id,
        platform_id=platform_id,
        product_url=url
    )

    db.add(listing)
    db.commit()
    db.refresh(listing)

    return listing


def add_price_snapshot(db: Session, listing_id: int, price: float, rating: float, delivery_time: int):

    if price is None:
        return None

    snapshot = PriceSnapshot(
        listing_id=listing_id,
        price=price,
        rating=rating,
        delivery_time_hours=delivery_time
    )

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot