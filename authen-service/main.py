from fastapi import FastAPI, Depends, HTTPException, status, Cookie, Body, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from typing import Annotated
from pydantic import BaseModel
import uvicorn
import asyncio
from loguru import logger
from contextlib import asynccontextmanager

PROJ_DIR = os.path.dirname(__file__)
load_dotenv(os.path.join(PROJ_DIR, '.env'))

# Config
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

REFRESH_SECRET_KEY = os.environ.get('REFRESH_SECRET_KEY')
REFRESH_TOKEN_EXPIRE_DAYS = float(os.environ.get('REFRESH_TOKEN_EXPIRE_DAYS'))


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('run in lifespan')
    logger.info('PROJ_DIR: {}'.format(PROJ_DIR))
    logger.info('ACCESS_TOKEN_EXPIRE_MINUTES: {}'.format(ACCESS_TOKEN_EXPIRE_MINUTES))
    logger.info('ACCESS_TOKEN_EXPIRE_MINUTES: {}'.format(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')))
    yield
    logger.info('system down')

app = FastAPI(lifespan= lifespan)
app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("./static/favicon.ico")
# --------------------
# JWT Utils
# --------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # contains "sub" and "exp"
    except JWTError as e:
        logger.error(e)
        return None

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

def verify_refresh_token(token: str):
    return jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])


class RegisterModel(BaseModel):
    fullName: str
    email: str
    password: str
    repeatPassword: str

# --------------------
# Routes
# --------------------
OptionsCorsHeaders = {
    "Access-Control-Allow-Methods": "GET, OPTIONS, POSTS",
    "Access-Control-Max-Age": "86400",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Origin": "https://mullet-immortal-labrador.ngrok-free.app"
}

CorsHeaders = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "https://mullet-immortal-labrador.ngrok-free.app",
    "Access-Control-Allow-Credentials": "true",
    "Vary": "Origin"
}

@app.options("/api/register")
async def register_options():
    return JSONResponse(content=None,headers=OptionsCorsHeaders)

@app.post("/api/register")
async def register(register_data: Annotated[RegisterModel, Body(embedd=True)]):
    # Dummy authentication (replace with DB check)
    if register_data.fullName != "admin" or register_data.password != "Phuoc272216@@":
        raise HTTPException(
            status_code=400, 
            detail="Invalid credentials"
        )

    access_token = create_access_token({"sub": register_data.fullName})
    refresh_token = create_refresh_token({"sub": register_data.fullName})

    response = JSONResponse(
        status_code= 200,
        content={"message": "Login successful"},
        headers=CorsHeaders
    )
    # Set cookie with HttpOnly flag
    response.set_cookie(
        key="jwt",
        value=access_token,
        httponly=True,
        secure=False,   # set True in production (HTTPS only)
        samesite="none"
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,   # set True in production (HTTPS only)
        samesite="none"
    )
    return response


@app.post("/api/login")
async def login(username: str, password: str):
    # Dummy authentication (replace with DB check)
    if username != "admin" or password != "secret":
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": username})
    response = JSONResponse(
        content={"message": "Login successful"}, 
        # headers=CorsHeaders
    )
    # Set cookie with HttpOnly flag
    response.set_cookie(
        key="jwt",
        value=token,
        httponly=True,
        secure=False,   # set True in production (HTTPS only)
        samesite="none"
    )
    return response

# @app.options("/api/protected")
# def protected_options():
#     return JSONResponse(content=None,headers=OptionsCorsHeaders)

@app.get("/api/protected")
async def protected(request: Request,jwt: str | None = Cookie(default=None)):
    print('inspect cookies: ',request.cookies)
    if not jwt:
        logger.info('not jwt')
        raise HTTPException(
            status_code=401, 
            detail="Missing token",
            headers=CorsHeaders
        )

    payload = verify_access_token(jwt)

    if payload:
        logger.info('return payload')
        return JSONResponse(
            content={"payload": payload}, 
            status_code=200, 
            headers=CorsHeaders
        )
    else:
        logger.info('return 401')
        return HTTPException(
                status_code=401,
                detail="Invalid or Expired",
                headers=CorsHeaders
        )

@app.post("/api/refresh")
async def refresh(refresh_token: str | None = Cookie(default=None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = verify_refresh_token(refresh_token)
        username = payload.get("sub")

        # Issue new access token
        new_access_token = create_access_token({"sub": username})
        response = JSONResponse(
            content={"message": "Token refreshed"}, 
            # headers=CorsHeaders
        )
        response.set_cookie("jwt", new_access_token, httponly=True, secure=False, samesite="lax")
        return response
    
    except JWTError:
        raise HTTPException(
            status_code=401, 
            detail="Invalid or expired refresh token", 
            # headers=CorsHeaders
        )

@app.post("/api/logout")
async def logout():
    response = JSONResponse(
        content={"message": "Logged out"},
        # headers=CorsHeaders
    )
    response.delete_cookie("jwt")
    response.delete_cookie("refresh_token")
    return response

@app.get("/health")
async def health_check():
    logger.info('run health_check')
    return JSONResponse(
        {
            "status": "Healthy",
        },
        status_code=200
    )

# async def main_run():
#     config = uvicorn.Config(
#         "main:app",
#         host="0.0.0.0",
#     	port=8080, 
#     	reload=True,
#         log_level = "info"
#     	)
#     server = uvicorn.Server(config)
#     await server.serve()

# if __name__ == "__main__":
#     asyncio.run(main_run())