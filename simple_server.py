from fastapi import FastAPI

app = FastAPI(title="GlobalCouponFinder API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Welcome to GlobalCouponFinder API", "status": "working"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "GlobalCouponFinder"}

if __name__ == "__main__":
    import uvicorn
    print("Starting server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
