from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import db
from routes import auth, habits
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(lifespan= lifespan)

app.include_router(auth.router, prefix="/auth")
app.include_router(habits.router, prefix="/habits")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://habit-tracker-frontend-five-chi.vercel.app/"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "welcome to the habit tracker api"}

