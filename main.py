from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import sentry_sdk
from config import settings
from database import init_db

# Initialize Sentry
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        environment="production" if not settings.DEBUG else "development"
    )

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZIP Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Startup event
@app.on_event("startup")
async def startup_event():
    init_db()
    print(f"{settings.APP_NAME} started successfully!")

# Root endpoint
@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": settings.APP_NAME}

# Import and include routers
from routers import stores, coupons

app.include_router(stores.router, prefix="/api/v1/stores", tags=["Stores"])
app.include_router(coupons.router, prefix="/api/v1/coupons", tags=["Coupons"])

# Import and include other routers (will create in next phases)
# from routers import auth, admin, subscriptions
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
# app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
# app.include_router(subscriptions.router, prefix="/api/v1/subscriptions", tags=["Subscriptions"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)