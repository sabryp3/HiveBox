import unittest
from unittest.mock import patch 
from main import temp_endpoint, get_temp
from version import VERSION

class TestVersion(unittest.TestCase):
        def test_returns_correct_version(self):
               self.assertEqual(VERSION, "v0.0.1")

    # Response contains sensor with 'Temperatur' title and valid float value
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
        


if __name__ == '__main__':
        unittest.main()