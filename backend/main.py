from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import tasks
from sqlmodel import SQLModel
from database import engine

app = FastAPI(title="FastAPI Task Backend", version="1.0.0")

# Add CORS middleware for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header for frontend to read responses
    expose_headers=["Authorization"]
)

# Include the task router
app.include_router(tasks.router)

@app.on_event("startup")
def on_startup():
    # Create database tables
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"message": "FastAPI Task Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)