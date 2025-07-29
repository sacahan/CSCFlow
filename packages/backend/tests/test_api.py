from fastapi import HTTPException
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch

client = TestClient(app)

# 添加身份驗證令牌
AUTH_TOKEN = "Bearer test_token"

# 更新測試用戶端的 headers
client.headers.update({"Authorization": AUTH_TOKEN})


# 測試取得所有運動中心的 API
@patch("src.api.get_centers")
def test_get_centers(mock_get_centers):
    mock_get_centers.return_value = [
        {
            "id": "1",
            "name": "運動中心A",
            "address": "地址A",
            "max_capacity": {"gym": 100, "pool": 50},
            "website_url": "https://example.com",
        }
    ]
    response = client.get("/api/v1/centers")  # 發送 GET 請求
    assert response.status_code == 200  # 確保回應狀態碼為 200
    assert isinstance(response.json(), list)  # 確保回應為列表
    assert len(response.json()) > 0  # 確保列表中至少有一個元素
    assert "id" in response.json()[0]  # 確保每個元素包含 id 欄位
    assert "name" in response.json()[0]  # 確保每個元素包含 name 欄位
    assert "max_capacity" in response.json()[0]  # 確保每個元素包含 max_capacity 欄位
    assert "website_url" in response.json()[0]  # 確保每個元素包含 website_url 欄位


# 測試取得特定運動中心的 API
@patch("src.api.get_center")
def test_get_center(mock_get_center):
    mock_get_center.return_value = {
        "id": "1",
        "name": "運動中心A",
        "address": "地址A",
        "max_capacity": {"gym": 100, "pool": 50},
        "website_url": "https://example.com",
    }
    response = client.get("/api/v1/centers/1")  # 發送 GET 請求，指定中心 ID 為 1
    assert response.status_code == 200  # 確保回應狀態碼為 200
    data = response.json()  # 解析回應 JSON 資料
    assert data["id"] == "1"  # 確保回應的中心 ID 為 1
    assert data["name"] == "運動中心A"  # 確保回應的中心名稱正確
    assert "max_capacity" in data  # 確保回應包含 max_capacity 欄位
    assert "website_url" in data  # 確保回應包含 website_url 欄位


# 測試取得不存在的運動中心時的回應
@patch("src.api.get_center")
def test_get_center_not_found(mock_get_center):
    mock_get_center.side_effect = HTTPException(
        status_code=404, detail="Center not found"
    )
    response = client.get("/api/v1/centers/999")  # 發送 GET 請求，指定不存在的中心 ID
    assert response.status_code == 404  # 確保回應狀態碼為 404
    assert response.json()["detail"] == "Center not found"  # 確保回應的錯誤訊息正確


# 測試取得所有運動中心即時流量的 API
def test_get_current_flows():
    response = client.get("/api/v1/flows/current")  # 發送 GET 請求
    assert response.status_code == 200  # 確保回應狀態碼為 200
    assert isinstance(response.json(), list)  # 確保回應為列表
    assert len(response.json()) > 0  # 確保列表中至少有一個元素
    assert "id" in response.json()[0]  # 確保每個元素包含 id 欄位
    assert "gym" in response.json()[0]  # 確保每個元素包含 gym 欄位
    assert "pool" in response.json()[0]  # 確保每個元素包含 pool 欄位


# 測試取得特定運動中心即時流量的 API
def test_get_current_flows_with_center_id():
    response = client.get(
        "/api/v1/flows/current?center_id=1"
    )  # 發送 GET 請求，指定中心 ID 為 1
    assert response.status_code == 200  # 確保回應狀態碼為 200
    data = response.json()  # 解析回應 JSON 資料
    assert len(data) == 1  # 確保回應列表中只有一個元素
    assert data[0]["id"] == "1"  # 確保該元素的 ID 為 1


# 測試取得不存在的運動中心即時流量時的回應
def test_get_current_flows_center_not_found():
    response = client.get(
        "/api/v1/flows/current?center_id=999"
    )  # 發送 GET 請求，指定不存在的中心 ID
    assert response.status_code == 404  # 確保回應狀態碼為 404
    assert response.json()["detail"] == "Center not found"  # 確保回應的錯誤訊息正確


# 測試更新運動中心流量的 API
def test_update_flow():
    response = client.post(
        "/api/v1/flows", json={"center_id": "1", "area_type": "gym", "count": 60}
    )  # 發送 POST 請求，更新中心 ID 為 1 的 gym 區域流量
    assert response.status_code == 200  # 確保回應狀態碼為 200
    assert response.json()["success"] is True  # 確保更新成功
    assert (
        response.json()["message"] == "Flow updated successfully"
    )  # 確保回應的訊息正確


# 測試更新運動中心流量時，提供無效區域類型的回應
def test_update_flow_invalid_area_type():
    response = client.post(
        "/api/v1/flows", json={"center_id": "1", "area_type": "invalid", "count": 60}
    )  # 發送 POST 請求，區域類型設為無效值
    assert response.status_code == 400  # 確保回應狀態碼為 400
    assert response.json()["detail"] == "Invalid area_type"  # 確保回應的錯誤訊息正確


# 測試取得運動中心趨勢統計資料的 API
def test_get_trend_stats():
    response = client.get(
        "/api/v1/stats/trend",
        params={
            "center_id": "1",
            "area_type": "gym",
            "time_range": "daily",
            "start_date": "2025-07-27",
            "end_date": "2025-07-28",
        },
    )  # 發送 GET 請求，取得中心 ID 為 1 的 gym 區域每日趨勢統計資料
    assert response.status_code == 200  # 確保回應狀態碼為 200
    data = response.json()  # 解析回應 JSON 資料
    assert data["center_id"] == "1"  # 確保回應的中心 ID 為 1
    assert data["area_type"] == "gym"  # 確保回應的區域類型為 gym
    assert isinstance(data["data"], list)  # 確保統計資料為列表
    assert len(data["data"]) > 0  # 確保統計資料列表中至少有一個元素


# 測試取得運動中心趨勢統計資料時，提供無效區域類型的回應
def test_get_trend_stats_invalid_area_type():
    response = client.get(
        "/api/v1/stats/trend",
        params={
            "center_id": "1",
            "area_type": "invalid",
            "time_range": "daily",
            "start_date": "2025-07-27",
            "end_date": "2025-07-28",
        },
    )  # 發送 GET 請求，區域類型設為無效值
    assert response.status_code == 400  # 確保回應狀態碼為 400
    assert response.json()["detail"] == "Invalid area_type"  # 確保回應的錯誤訊息正確


# 測試取得運動中心趨勢統計資料時，提供無效時間範圍的回應
def test_get_trend_stats_invalid_time_range():
    response = client.get(
        "/api/v1/stats/trend",
        params={
            "center_id": "1",
            "area_type": "gym",
            "time_range": "invalid",
            "start_date": "2025-07-27",
            "end_date": "2025-07-28",
        },
    )  # 發送 GET 請求，時間範圍設為無效值
    assert response.status_code == 400  # 確保回應狀態碼為 400
    assert response.json()["detail"] == "Invalid time_range"  # 確保回應的錯誤訊息正確


# 測試健康檢查的 API
def test_health_check():
    response = client.get("/health")  # 發送 GET 請求
    assert response.status_code == 200  # 確保回應狀態碼為 200
    data = response.json()  # 解析回應 JSON 資料
    assert data["status"] == "ok"  # 確保系統狀態為正常
    assert data["database"] == "connected"  # 確保資料庫連線正常
    assert data["cache"] == "ok"  # 確保快取系統正常
