from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from models_sqlite import Store, Coupon
from countries import get_countries_by_region, get_all_countries
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/")
@limiter.limit("60/minute")
async def get_stores(
    request: Request,
    region: Optional[str] = Query(None, regex="^(america|europe|asia)$"),
    country: Optional[str] = None,
    store_type: Optional[str] = Query(None, regex="^(retail|food_delivery|grocery)$"),
    category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all stores with filters
    """
    query = db.query(Store).filter(Store.is_active == True)
    
    # Apply filters
    if region:
        query = query.filter(Store.region == region)
    
    if country:
        query = query.filter(Store.country == country)
    
    if store_type:
        query = query.filter(Store.store_type == store_type)
    
    if category:
        query = query.filter(Store.category == category)
    
    if search:
        query = query.filter(Store.name.ilike(f"%{search}%"))
    
    # Get total count
    total = query.count()
    
    # Pagination
    stores = query.offset((page - 1) * limit).limit(limit).all()
    
    # Add active coupon count to each store
    stores_with_counts = []
    for store in stores:
        store_dict = {
            "id": store.id,
            "name": store.name,
            "slug": store.slug,
            "domain": store.domain,
            "logo_url": store.logo_url,
            "region": store.region,
            "country": store.country,
            "store_type": store.store_type,
            "category": store.category,
            "active_coupons_count": db.query(Coupon).filter(
                Coupon.store_id == store.id,
                Coupon.is_active == True
            ).count()
        }
        stores_with_counts.append(store_dict)
    
    return {
        "stores": stores_with_counts,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
        "filters": {
            "region": region,
            "country": country,
            "store_type": store_type,
            "category": category
        }
    }

@router.get("/countries")
@limiter.limit("60/minute")
async def get_countries(
    request: Request,
    region: Optional[str] = Query(None, regex="^(america|europe|asia)$")
):
    """
    Get all countries, optionally filtered by region
    """
    if region:
        countries = get_countries_by_region(region)
    else:
        countries = get_all_countries()
    
    return {
        "countries": [
            {"code": code, "name": name}
            for code, name in countries.items()
        ]
    }

@router.get("/{slug}")
@limiter.limit("60/minute")
async def get_store(
    request: Request,
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Get single store by slug with active coupons count
    """
    store = db.query(Store).filter(Store.slug == slug).first()
    
    if not store:
        return {"error": "Store not found"}, 404
    
    active_coupons_count = db.query(Coupon).filter(
        Coupon.store_id == store.id,
        Coupon.is_active == True
    ).count()
    
    return {
        "store": {
            "id": store.id,
            "name": store.name,
            "slug": store.slug,
            "domain": store.domain,
            "logo_url": store.logo_url,
            "region": store.region,
            "country": store.country,
            "store_type": store.store_type,
            "category": store.category,
            "active_coupons_count": active_coupons_count,
            "last_scraped_at": store.last_scraped_at
        }
    }

@router.get("/regions/stats")
@limiter.limit("60/minute")
async def get_region_stats(request: Request, db: Session = Depends(get_db)):
    """
    Get statistics for each region
    """
    stats = {}
    
    for region in ["america", "europe", "asia"]:
        store_count = db.query(Store).filter(
            Store.region == region,
            Store.is_active == True
        ).count()
        
        coupon_count = db.query(Coupon).join(Store).filter(
            Store.region == region,
            Store.is_active == True,
            Coupon.is_active == True
        ).count()
        
        stats[region] = {
            "stores": store_count,
            "coupons": coupon_count
        }
    
    return {"stats": stats}
