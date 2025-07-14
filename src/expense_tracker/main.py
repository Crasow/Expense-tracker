from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from contextlib import asynccontextmanager
from expense_tracker.api import users
from expense_tracker.db import init_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    """initialize database on startup"""
    print("🚀 Initializing database...")
    try:
        await init_database()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        raise
    yield

app = FastAPI(lifespan=lifespan, title="Expense Tracker", description="API for expense tracking", version="0.1.0")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_errors = []

    for error in errors:
        loc = " -> ".join(str(x) for x in error["loc"])
        msg = error["msg"]
        custom_errors.append(f"{loc}: {msg}")

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Ошибка валидации данных",
            "errors": custom_errors,
        },
    )
    
@app.get("/")
def root():
    return {"message": "It works!"}

app.include_router(users.router)