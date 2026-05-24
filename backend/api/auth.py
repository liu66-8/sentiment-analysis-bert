import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["认证"])

active_tokens = {}


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    token: str
    message: str


@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest):
    if req.username == "admin" and req.password == "admin":
        token = str(uuid.uuid4())
        active_tokens[token] = {
            "username": req.username,
            "login_at": datetime.now(timezone.utc).isoformat(),
        }
        return LoginResponse(success=True, token=token, message="登录成功")
    raise HTTPException(status_code=401, detail="用户名或密码错误")


@router.get("/verify")
async def verify_token(token: str = ""):
    if token in active_tokens:
        return {"valid": True, "username": active_tokens[token]["username"]}
    return {"valid": False}


@router.post("/logout")
async def logout(token: str = ""):
    active_tokens.pop(token, None)
    return {"success": True}
