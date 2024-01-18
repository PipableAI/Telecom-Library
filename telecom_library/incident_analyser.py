from datetime import datetime
from typing import Any, Dict, List

from telecom_library.database import DatabaseConnector

def get_cm_policy_by_baseband_type(db_connector: DatabaseConnector, baseband_type: str) -> str:
    """
    Get the Config management (CM) profile for a specific baseband type from the CM policy.

    Parameters:
    - db_connector (DatabaseConnector): An instance of DatabaseConnector for connecting to the database.
    - baseband_type (str): The baseband type for which to retrieve the CM policy.

    Returns:
    - str: The CM profile for the specified baseband type.

    Example:
    get_cm_policy_by_baseband_type(db_connector, 'DUX3423')
    """
    query = f"SELECT cm_profile FROM cm_policy WHERE baseband_type = '{baseband_type}';"
    result = db_connector.execute_query(query)
    return result[0]['cm_profile'] if result else None

def get_cm_profile_mismatch_events(db_connector: DatabaseConnector) -> List[Dict[str, Any]]:
    """
    Get a list of events where the Config management (CM) profile mismatches the expected profile.

    Parameters:
    - db_connector (DatabaseConnector): An instance of DatabaseConnector for connecting to the database.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries representing events with CM profile mismatches.

    Example:
    get_cm_profile_mismatch_events(db_connector)
    """
    query = """
        SELECT bi.site_id, e.event_id, e.event_detail, bi.cm_profile 
        FROM baseband_info bi 
        JOIN site_events se ON bi.site_id = se.site_id
        JOIN events e ON se.event_id = e.event_id
        JOIN cm_policy cp ON bi.baseband_type = cp.baseband_type
        WHERE cp.cm_profile <> bi.cm_profile;
    """
    return db_connector.execute_query(query)

def get_baseband_replacement_events(
    db_connector: DatabaseConnector, site_id: str
) -> List[Dict[str, Any]]:
    query = f"""
        SELECT e.*, se.site_id ,bi.baseband_type
        FROM events e
        JOIN site_events se ON e.event_id = se.event_id
        JOIN baseband_info bi ON se.site_id = bi.site_id
        WHERE se.site_id = '{site_id}' AND e.event_detail = 'Baseband replacement';
    """
    events = db_connector.execute_query(query)

    # Calculate 'days ago' based on the event timestamp
    for event in events:
        event_timestamp = event.get("event_timestamp")
        if event_timestamp:
            event_days_ago = (datetime.utcnow() - event_timestamp).days
            event["days_ago"] = event_days_ago

    return events