from fastapi import (
    FastAPI,
    HTTPException,
    WebSocket,
    Depends,
    WebSocketDisconnect,
    status,
)
from typing import List, Optional, Dict, Set
import asyncio
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
import jwt
from fastapi.responses import JSONResponse
import redis
from functools import wraps
import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import sessionmaker, Session

# 從 schemas.py 導入所需的模型
from .schemas import (
    UserRole,
    User,
    TokenResponse,
    SportCenterResponse,
    RealTimeFlowResponse,
    UpdateFlowRequest,
    TrendStatsResponse,
)

# 驗證用戶函數
from .db import SessionLocal as LocalSession
from .models import User as UserModel, SportCenter, RealTimeFlow as Flow, Base

# 從 models.py 導入資料庫模型
from contextlib import asynccontextmanager

# 載入環境變數
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def verify_user(username: str, password: str) -> Optional[User]:
    session: Session = LocalSession()
    try:
        user_record = (
            session.query(UserModel).filter(UserModel.username == username).first()
        )
        if (
            user_record and user_record.hashed_password == password
        ):  # 實際應用中應該比對雜湊
            return User(
                username=user_record.username,
                email=user_record.email,
                full_name=user_record.full_name,
                role=user_record.role,
                disabled=user_record.disabled,
            )
        return None
    finally:
        session.close()


# 獲取當前用戶函數
# OAuth2PasswordBearer 用於處理 Token 的驗證
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="無效的認證憑證",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    session: Session = LocalSession()
    try:
        user_record = (
            session.query(UserModel).filter(UserModel.username == username).first()
        )
        if user_record is None:
            raise credentials_exception
        return User(
            username=user_record.username,
            email=user_record.email,
            full_name=user_record.full_name,
            role=user_record.role,
            disabled=user_record.disabled,
        )
    finally:
        session.close()


# 操作日誌記錄
def log_operation(user: User, operation: str, details: dict):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user.username,
        "role": user.role,
        "operation": operation,
        "details": details,
    }
    # 在實際應用中，應該將日誌儲存到資料庫或日誌系統
    print(f"操作日誌: {log_entry}")  # 開發環境下先印出日誌


# 初始化 FastAPI 應用
app = FastAPI(
    title="運動中心即時人流系統 API",
    description="提供運動中心即時人流監控與管理的RESTful API服務",
    version="1.0.0",
)

# 環境變數設定
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 初始化資料庫連線
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 初始化 Redis 客戶端
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    db=int(os.getenv("REDIS_DB", "0")),
    password=os.getenv("REDIS_PASSWORD", ""),
    decode_responses=True,
)


# 資料庫相依注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 是否為開發環境
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# API 版本和前綴
API_VERSION = os.getenv("API_VERSION", "v1")
API_PREFIX = os.getenv("API_PREFIX", f"/api/{API_VERSION}")

# OAuth2PasswordBearer 用於處理 Token 的驗證
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# 建立 JWT Token 的函式
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()  # 複製資料以避免修改原始資料
    expire = (
        datetime.now(datetime.timezone.utc) + expires_delta
    )  # 計算 Token 的到期時間
    to_encode.update({"exp": expire})  # 將到期時間加入資料中
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )  # 使用密鑰與演算法加密資料
    return encoded_jwt  # 返回加密後的 Token


# 檢查使用者角色的裝飾器
def check_role(allowed_roles: List[UserRole]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token = kwargs.get("token")
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="未提供認證 Token"
                )
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_role = payload.get("role")
                if user_role not in [role.value for role in allowed_roles]:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, detail="沒有足夠的權限"
                    )
            except jwt.PyJWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="無效的認證 Token"
                )
            return await func(*args, **kwargs)

        return wrapper

    return decorator


# Redis 快取裝飾器
def cache(ttl_seconds: int = 300):  # 預設 5 分鐘
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 根據函數名稱和參數生成快取 key
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            # 嘗試從快取獲取資料
            cached_data = redis_client.get(cache_key)
            if cached_data:
                return cached_data
            # 如果沒有快取資料，執行原始函數
            result = await func(*args, **kwargs)
            # 儲存結果到快取
            redis_client.setex(cache_key, ttl_seconds, str(result))
            return result

        return wrapper

    return decorator


# WebSocket 連線管理器
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, center_id: str):
        await websocket.accept()
        if center_id not in self.active_connections:
            self.active_connections[center_id] = set()
        self.active_connections[center_id].add(websocket)

    def disconnect(self, websocket: WebSocket, center_id: str):
        if center_id in self.active_connections:
            self.active_connections[center_id].discard(websocket)
            if not self.active_connections[center_id]:
                del self.active_connections[center_id]

    async def broadcast(self, message: dict, center_id: str):
        if center_id in self.active_connections:
            for connection in self.active_connections[center_id]:
                try:
                    await connection.send_json(message)
                except WebSocketDisconnect:
                    self.disconnect(connection, center_id)


