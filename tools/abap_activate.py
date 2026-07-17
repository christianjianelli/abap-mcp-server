import httpx
import os
import uuid

from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

class Object(BaseModel):
    object: str
    objName: str
    
class Objects(BaseModel):
    objects: List[Object]


load_dotenv()

url = os.getenv("BASE_URL") + "abap_activate_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)

async def mass_activate(objects: Objects) -> str:
    """Activates multiple objects in the SAP ABAP system based on the provided objects list.

    Args:
        objects: An Objects object containing the technical information of the objects to be activated.

    Returns:
        A string indicating the success or failure of the objects activation.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.put(url, json=objects.model_dump())

        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text
    
async def mass_activate_for_transport_request(transport_request: str) -> str:
    """Activates multiple objects in the SAP ABAP system based on the provided transport request.

    Args:
        transport_request: The transport request containing the objects to be activated.

    Returns:
        A string indicating the success or failure of the objects activation.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.put(url, params={"transport_request": transport_request, "r": str(uuid.uuid4())})

        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

async def get_allowed_object_types() -> str:
    """Returns the allowed object types for mass activation. Examples: DOMA, DTEL, CLAS, TABL, etc

    Args:
        None

    Returns:
        A string containing the allowed object types for mass activation.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.get(url, params={"r": str(uuid.uuid4())})
       
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

def get_tools():
    return [
        ("mass_activate", mass_activate),
        ("mass_activate_for_transport_request", mass_activate_for_transport_request),
        ("get_allowed_object_types", get_allowed_object_types)
    ]