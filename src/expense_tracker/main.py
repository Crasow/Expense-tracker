from fastapi import FastAPI
from expense_tracker.api import users

app = FastAPI()

@app.get("/")
def root():
    return {"message": "It works!"}

app.include_router(users.router)