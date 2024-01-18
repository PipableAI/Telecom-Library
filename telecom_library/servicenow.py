from typing import Any, Dict


def get_incidents_from_servicenow() -> Dict[str, Any]:
    """
    Mock function to retrieve incidents from ServiceNow.

    Parameters:
    - user_id (str): The ID of the user.

    Returns:
    - Dict[str, Any]: A dictionary representing the mock ServiceNow response with incident details.
    """
    return {
        "result": [
            {
                "parent": "",
                "made_sla": "true",
                "caused_by": "",
                "watch_list": "",
                "upon_reject": "cancel",
                "sys_updated_on": "2023-01-08 16:48:44",
                "child_incidents": "0",
                "hold_reason": "",
                "origin_table": "",
                "task_effective_number": "INC0010003",
                "approval_history": "",
                "number": "INC0010003",
                "resolved_by": "",
                "sys_updated_by": "aes.creator",
                "opened_by": {
                    "link": "https://dev139371.service-now.com/api/now/table/sys_user/33a5f6899710211018b7bf1e6253af7b",
                    "value": "33a5f6899710211018b7bf1e6253af7b",
                },
            },
        ]
    }
