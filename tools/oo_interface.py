import httpx
import os
import uuid

from dotenv import load_dotenv
from pydantic import BaseModel

class InterfaceCreate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    package: str

class InterfaceUpdate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    sourceCode: str

load_dotenv()

url = os.getenv("BASE_URL") + "oo_interface_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)


async def read_interface(name: str) -> str:
    """Returns the source code of an ABAP interface.

    Args:
        name: The name of the ABAP interface to look up.

    Returns:
        The source code of the ABAP interface.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
            response = client.get(url, params={"name": name, "r": str(uuid.uuid4())})

            return response.text
        
        except Exception as e:
            return f"Error: {e}"


async def search_interfaces(package: str, name: str = "", description: str = "") -> str:
    """Returns a list of ABAP interfaces matching the search criteria.

    Args:
        package: The package containing the ABAP interface.
        name: The name of the ABAP interface to look up.
        description: A description of the ABAP interface.

    Returns:
        A list of ABAP interfaces matching the search criteria.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
            response = client.get(url, params={"package": package, "name": name, "description": description, "r": str(uuid.uuid4())})

            return response.text
        
        except Exception as e:
            return f"Error: {e}"


def get_tools():
    return [
        ("read_interface", read_interface),
        ("search_interfaces", search_interfaces),
    ]
