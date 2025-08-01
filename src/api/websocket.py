"""
WebSocket 服務
提供即時人流更新功能
"""

from fastapi import WebSocket, APIRouter, status
from fastapi.security import APIKeyHeader
from typing import Dict
from jose import JWTError, jwt
from datetime import datetime
import os

router = APIRouter()

# JWT 設定
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Token header
token_header = APIKeyHeader(name="Authorization", auto_error=False)

# 儲存活躍的 WebSocket 連接
active_connections: Dict[str, WebSocket] = {}


async def verify_token(websocket: WebSocket) -> bool:
    try:
        # 從查詢參數獲取 token
        token = websocket.query_params.get("token")
        if not token:
            # 從 headers 獲取 token
            token = websocket._headers.get("authorization", "").replace("Bearer ", "")

        if not token:
            return False

        # 驗證 token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if not payload:
            return False

        # 檢查 token 是否過期
        expires_at = payload.get("exp")
        if not expires_at or datetime.utcfromtimestamp(expires_at) < datetime.utcnow():
            return False

        return True
    except JWTError:
        return False


@router.websocket("/ws/current_flows/{center_id}")
async def websocket_endpoint(websocket: WebSocket, center_id: str):
    # 驗證 token
    is_valid = await verify_token(websocket)
    if not is_valid:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    active_connections[center_id] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            # 驗證並處理接收到的數據
            if data.get("type") == "update":
                # 廣播更新給所有訂閱該中心的客戶端
                await websocket.send_json(
                    {
                        "type": "update",
                        "data": {
                            "center_id": center_id,
                            "timestamp": data["data"]["timestamp"],
                            "gym": data["data"]["gym"],
                            "pool": data["data"]["pool"],
                        },
                    }
                )
    except Exception:
        if center_id in active_connections:
            del active_connections[center_id]
