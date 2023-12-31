from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import volunteers, events, planner, organizations, admin
import json
import logging
import sys

description = """
Volunteer Verse Description
"""

app = FastAPI(
    title="Volunteer Verse",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Ananya Thapar",
        "email": "athapar@calpoly.edu",
    },
)

app.include_router(volunteers.router)
app.include_router(events.router)
app.include_router(planner.router)
app.include_router(organizations.router)
app.include_router(admin.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome to the Volunteer Verse!"}
