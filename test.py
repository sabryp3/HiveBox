import unittest
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch 
from redis.asyncio import Redis
from main import temp_endpoint, get_temp, app
from version import VERSION

client = TestClient(app)


@pytest.mark.asyncio
async def test_returns_correct_version():
    assert VERSION == "v0.0.1"


def test_valid_temperature_sensor():
    mock_response = {
        'sensors': [
            {'title': 'Other', 'lastMeasurement': {'value': '10.0'}},
            {'title': 'Temperatur', 'lastMeasurement': {'value': '23.5'}},
        ]
    }

    result = get_temp(mock_response)

    assert isinstance(result, float)
    assert result == 23.5


@pytest.mark.asyncio
@patch('main.redis', new_callable=AsyncMock)
@patch('main.httpx.get')
async def test_temp_endpoint(mock_get, mock_redis):
    # Mock Redis behavior
    mock_redis.get.return_value = None
    mock_redis.set.return_value = None
    # Mock HTTP response
    mock_get.return_value.json.return_value = {
        'sensors': [
            {'title': 'Temperatur', 'lastMeasurement': {'value': '20.0'}},
        ]
    }
    result = await temp_endpoint()
    assert result == "Good"

@pytest.mark.asyncio
async def test_temp_integration():
    # Mock Redis methods directly
    with patch.object(Redis, "get", new=AsyncMock(return_value=None)) as mock_get, \
         patch.object(Redis, "set", new=AsyncMock()) as mock_set:
        
        with TestClient(app) as test_client:
            response = test_client.get("/temperature")
            assert response.status_code == 200

if __name__ == '__main__':
        unittest.main()