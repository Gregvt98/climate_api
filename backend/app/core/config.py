import os

PROJECT_NAME = "climate_api"

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

SA_API = os.getenv("SA_API")

API_V1_STR = "/api/v1"

print(SA_API)
