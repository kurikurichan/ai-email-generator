from fastapi import FastAPI

from .routers import email

# Create a new instance of the FastAPI class
app = FastAPI()
# Link the email router to the main app
app.include_router(email.router)
