import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.repositories.sport_center_repository import SportCenterRepository
from src.database.models.sport_center import SportCenter


@pytest.mark.asyncio
async def test_get_active_centers(async_session: AsyncSession):
    repository = SportCenterRepository(async_session)

    # Arrange: 插入測試資料
    center1 = SportCenter(id="1", name="Center 1", is_active=True)
    center2 = SportCenter(id="2", name="Center 2", is_active=False)
    async_session.add_all([center1, center2])
    await async_session.commit()

    # Act: 呼叫方法
    active_centers = await repository.get_active_centers()

    # Assert: 驗證結果
    assert len(active_centers) == 1
    assert active_centers[0].id == "1"
