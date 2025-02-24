from airport_code_validator import AirportCodeValidator
import unittest
from unittest.mock import patch
import pandas as pd

class TestAirportCodeValidator(unittest.TestCase):
    @patch("pandas.read_csv")
    def test_airports(self, mock_read_csv):
        mock_data = pd.DataFrame({
            "IATA": ["JFK", "ANC", "HNL", "YYZ"],
            "ICAO": ["KJFK", "PANC", "PHNL", "CYYZ"],
            "Country": ["United States", "United States", "United States", "Canada"],
            "Tz Database Timezone": ["America/New_York", "America/Anchorage", "Pacific/Honolulu", "America/Toronto"]
        })
        mock_read_csv.return_value = mock_data

        test_cases = {
            "JFK": True, "KJFK": True,   # Valid US
            "ANC": False, "PANC": False, # Alaska
            "HNL": False, "PHNL": False, # Hawaii
            "YYZ": False, "CYYZ": False, # Non-US
            "FAKE": False                # Non-existent
        }

        for code, expected in test_cases.items():
            with self.subTest(airport_code=code):
                self.assertEqual(AirportCodeValidator.is_valid(code), expected)

if __name__ == "__main__":
    unittest.main()