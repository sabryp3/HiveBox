import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch 
from main import temp_endpoint, get_temp, app
from version import VERSION

client = TestClient(app)



class TestVersion(unittest.TestCase):
        def test_returns_correct_version(self):
               self.assertEqual(VERSION, "v0.0.1")

class TestTemperatureSensor(unittest.TestCase):
    """Test that the temperature sensor returns the correct value."""
    
    def test_valid_temperature_sensor(self):
        mock_response = {
            'sensors': [
                {'title': 'Other', 'lastMeasurement': {'value': '10.0'}},
                {'title': 'Temperatur', 'lastMeasurement': {'value': '23.5'}},
            ]
        }
        
        result = get_temp(mock_response)
        
        self.assertIsInstance(result, float)
        self.assertEqual(result, 23.5)

    @patch('main.httpx.get')
    def test_temp_endpoint(self, mock_get):
        mock_get.return_value.json.return_value = {
            'sensors': [
                {'title': 'Temperatur', 'lastMeasurement': {'value': '20.0'}},   
            ]
        }
        result = temp_endpoint()
        self.assertEqual(result, "Good")

class Testintegration(unittest.TestCase):
    def test_temp_integration(self):
        response = client.get("/temperature")
        assert response.status_code == 200

if __name__ == '__main__':
        unittest.main()