"""
FastAPI authentication server with multiple authentication methods like AWS, Google, Facebook, etc.

"""

from contextlib import asynccontextmanager

import stytch
from fastapi import FastAPI, Response
from pydantic import BaseModel, EmailStr

# Get general settings from config.py
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event"""
    # tudo que ficar antes do comando yield é executado antes de iniciar o servidor
    # busca a conexão com o servidor de autenticação da MSAL (Microsoft Authentication Library)
    print("Starting up the server...")

    app.settings = settings
    app.sessions = set()
    # tries to create the Stycth authentication client
    try:
      app.stytch_client = stytch.Client(
        project_id=settings.STYTCH_PROJECT_ID,
        secret=settings.STYTCH_SECRET,
        environment="test",
      )
    except Exception as e:
      print(f"Error connecting to Stytch: {e}")
      raise e

    yield
    # everything after yield is executed after the server stops
    print("Shutting down the server...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    lifespan=lifespan,
    openapi_url=f"{settings.API_VERSION_STR}/openapi.json",
    url_prefix=settings.API_VERSION_STR,
)

# takes an email received from the request and
# returns
# status_code: with possible values
#    200 if the email is present in the database
#    201 if the email is new and the user is created
#    4XX errors like invalid email or not verified or
#    5XX errors like internal server errors
# request_id : a unique id for the request, for debuging and tracing purposes
# user_id : the user_id of the logged in user
# email_id : a unique id for the email, for debuging and tracing purposes
#  user_create: boolean indicating if the user was created or not
# The link will provide login for old users or creation of a new user if the email is not found
class TentativeUser(BaseModel):
  email: EmailStr

@app.post("/login_or_create_user")
async def login_or_create_user(user:TentativeUser) -> Response :
  try:
    resp = await app.stytch_client.magic_links.email.login_or_create_async(
        email=user.email,
    )
    return { "status" : "ok", "data": resp}
  except Exception as e:
    print(e)
    return {"status_code": 500, "message": "Internal Server Error"}


@app.get("/")
async def health_check():
    return {"status": "ok", "message":"I'm completely operational and all my circuits are functioning perfectly"}

# This is the endpoint the link in the magic link hits.
# It takes the token from the link's query params and hits the
# stytch authenticate endpoint to verify the token is valid
@app.get("/authenticate/{stytch_token_type},{token}")
async def authenticate(stytch_token_type: str, token: str)  -> str:
    resp = await app.stytch_client.magic_links.authenticate_async(
        token=token,
        session_duration_minutes=app.settings.SESSION_DURATION_MINUTES,
        )
    if resp.status_code != 200:
        print(resp)
        return "something went wrong authenticating token"
    print(f"User {resp.user} is authenticated")
    if app.sessions.has(resp.session_token):
        return "already logged in"
    app.sessions.add(resp.session_token)
    return

# handles the logout endpoint
@app.get("/logout/{session_token}")
async def logout(session_token:str) -> None:
    app.session.delete(session_token)
    return None

# Helper method for session authentication
async def get_authenticated_user():
    stytch_session = app.sessions.has("stytch_session_token")
    if not stytch_session:
        return None
    resp = await app.stytch_client.sessions.authenticate_async(session_token=stytch_session)
    if resp.status_code != 200:
        return None
    return resp.user
