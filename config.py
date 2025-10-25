from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "GlobalCouponFinder"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Database
    DATABASE_URL: str = "sqlite:///./couponfinder.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    UPSTASH_REDIS_URL: Optional[str] = None
    
    # JWT
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Stripe
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    
    # Supabase
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    
    # Email
    RESEND_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "noreply@globalcouponfinder.com"
    
    # Sentry
    SENTRY_DSN: Optional[str] = None
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "https://yourdomain.com"]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Free tier limits
    FREE_DAILY_COUPON_LIMIT: int = 50
    PREMIUM_DAILY_COUPON_LIMIT: int = 999999
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

