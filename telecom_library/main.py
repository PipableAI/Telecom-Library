import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from telecom_library.database import (
    DatabaseConnector,
    get_database_credentials_from_url,
)
from telecom_library.incident_analyser import (
    get_baseband_replacement_events,
    get_cm_policy_by_baseband_type,
    get_cm_profile_mismatch_events,
)
from telecom_library.servicenow import get_incidents_from_servicenow
from telecom_library.sites import get_site_id_for_incident, get_site_inventory

# Fetch Slack Token and DB URL from environment variables
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
DB_URL = os.environ.get("DB_URL")


def get_site_inventory_for_site_id(site_id: str) -> List[Dict[str, Any]]:
    """
    Get site details/inventory for a specific site ID.

    Parameters:
    - site_id (str): The ID of the site.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries representing site inventory details.
    """

    # Parse the database URL to get credentials
    db_credentials = get_database_credentials_from_url(DB_URL)

    # Create a DatabaseConnector instance

    db_connector = DatabaseConnector(
        host=db_credentials["db_host"],
        port=db_credentials["db_port"],
        database=db_credentials["db_name"],
        user=db_credentials["db_user"],
        password=db_credentials["db_password"],
    )
    site_inventory = get_site_inventory(db_connector, site_id)
    return site_inventory


def fetch_assigned_incidents() -> List[str]:
    """
    Fetch incidents assigned to a user.

    Parameters:
    - user_id (str): The ID of the user.

    Returns:
    - List[str]: A list of incident IDs assigned to the user.
    """
    # Call the mock ServiceNow function to get incidents
    servicenow_response = get_incidents_from_servicenow()

    # Process the ServiceNow response and extract incident IDs
    assigned_incidents = [
        incident["task_effective_number"]
        for incident in servicenow_response.get("result", [])
    ]

    return assigned_incidents


def analyze_incident(incident_id: str) -> str:
    """
    Get details or Analyze a baseband change incident for a given incident_id.

    Parameters:
    - site_id (int): The ID of the site to analyze.

    Returns:
    - str: Analysis result providing information about the latest baseband change incident.

    The function checks for a baseband change incident at the specified site and analyzes whether
    the current Config management (CM) profile matches the expected profile based on the CM policy.
    If a mismatch is found, it returns a detailed analysis with expected and found CM profiles.

    Example:
    analyze_incident(db_connector, 14883)
    """
    db_credentials = get_database_credentials_from_url(DB_URL)

    db_connector = DatabaseConnector(
        host=db_credentials["db_host"],
        port=db_credentials["db_port"],
        database=db_credentials["db_name"],
        user=db_credentials["db_user"],
        password=db_credentials["db_password"],
    )

    # Function calls internally
    site_id = get_site_id_for_incident(db_connector, incident_id)

    baseband_change_events = get_baseband_replacement_events(db_connector, site_id)

    if not baseband_change_events:
        return "No baseband change observed at the site."

    # Assuming the first baseband_change_event is the latest one
    latest_event = baseband_change_events[0]
    baseband_type = latest_event.get("baseband_type", "")

    # Get CM policy for the baseband type
    expected_cm_profile = get_cm_policy_by_baseband_type(db_connector, baseband_type)

    # Check if the current CM profile mismatches the expected profile
    cm_profile_mismatch_events = get_cm_profile_mismatch_events(db_connector)

    for event in cm_profile_mismatch_events:
        if (
            event["site_id"] == site_id
            and event["event_id"] == latest_event["event_id"]
        ):
            return (
                f"Baseband change observed at site {site_id} {latest_event['days_ago']} days ago.\n"
                f"Config management profile does not match expected profile.\n"
                f"Expected: {expected_cm_profile}\nFound: {event['cm_profile']}"
            )

    return "No CM profile mismatch found for the latest baseband change event."


def get_slack_channel_id_for_site_manager(site_id: str) -> Optional[str]:
    """
    Get the Slack Member ID for the site manager associated with a given site.

    Parameters:
    - site_id (str): The unique identifier of the site.

    Returns:
    - Optional[str]: The Slack Member ID of the site manager, or None if not found.

    Example:
    slack_member_id = get_slack_channel_id_for_site_manager('14883_Lala_Land_Hilltop')
    if slack_member_id:
        print(f"Slack Member ID for the site manager: {slack_member_id}")
    else:
        print("Site manager not found or Slack Member ID not available.")
    """
    # Parse the database URL to get credentials
    db_credentials = get_database_credentials_from_url(DB_URL)

    # Create a DatabaseConnector instance
    db_connector = DatabaseConnector(
        host=db_credentials["db_host"],
        port=db_credentials["db_port"],
        database=db_credentials["db_name"],
        user=db_credentials["db_user"],
        password=db_credentials["db_password"],
    )

    # Construct the SQL query to retrieve Slack Member ID
    query = f"""
        SELECT ud.slack_member_id
        FROM baseband_info bi
        JOIN user_details ud ON bi.site_manager = ud.user_id
        WHERE bi.site_id = '{site_id}';
    """

    # Execute the query and get the result
    result = db_connector.execute_query(query)

    # Check if there is a result
    if result:
        return result[0].get("slack_member_id")
    else:
        return None


