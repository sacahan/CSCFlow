"""
WebSocket 服務
提供即時人流更新功能
"""

from fastapi import WebSocket, APIRouter
from typing import Dict

router = APIRouter()

# 儲存活躍的 WebSocket 連接
active_connections: Dict[str, WebSocket] = {}


@router.websocket("/ws/current_flows/{center_id}")
async def websocket_endpoint(websocket: WebSocket, center_id: str):
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
