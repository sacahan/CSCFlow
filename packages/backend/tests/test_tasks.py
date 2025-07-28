import unittest
from unittest.mock import AsyncMock, patch
from src.tasks import calculate_hourly_stats, cleanup_old_data


class TestTasks(unittest.TestCase):
    @patch("src.tasks.get_db_session", new_callable=AsyncMock)
    async def test_calculate_hourly_stats(self, mock_get_db_session):
        mock_session = mock_get_db_session.return_value.__aenter__.return_value
        mock_session.execute.return_value = [
            {
                "center_id": "test_center_id",
                "area_type": "gym",
                "avg_count": 50,
                "max_count": 100,
            }
        ]

        await calculate_hourly_stats()
        mock_session.merge.assert_called_once()

    @patch("src.tasks.get_db_session", new_callable=AsyncMock)
    async def test_cleanup_old_data(self, mock_get_db_session):
        mock_session = mock_get_db_session.return_value.__aenter__.return_value

        await cleanup_old_data()
        mock_session.execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()
