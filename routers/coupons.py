from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from models import Store, Coupon
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/")
@limiter.limit("60/minute")
async def get_coupons(
    request: Request,
    region: Optional[str] = Query(None, regex="^(america|europe|asia)$"),
    country: Optional[str] = None,
    store_slug: Optional[str] = None,
    store_type: Optional[str] = Query(None, regex="^(retail|food_delivery|grocery)$"),
    category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all coupons with filters
    """
    query = db.query(Coupon).filter(Coupon.is_active == True)
    
    # Join with Store to filter by store attributes
    query = query.join(Store)
    
    # Apply filters
    if region:
        query = query.filter(Store.region == region)
    
    if country:
        query = query.filter(Store.country == country)
    
    if store_slug:
        query = query.filter(Store.slug == store_slug)
    
    if store_type:
        query = query.filter(Store.store_type == store_type)
    
    if category:
        query = query.filter(Store.category == category)
    
    if search:
        query = query.filter(Coupon.title.ilike(f"%{search}%"))
    
    # Get total count
    total = query.count()
    
    # Pagination
    coupons = query.offset((page - 1) * limit).limit(limit).all()
    
    # Format response
    coupons_data = []
    for coupon in coupons:
        coupon_dict = {
            "id": coupon.id,
            "title": coupon.title,
            "description": coupon.description,
            "code": coupon.code,
            "discount": coupon.discount,
            "expiry_date": coupon.expiry_date,
            "store_name": coupon.store.name,
            "store_slug": coupon.store.slug,
            "store_domain": coupon.store.domain,
            "region": coupon.store.region,
            "country": coupon.store.country,
            "store_type": coupon.store.store_type,
            "category": coupon.store.category,
            "created_at": coupon.created_at,
            "updated_at": coupon.updated_at
        }
        coupons_data.append(coupon_dict)
    
    return {
        "coupons": coupons_data,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
        "filters": {
            "region": region,
            "country": country,
            "store_slug": store_slug,
            "store_type": store_type,
            "category": category,
            "search": search
        }
    }

@router.get("/{coupon_id}")
@limiter.limit("60/minute")
async def get_coupon(
    request: Request,
    coupon_id: int,
    db: Session = Depends(get_db)
):
    """
    Get single coupon by ID
    """
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    return {
        "coupon": {
            "id": coupon.id,
            "title": coupon.title,
            "description": coupon.description,
            "code": coupon.code,
            "discount": coupon.discount,
            "expiry_date": coupon.expiry_date,
            "store_name": coupon.store.name,
            "store_slug": coupon.store.slug,
            "store_domain": coupon.store.domain,
            "region": coupon.store.region,
            "country": coupon.store.country,
            "store_type": coupon.store.store_type,
            "category": coupon.store.category,
            "created_at": coupon.created_at,
            "updated_at": coupon.updated_at
        }
    }

@router.post("/{coupon_id}/click")
@limiter.limit("60/minute")
async def track_coupon_click(
    request: Request,
    coupon_id: int,
    db: Session = Depends(get_db)
):
    """
    Track coupon click and return affiliate URL
    """
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    # TODO: Implement affiliate URL generation
    # For now, return the store's domain
    affiliate_url = f"https://{coupon.store.domain}"
    
    # TODO: Track click in database
    # For now, just return the URL
    
    return {
        "coupon_id": coupon_id,
        "affiliate_url": affiliate_url,
        "store_name": coupon.store.name,
        "message": "Click tracked successfully"
    }
