from fastapi import FastAPI
from app.routers import products, categories
from app.database import Base, engine

app = FastAPI()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(products.router)
app.include_router(categories.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Marketplace API"}