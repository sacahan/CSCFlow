import unittest
from src.schemas import (
    User,
    TokenResponse,
    LocationInfo,
    MaxCapacity,
    SportCenterResponse,
)


class TestSchemas(unittest.TestCase):
    def test_user_schema(self):
        user = User(
            username="test_user",
            email="test@example.com",
            full_name="Test User",
            role="admin",
            disabled=False,
        )
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.role, "admin")

    def test_token_response_schema(self):
        token = TokenResponse(
            access_token="test_token",
            token_type="Bearer",
            expires_in=3600,
            user={"username": "test_user", "role": "admin"},
        )
        self.assertEqual(token.token_type, "Bearer")
        self.assertEqual(token.expires_in, 3600)

    def test_location_info_schema(self):
        location = LocationInfo(lat=25.033, lng=121.565)  # Removed place_id field
        self.assertEqual(location.lat, 25.033)

    def test_max_capacity_schema(self):
        capacity = MaxCapacity(gym=100, pool=50)
        self.assertEqual(capacity.gym, 100)
        self.assertEqual(capacity.pool, 50)

    def test_sport_center_response_schema(self):
        center_response = SportCenterResponse(
            id="test_id",
            name="運動中心A",
            address="地址A",
            max_capacity=MaxCapacity(gym=100, pool=50),
            website_url="https://example.com",
        )
        self.assertEqual(center_response.name, "運動中心A")


if __name__ == "__main__":
    unittest.main()
