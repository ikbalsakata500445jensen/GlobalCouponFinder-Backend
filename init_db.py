from database import init_db, SessionLocal
from models import Category, Store
from datetime import datetime

def seed_categories():
    db = SessionLocal()
    
    categories = [
        {"name": "Fashion & Apparel", "slug": "fashion", "icon": "👗"},
        {"name": "Electronics", "slug": "electronics", "icon": "💻"},
        {"name": "Beauty & Personal Care", "slug": "beauty", "icon": "💄"},
        {"name": "Home & Garden", "slug": "home-garden", "icon": "🏡"},
        {"name": "Food & Grocery", "slug": "food-grocery", "icon": "🍔"},
        {"name": "Food Delivery", "slug": "food-delivery", "icon": "🚚"},
        {"name": "Sports & Outdoors", "slug": "sports", "icon": "⚽"},
        {"name": "Toys & Kids", "slug": "toys-kids", "icon": "🧸"},
        {"name": "Books & Media", "slug": "books-media", "icon": "📚"},
        {"name": "Pet Supplies", "slug": "pet-supplies", "icon": "🐾"},
        {"name": "Health & Wellness", "slug": "health-wellness", "icon": "💊"},
        {"name": "Automotive", "slug": "automotive", "icon": "🚗"},
    ]
    
    for cat_data in categories:
        existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
        if not existing:
            category = Category(**cat_data)
            db.add(category)
    
    db.commit()
    print("Categories seeded successfully!")
    db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Seeding categories...")
    seed_categories()
    print("Database initialization complete!")
