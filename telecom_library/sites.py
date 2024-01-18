from typing import Any, Dict, List

from telecom_library.database import DatabaseConnector


def get_site_inventory(
    db_connector: DatabaseConnector, site_id: str
) -> List[Dict[str, Any]]:
    """
    Get site inventory for a specific site ID.

    Parameters:
    - db_connector (DatabaseConnector): An instance of DatabaseConnector.
    - site_id (str): The ID of the site.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries representing site inventory details.
    """
    query = f"SELECT * FROM baseband_info WHERE site_id = '{site_id}';"
    return db_connector.execute_query(query)

from typing import Optional

def get_site_id_for_incident(
    db_connector: DatabaseConnector, event_id: str
) -> Optional[str]:
    query = f"""
        SELECT site_id
        FROM site_events
        WHERE event_id = '{event_id}';
    """
    result = db_connector.execute_query(query)
    
    # Check if there is a result
    if result:
        return result[0].get("site_id")
    else:
        return None
    
from typing import Optional

def get_slack_member_id_for_site_manager(
    db_connector: DatabaseConnector, site_id: str
) -> Optional[str]:
    query = f"""
        SELECT ud.slack_member_id
        FROM baseband_info bi
        JOIN user_details ud ON bi.site_manager = ud.user_id
        WHERE bi.site_id = '{site_id}';
    """
    result = db_connector.execute_query(query)
    
    # Check if there is a result
    if result:
        return result[0].get("slack_member_id")
    else:
        return None