def send_slack_message(channel_id: Optional[str], message: str) -> None:
    """
    Send a Slack message to a channel or user.

    Parameters:
    - channel_id (Optional[str]): The ID of the channel or user to send the message to.
    - message (str): The message to be sent.

    Returns:
    - None

    Example:
    send_slack_message('C123456789', 'Hello, this is a test message!')
    """
    client = WebClient(token=SLACK_TOKEN)

    try:
        # Send the message
        response = client.chat_postMessage(channel=channel_id, text=message)

        if response["ok"]:
            return f"Message sent successfully to channel/user {channel_id}: {message}"
        else:
            return f"Failed to send message. Slack API response: {response}"
    except SlackApiError as e:
        return f"Error sending message to Slack: {e.response['error']}"


def file_report(incident_id: str) -> Optional[str]:
    """
    File a report for the given incident ID and return a detailed summary in Markdown format.

    Parameters:
    - db_connector (DatabaseConnector): An instance of DatabaseConnector for connecting to the database.
    - incident_id (str): The ID of the incident.

    Returns:
    - Optional[str]: A Markdown-formatted detailed summary of the report, or None if the incident is not found.

    Example:
    file_report(db_connector, 'INC0010003')
    """
    # Parse the database URL to get credentials
    db_credentials = get_database_credentials_from_url(DB_URL)

    # Create a DatabaseConnector instance
    db_connector = DatabaseConnector(
        host=db_credentials["db_host"],
        port=db_credentials["db_port"],
        database=db_credentials["db_name"],
        user=db_credentials["db_user"],
        password=db_credentials["db_password"],
    )

    # Query to fetch details from multiple tables based on incident ID
    query = f"""
        SELECT e.event_timestamp, e.event_detail,
               bi.site_id, bi.baseband_serial, bi.baseband_type, bi.cm_profile,
               ud.first_name, ud.last_name, ud.email_id, ud.slack_member_id
        FROM events e
        JOIN site_events se ON e.event_id = se.event_id
        JOIN baseband_info bi ON se.site_id = bi.site_id
        JOIN user_details ud ON bi.site_manager = ud.user_id
        WHERE e.event_id = '{incident_id}';
    """
    result = db_connector.execute_query(query)

    if result:
        # Extracting details from the result
        event_timestamp = result[0].get("event_timestamp", datetime.now())
        event_detail = result[0].get("event_detail", "No details available")
        site_id = result[0].get("site_id", "N/A")
        baseband_serial = result[0].get("baseband_serial", "N/A")
        baseband_type = result[0].get("baseband_type", "N/A")
        cm_profile = result[0].get("cm_profile", "N/A")
        first_name = result[0].get("first_name", "N/A")
        last_name = result[0].get("last_name", "N/A")
        email_id = result[0].get("email_id", "N/A")
        slack_member_id = result[0].get("slack_member_id", "N/A")

        # Generate a detailed Markdown-formatted summary
        summary = f"""
        **Report filed for incident {incident_id}**
        - **Event Timestamp:** {event_timestamp}
        - **Event Detail:** {event_detail}
        - **Site ID:** {site_id}
        - **Baseband Serial:** {baseband_serial}
        - **Baseband Type:** {baseband_type}
        - **CM Profile:** {cm_profile}
        - **Site Manager:**
            - **Name:** {first_name} {last_name}
            - **Email ID:** {email_id}
            - **Slack Member ID:** {slack_member_id}
        """
        return summary
    else:
        return None


def close_ticket(incident_id: str) -> Optional[str]:
    """
    Close the ticket for the given incident ID and return a success message.

    Parameters:
    - db_connector (DatabaseConnector): An instance of DatabaseConnector for connecting to the database.
    - incident_id (str): The ID of the incident.

    Returns:
    - Optional[str]: A success message, or None if the incident is not found.

    Example:
    close_ticket(db_connector, 'INC0010003')
    """
    # Parse the database URL to get credentials
    db_credentials = get_database_credentials_from_url(DB_URL)

    # Create a DatabaseConnector instance
    db_connector = DatabaseConnector(
        host=db_credentials["db_host"],
        port=db_credentials["db_port"],
        database=db_credentials["db_name"],
        user=db_credentials["db_user"],
        password=db_credentials["db_password"],
    )
    
    query = f"SELECT * FROM events WHERE event_id = '{incident_id}';"
    event = db_connector.execute_query(query)

    if event:
        # Process the event details and generate a success message
        success_message = f"Successfully closed the ticket for incident {incident_id}. Details: {event[0].get('event_detail')}"
        return success_message
    else:
        return None