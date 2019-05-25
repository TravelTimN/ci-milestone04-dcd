import os

class Config:
    MONGO_DBNAME = "2BN-Desserts"
    MONGO_URI = os.getenv("MONGO_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")