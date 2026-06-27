import httpx
import os
import uuid

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

url = os.getenv("BASE_URL") + "cds_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)

class CdsCreate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    package: str
    source: str

class CdsUpdate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    source: str

async def create_cds_view(cds: CdsCreate) -> str:
    """Creates a new CDS view.

    Args:
        cds: A CdsCreate object containing the necessary information to create the CDS view.

    Returns:
        A message indicating the result of the operation.
    """
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:
        try:
            response = client.post(url, json=cds.model_dump())

            return response.text
        
        except Exception as e:
            return f"Error: {e}"

async def read_cds_view(name: str) -> str:
    """Returns the source code of a CDS view.

    Args:
        name: The name of the CDS view to look up.

    Returns:
        The source code of the CDS view.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.get(url, params={"name": name, "r": str(uuid.uuid4())})

            return response.text

        except Exception as e:
            return f"Error: {e}"


async def update_cds_view(cds: CdsUpdate) -> str:
    """Updates an existing CDS view.

    Args:
        cds: A CdsUpdate object containing the updated information for the CDS view.

    Returns:
        A message indicating the result of the operation.
    """
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:
        try:
            response = client.put(url, json=cds.model_dump())

            return response.text
        
        except Exception as e:
            return f"Error: {e}"

async def delete_cds_view(name: str, transport_request: str) -> str:
    """Deletes a CDS view.

    Args:
        name: The name of the CDS view to delete.
        transport_request: The transport request associated with the CDS view to delete.

    Returns:
        A message indicating the result of the operation.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.delete(url, params={"name": name, "transport_request": transport_request, "r": str(uuid.uuid4())})

            return response.text

        except Exception as e:
            return f"Error: {e}"

def get_tools():
    return [
        ("create_cds_view", create_cds_view),
        ("read_cds_view", read_cds_view),
        ("update_cds_view", update_cds_view),
        ("delete_cds_view", delete_cds_view),
    ]