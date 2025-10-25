from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Table, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

# Many-to-many relationship
store_categories = Table('store_categories', Base.metadata,
    Column('store_id', Integer, ForeignKey('stores.id', ondelete='CASCADE')),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE'))
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_premium = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    premium_expires_at = Column(DateTime, nullable=True)
    daily_coupon_count = Column(Integer, default=0)
    last_coupon_reset = Column(DateTime, default=datetime.utcnow)
    region = Column(String(20), default='america')  # america, europe, asia
    country = Column(String(50), nullable=True)  # US, UK, IN, SG, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    favorites = relationship('UserFavorite', back_populates='user', cascade='all, delete-orphan')
    subscriptions = relationship('Subscription', back_populates='user', cascade='all, delete-orphan')

class Store(Base):
    __tablename__ = 'stores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    domain = Column(String(255), unique=True, nullable=False)
    logo_url = Column(Text, nullable=True)
    region = Column(String(20), nullable=False, index=True)  # america, europe, asia
    country = Column(String(50), nullable=False, index=True)  # US, UK, IN, SG, etc.
    store_type = Column(String(50), default='retail')  # retail, food_delivery, grocery
    category = Column(String(100), nullable=True)  # fashion, electronics, food, etc.
    affiliate_network = Column(String(100), nullable=True)  # shareasale, cj, amazon, etc.
    affiliate_id = Column(String(255), nullable=True)
    merchant_id = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    scrape_frequency = Column(Integer, default=60)  # minutes
    last_scraped_at = Column(DateTime, nullable=True)
    scraper_config = Column(Text, nullable=True)  # JSON as text for SQLite
    created_at = Column(DateTime, default=datetime.utcnow)
    
    coupons = relationship('Coupon', back_populates='store', cascade='all, delete-orphan')
    categories = relationship('Category', secondary=store_categories, back_populates='stores')
    scrape_logs = relationship('ScrapeLog', back_populates='store', cascade='all, delete-orphan')

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    icon = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    stores = relationship('Store', secondary=store_categories, back_populates='categories')

class Coupon(Base):
    __tablename__ = 'coupons'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    store_id = Column(Integer, ForeignKey('stores.id', ondelete='CASCADE'), nullable=False, index=True)
    code = Column(String(100), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    discount_type = Column(String(20), nullable=True)  # percentage, fixed, free_shipping, bogo
    discount_value = Column(Numeric(10, 2), nullable=True)
    minimum_purchase = Column(Numeric(10, 2), nullable=True)
    maximum_discount = Column(Numeric(10, 2), nullable=True)
    expires_at = Column(DateTime, nullable=True, index=True)
    affiliate_url = Column(Text, nullable=True)
    source_url = Column(Text, nullable=True)
    is_verified = Column(Boolean, default=False)
    is_exclusive = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, index=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    store = relationship('Store', back_populates='coupons')
    clicks = relationship('CouponClick', back_populates='coupon', cascade='all, delete-orphan')
    feedbacks = relationship('CouponFeedback', back_populates='coupon', cascade='all, delete-orphan')

class UserFavorite(Base):
    __tablename__ = 'user_favorites'
    
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id', ondelete='CASCADE'), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='favorites')

class CouponClick(Base):
    __tablename__ = 'coupon_clicks'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    coupon_id = Column(String(36), ForeignKey('coupons.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    country_code = Column(String(2), nullable=True)
    clicked_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    coupon = relationship('Coupon', back_populates='clicks')

class CouponFeedback(Base):
    __tablename__ = 'coupon_feedback'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    coupon_id = Column(String(36), ForeignKey('coupons.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    worked = Column(Boolean, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    coupon = relationship('Coupon', back_populates='feedbacks')

class ScrapeLog(Base):
    __tablename__ = 'scrape_logs'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    store_id = Column(Integer, ForeignKey('stores.id', ondelete='CASCADE'), nullable=False, index=True)
    status = Column(String(20), nullable=False)  # success, failed, partial
    coupons_found = Column(Integer, default=0)
    coupons_new = Column(Integer, default=0)
    coupons_updated = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    store = relationship('Store', back_populates='scrape_logs')

class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    stripe_subscription_id = Column(String(255), unique=True, nullable=True)
    stripe_customer_id = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False)  # active, cancelled, expired, trialing
    plan = Column(String(20), nullable=False)  # monthly, yearly
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    cancel_at_period_end = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('User', back_populates='subscriptions')
