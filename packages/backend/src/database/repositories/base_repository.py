"""
基礎資料庫存取類別
"""

from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from ..models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """基礎資料庫存取類別"""

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get(self, id: int) -> Optional[T]:
        """依 ID 取得單一記錄"""
        result = await self.session.execute(
            select(self.model).filter(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> List[T]:
        """取得所有記錄"""
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def add(self, entity: T) -> T:
        """新增記錄"""
        self.session.add(entity)
        await self.session.commit()
        return entity

    async def update(self, id: int, values: dict) -> Optional[T]:
        """更新記錄"""
        await self.session.execute(
            update(self.model).where(self.model.id == id).values(**values)
        )
        await self.session.commit()
        return await self.get(id)

    async def delete(self, id: int) -> bool:
        """刪除記錄"""
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.session.commit()
        return result.rowcount > 0
