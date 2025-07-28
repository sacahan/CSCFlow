from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import api_router

app = FastAPI(title="CSCFlow API")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊 API 路由
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to CSCFlow API"}