manager = ConnectionManager()


# 取得所有運動中心的 API
@app.get("/api/v1/centers", response_model=List[SportCenterResponse])
@cache(ttl_seconds=86400)  # 快取24小時
async def get_centers(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    centers = db.query(SportCenter).all()

    # 轉換為回應格式
    response_centers = []
    for center in centers:
        response_centers.append(
            {
                "id": str(center.id),
                "name": center.name,
                "address": center.address,
                "formatted_address": center.formatted_address,
                "location": center.location,
                "max_capacity": center.max_capacity,
            }
        )

    return response_centers


# 取得單一運動中心的 API
@app.get("/api/v1/centers/{center_id}", response_model=SportCenterResponse)
def get_center(center_id: str):
    # 模擬資料，未連接資料庫
    if center_id == "1":
        return {
            "id": "1",
            "name": "運動中心A",
            "address": "地址A",
            "formatted_address": "格式化地址A",
            "location": {"lat": 25.0330, "lng": 121.5654, "place_id": "ChIJ123"},
            "max_capacity": {"gym": 100, "pool": 50},
        }
    raise HTTPException(
        status_code=404, detail="Center not found"
    )  # 找不到中心時回傳 404


# 取得即時流量的 API
@app.get("/api/v1/flows/current", response_model=List[RealTimeFlowResponse])
async def get_current_flows(
    center_id: Optional[str] = None, db: Session = Depends(get_db)
):
    # 查詢所有中心或特定中心
    query = db.query(SportCenter)
    if center_id:
        query = query.filter(SportCenter.id == center_id)

    centers = query.all()
    if center_id and not centers:
        raise HTTPException(status_code=404, detail="運動中心未找到")

    result = []
    for center in centers:
        # 獲取最新的流量記錄
        latest_gym_flow = (
            db.query(Flow)
            .filter(Flow.center_id == center.id, Flow.area_type == "gym")
            .order_by(Flow.timestamp.desc())
            .first()
        )

        latest_pool_flow = (
            db.query(Flow)
            .filter(Flow.center_id == center.id, Flow.area_type == "pool")
            .order_by(Flow.timestamp.desc())
            .first()
        )

        # 計算百分比
        gym_percentage = (
            latest_gym_flow.count / center.gym_max_capacity * 100
            if latest_gym_flow
            else 0
        )
        pool_percentage = (
            latest_pool_flow.count / center.pool_max_capacity * 100
            if latest_pool_flow
            else 0
        )

        result.append(
            {
                "id": str(center.id),
                "name": center.name,
                "gym": {
                    "current_count": latest_gym_flow.count if latest_gym_flow else 0,
                    "max_capacity": center.gym_max_capacity,
                    "percentage": gym_percentage,
                },
                "pool": {
                    "current_count": latest_pool_flow.count if latest_pool_flow else 0,
                    "max_capacity": center.pool_max_capacity,
                    "percentage": pool_percentage,
                },
            }
        )

    return result


# 更新流量的 API
@app.post("/api/v1/flows")
@check_role([UserRole.IOT_DEVICE, UserRole.STAFF])  # 只有IoT設備和職員可以更新流量
async def update_flow(
    request: UpdateFlowRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if request.area_type not in ["gym", "pool"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="區域類型必須為 'gym' 或 'pool'",
        )

    # 檢查運動中心是否存在
    center = db.query(SportCenter).filter(SportCenter.id == request.center_id).first()
    if not center:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="運動中心未找到"
        )

    # 建立新的流量記錄
    new_flow = Flow(
        center_id=request.center_id,
        area_type=request.area_type,
        count=request.count,
        timestamp=datetime.utcnow(),
    )
    db.add(new_flow)

    try:
        db.commit()

        # 使用Redis快取更新即時資料
        cache_key = f"flow:{request.center_id}:{request.area_type}"
        flow_data = {
            "current_count": request.count,
            "timestamp": new_flow.timestamp.isoformat(),
        }
        redis_client.hmset(cache_key, flow_data)
        redis_client.expire(cache_key, 300)  # 5分鐘過期

        # 廣播更新給WebSocket客戶端
        await manager.broadcast(
            {
                "type": "update",
                "data": {
                    "center_id": request.center_id,
                    "area_type": request.area_type,
                    "count": request.count,
                    "timestamp": flow_data["timestamp"],
                },
            },
            request.center_id,
        )

        # 記錄操作日誌
        log_operation(
            current_user,
            "update_flow",
            {
                "center_id": request.center_id,
                "area_type": request.area_type,
                "count": request.count,
            },
        )

        return {"success": True, "message": "已成功更新流量資料"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新流量資料時發生錯誤: {str(e)}",
        )


# 取得趨勢統計的 API
@app.get("/api/v1/stats/trend", response_model=TrendStatsResponse)
async def get_trend_stats(
    center_id: str,
    area_type: str,
    time_range: str,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
):
    if area_type not in ["gym", "pool"]:
        raise HTTPException(status_code=400, detail="區域類型不正確")
    if time_range not in ["daily", "weekly", "monthly"]:
        raise HTTPException(status_code=400, detail="時間範圍不正確")

    try:
        start_datetime = datetime.fromisoformat(start_date)
        end_datetime = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式不正確")

    # 檢查運動中心是否存在
    center = db.query(SportCenter).filter(SportCenter.id == center_id).first()
    if not center:
        raise HTTPException(status_code=404, detail="運動中心未找到")

    # 查詢指定時間範圍內的流量記錄
    flows = (
        db.query(Flow)
        .filter(
            Flow.center_id == center_id,
            Flow.area_type == area_type,
            Flow.timestamp.between(start_datetime, end_datetime),
        )
        .order_by(Flow.timestamp)
        .all()
    )

    # 根據時間範圍計算平均值
    data = []
    max_capacity = (
        center.gym_max_capacity if area_type == "gym" else center.pool_max_capacity
    )

    for flow in flows:
        percentage = (flow.count / max_capacity * 100) if max_capacity > 0 else 0
        data.append(
            {
                "timestamp": flow.timestamp.isoformat(),
                "count": flow.count,
                "percentage": round(percentage, 2),
            }
        )

    return {"center_id": center_id, "area_type": area_type, "data": data}


# WebSocket 連線的 API
@app.websocket("/ws/flows/{center_id}")
async def websocket_endpoint(websocket: WebSocket, center_id: str):
    try:
        await manager.connect(websocket, center_id)
        # 模擬即時更新資料，未連接資料庫
        while True:
            update_data = {
                "type": "update",
                "data": {
                    "center_id": center_id,
                    "timestamp": datetime.utcnow().isoformat(),
                    "gym": {"current_count": 50, "percentage": 50},
                    "pool": {"current_count": 20, "percentage": 40},
                },
            }
            await manager.broadcast(update_data, center_id)
            await asyncio.sleep(5)  # 模擬每5秒更新一次
    except WebSocketDisconnect:
        manager.disconnect(websocket, center_id)
    except Exception:
        manager.disconnect(websocket, center_id)
        await websocket.close()


# 健康檢查的 API
@app.get("/health")
def health_check():
    # 模擬健康檢查，未連接資料庫或快取系統
    health_status = {"status": "ok", "database": "connected", "cache": "ok"}
    return health_status  # 返回健康狀態


# 取得附近運動中心的 API
@app.get("/api/v1/centers/nearby")
def get_nearby_centers(lat: float, lng: float, radius: int = 5000):
    # 模擬資料，未連接資料庫
    centers = [
        {
            "id": "1",
            "name": "運動中心A",
            "formatted_address": "格式化地址A",
            "location": {"lat": 25.0330, "lng": 121.5654, "place_id": "ChIJ123"},
            "distance": 1000,
            "current_stats": {
                "gym": {"current_count": 50, "percentage": 50},
                "pool": {"current_count": 20, "percentage": 40},
            },
        }
    ]
    # 根據距離篩選
    filtered_centers = [center for center in centers if center["distance"] <= radius]
    return {"centers": filtered_centers}  # 返回篩選後的運動中心列表


# 登入的 API
@app.post("/api/v1/auth/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = verify_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="使用者名稱或密碼錯誤",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "role": user.role,
            "exp": datetime.now(datetime.timezone.utc) + access_token_expires,
        }
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES,
        user=user,
    )


# 自訂 HTTP 錯誤處理
@app.exception_handler(HTTPException)
def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "code": exc.detail if isinstance(exc.detail, str) else "UnknownError",
            "message": (
                exc.detail if isinstance(exc.detail, str) else "An error occurred"
            ),
            "details": exc.detail if isinstance(exc.detail, dict) else None,
            "detail": exc.detail,  # 確保包含 detail 欄位
        },
    )


# 在應用啟動時建立資料表
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup code can be added here if needed


app.lifespan = lifespan
