from dotenv import load_dotenv
import os

# This automatically loads from ".env" in project root
load_dotenv()

def get_env():
    return os.getenv("APP_ENV", "prod")