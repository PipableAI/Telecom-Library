# tests/test_main.py
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock
from telecom_library.database import DatabaseConnector
from telecom_library.incident_analyser import (
    get_baseband_change_events,
    get_cm_policy_by_baseband_type,
    get_cm_profile_mismatch_events
)

class TestMainFunctions(unittest.TestCase):

    def setUp(self):
        # Create a mock database connector for testing
        self.db_connector = MagicMock(spec=DatabaseConnector)

    def test_get_baseband_change_events(self):
        # Set up a timestamp two days ago
        timestamp_two_days_ago = datetime.utcnow() - timedelta(days=2)
        
        # Mocking the execute_query result for get_baseband_change_events
        self.db_connector.execute_query.return_value = [
            {"site_id": "14883_Lala_Land_Hilltop", "event_id": "INC0010003", "event_detail": "Baseband replacement", "event_timestamp": timestamp_two_days_ago}
        ]

        result = get_baseband_change_events(self.db_connector, site_id="14883_Lala_Land_Hilltop")
        
        # Calculate 'days ago' based on the event timestamp
        days_ago = (datetime.utcnow() - timestamp_two_days_ago).days

        expected_result = [{"site_id": "14883_Lala_Land_Hilltop", "event_id": "INC0010003", "event_detail": "Baseband replacement", "event_timestamp": timestamp_two_days_ago, "days_ago": days_ago}]
        self.assertEqual(result, expected_result)

    def test_get_cm_policy_by_baseband_type(self):
        # Mocking the execute_query result for get_cm_policy_by_baseband_type
        self.db_connector.execute_query.return_value = [{"cm_profile": "1234567890.prf"}]

        result = get_cm_policy_by_baseband_type(self.db_connector, baseband_type="DUX3423")
        self.assertEqual(result, "1234567890.prf")

    def test_get_cm_profile_mismatch_events(self):
        # Mocking the execute_query result for get_cm_profile_mismatch_events
        self.db_connector.execute_query.return_value = [
            {"site_id": "14883_Lala_Land_Hilltop", "event_id": "INC0010003", "event_detail": "Mismatch", "cm_profile": "7890123455.prf"}
        ]

        result = get_cm_profile_mismatch_events(self.db_connector)
        expected_result = [{"site_id": "14883_Lala_Land_Hilltop", "event_id": "INC0010003", "event_detail": "Mismatch", "cm_profile": "7890123455.prf"}]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
