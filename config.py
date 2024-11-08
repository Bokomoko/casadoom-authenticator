import os
import sys

from dotenv import load_dotenv

load_dotenv()


class Settings:
  PROJECT_NAME: str = "FastAPI Authentication Server"
  PROJECT_DESCRIPTION: str = "Authentication server for the entire corporation.\n Makes uses of Stytch for authentication."
  API_VERSION_STR: str = "/api/v1"
  SECRET_KEY: str = "secret_key"
  HOST = os.getenv("HOST", "localhost")
  PORT = int(os.getenv("PORT", "3000"))
  SESSION_DURATION_MINUTES = 60

# Load the Stytch credentials, but quit if they aren't defined
  STYTCH_PROJECT_ID = os.getenv("STYTCH_PROJECT_ID")
  STYTCH_SECRET = os.getenv("STYTCH_SECRET")
  if STYTCH_PROJECT_ID is None:
      sys.exit("STYTCH_PROJECT_ID env variable must be set before running")
  if STYTCH_SECRET is None:
      sys.exit("STYTCH_SECRET env variable must be set before running")


settings = Settings()
