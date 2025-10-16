from fastapi import FastAPI, HTTPException, status, Depends, Header, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from datetime import datetime

from models import LoginRequest, TokenResponse, Item, ProfileUpdate
from auth import create_access_token, decode_access_token

load_dotenv()
PORT = int(os.getenv("PORT", "3000"))


app = FastAPI(title="JWT Marketplace API")


app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

USERS = {
"user1@example.com": {
"id": "user1@example.com",
"email": "user1@example.com",
"password": "pass123",
"name": "Demo User"
}
}


ITEMS = [
{"id": 1, "name": "Tumbler", "price": 150000},
{"id": 2, "name": "Sticker Pack", "price": 25000},
{"id": 3, "name": "Notebook", "price": 45000},
]

@app.middleware("http")
async def log_requests(request: Request, call_next):
    ts = datetime.utcnow().isoformat()
    print(f"[{ts}] {request.method} {request.url}")
    response = await call_next(request)
    return response


@app.post("/auth/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    user = USERS.get(req.email)
    if not user or req.password != user.get("password"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid credentials"})

    token = create_access_token(subject=user["id"], email=user["email"], expires_minutes=15)
    print(f"[LOGIN] user={req.email}")
    return {"access_token": token}

@app.post("/auth/register")
async def register(req: LoginRequest):
    if req.email in USERS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Email already registered"})
    
    USERS[req.email] = {
        "id": req.email,
        "email": req.email,
        "password": req.password,
        "name": "New User"
    }
    print(f"[REGISTER] user={req.email}")
    return {"message": "User registered successfully"}

@app.get("/items")
async def get_items():
    return {"items": ITEMS}


async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Missing or invalid Authorization header"})
    try:
        scheme, token = authorization.split()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Missing or invalid Authorization header"})
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Missing or invalid Authorization header"})
    try:
        payload = decode_access_token(token)
    except ValueError as e:
        msg = str(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": msg})


    user = USERS.get(payload.get("email"))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})
    return user


@app.put("/profile")
async def update_profile(update: ProfileUpdate, current_user: dict = Depends(get_current_user)):
    if not update.name and not update.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "At least one field (name or email) must be provided"})
    if update.name:
        current_user["name"] = update.name
    if update.email:
        if update.email != current_user["email"] and update.email in USERS:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Email already in use"})
        USERS.pop(current_user["email"], None)
        current_user["email"] = update.email
        USERS[current_user["email"]] = current_user
        print(f"[PROFILE UPDATE] user={current_user['email']}")
        return {"message": "Profile updated", "profile": {"name": current_user.get("name"), "email": current_user.get("email")}}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    detail = exc.detail
    if isinstance(detail, dict):
        return JSONResponse(status_code=exc.status_code, content=detail)
    return JSONResponse(status_code=exc.status_code, content={"error": detail})

@app.get("/")
def read_root():
    return {"message": "Welcome to the Marketplace API!"}