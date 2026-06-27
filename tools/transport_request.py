import httpx
import os
import uuid

from dotenv import load_dotenv

load_dotenv()

url = os.getenv("BASE_URL") + "transport_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)

async def read_transport_request(transport_request: str) -> str:
    """Returns the description of a transport request.

    Args:
        transport_request: The transport request number to look up.

    Returns:
        A string describing the transport request (description, owner, creation date, etc.).
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.get(url, params={"transport": transport_request, "r": str(uuid.uuid4())})

            return response.text

        except Exception as e:
            return f"Error: {e}"
        
async def search_transport_requests(description: str, modifiable: bool = True, released: bool = False, workbench: bool = True, customizing: bool = True, transport_of_copies: bool = True) -> str:
    """Searches for transport requests based on the provided criteria.
    
    Args:
        description: A string to search for in the transport request descriptions.
        modifiable: Whether to include modifiable transport requests in the search results (default: True).
        released: Whether to include released transport requests in the search results (default: False).
        workbench: Whether to include workbench transport requests in the search results (default: True).
        customizing: Whether to include customizing transport requests in the search results (default: True).
        transport_of_copies: Whether to include transport of copies in the search results (default: True).
    
    Returns:
        A string containing the search results, which may include transport request numbers and their descriptions.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:
    
        try:

            params = {
                "description": description, 
                "modifiable": "true" if modifiable else "false",
                "released": "true" if released else "false",
                "workbench": "true" if workbench else "false",
                "customizing": "true" if customizing else "false",
                "transport_of_copies": "true" if transport_of_copies else "false",
                "r": str(uuid.uuid4()),
                } 
    
            response = client.get(url + "/search", params=params)
    
            return response.text
    
        except Exception as e:
            return f"Error: {e}"


async def release_transport_request(transport_request: str) -> str:
    """Releases a transport request.

    Args:
        transport_request: The transport request number to release.

    Returns:
        The result of the release operation, either success or failure with an error message.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.put(url + "/release", params={"transport": transport_request, "r": str(uuid.uuid4())})

            return response.text

        except Exception as e:
            return f"Error: {e}"    

async def change_transport_request_description(transport_request: str, new_description: str) -> str:
    """Changes the description of a transport request.

    Args:
        transport_request: The transport request number to modify.
        new_description: The new description for the transport request.

    Returns:
        The result of the modification operation, either success or failure with an error message.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.put(url + "/change_description", params={"transport": transport_request, "description": new_description, "r": str(uuid.uuid4())})

            return response.text

        except Exception as e:
            return f"Error: {e}"       

def get_tools():
    return [
        ("read_transport_request", read_transport_request),
        ("search_transport_requests", search_transport_requests),
        ("release_transport_request", release_transport_request),
        ("change_transport_request_description", change_transport_request_description),
    ]
