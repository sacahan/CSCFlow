import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from src.database.repositories.real_time_flow_repository import RealTimeFlowRepository
from src.database.models.real_time_flow import RealTimeFlow


@pytest.mark.asyncio
async def test_get_latest_flow(async_session: AsyncSession):
    repository = RealTimeFlowRepository(async_session)

    # Arrange: 插入測試資料
    flow1 = RealTimeFlow(
        id="1",
        center_id="1",
        area_type="gym",
        timestamp=datetime.now() - timedelta(minutes=10),
    )
    flow2 = RealTimeFlow(
        id="2", center_id="1", area_type="gym", timestamp=datetime.now()
    )
    async_session.add_all([flow1, flow2])
    await async_session.commit()

    # Act: 呼叫方法
    latest_flow = await repository.get_latest_flow(center_id="1", area_type="gym")

    # Assert: 驗證結果
    assert latest_flow.id == "2"
