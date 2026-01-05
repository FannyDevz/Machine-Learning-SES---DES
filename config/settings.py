# config/settings.py
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT"))

def debug():
    print("DB_HOST:", DB_HOST)
    print("DB_USER:", DB_USER)
    print("DB_NAME:", DB_NAME)
    print("DB_PORT:", DB_PORT)
