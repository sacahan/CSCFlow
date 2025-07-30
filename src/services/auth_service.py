"""
認證服務
處理使用者認證和授權
"""

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timezone, datetime, timedelta
import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.secret_key = os.getenv("JWT_SECRET", "your-secret-key")

    async def authenticate(self, username: str, password: str) -> dict:
        """
        驗證使用者身份並產生 JWT Token
        """
        env_username = os.getenv("ADMIN_USERNAME", "admin")
        env_password = os.getenv("ADMIN_PASSWORD", "admin")

        if username == env_username and password == env_password:
            token = self._create_token({"sub": username})
            return {
                "access_token": token,
                "expires_in": 3600,  # 1 小時
            }
        return None

    def _create_token(self, data: dict) -> str:
        """
        產生 JWT Token
        """
        expire = datetime.now(timezone.utc) + timedelta(hours=1)
        data.update({"exp": expire})
        return jwt.encode(data, self.secret_key, algorithm="HS256")

    def verify_token(self, token: str) -> dict:
        """
        驗證 JWT Token 的有效性
        """
        if not token:
            raise HTTPException(status_code=401, detail="缺少 Token")
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token 已過期")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="無效的 Token")
