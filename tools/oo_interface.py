import httpx
import os
import uuid
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel

class InterfaceCreate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    package: str

class InterfaceUpdate(BaseModel):
    name: str
    shortDescription: Optional[str] = ""
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


async def create_interface(abapInterfaceCreate: InterfaceCreate) -> str:
    """Creates a new ABAP interface.

    Args:
        abapInterface: An instance of InterfaceCreate containing the interface details.

    Returns:
        A message indicating whether the creation was successful or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
            response = client.post(url, json=abapInterfaceCreate.model_dump())

            return response.text
        
        except Exception as e:
            return f"Error: {e}"
        
async def update_interface(abapInterfaceUpdate: InterfaceUpdate) -> str:
    """Updates an existing ABAP interface.

    Args:
        abapInterface: An instance of InterfaceUpdate containing the updated interface details.

    Returns:
        A message indicating whether the update was successful or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
            response = client.put(url, json=abapInterfaceUpdate.model_dump())

            return response.text
        
        except Exception as e:
            return f"Error: {e}"        
        
async def activate_interface(name: str) -> str:
    """Activates the source code of an ABAP interface.

    Args:
        name: The name of the ABAP interface to look up.

    Returns:
        A message indicating whether the activation was successful or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
            response = client.get(url + "/activate", params={"name": name, "r": str(uuid.uuid4())})

            return response.text
        
        except Exception as e:
            return f"Error: {e}"


async def check_interface_syntax(name: str) -> str:
    """Perform a syntax check on the source code of an ABAP interface.

    Args:
        name: The name of the ABAP interface to check.

    Returns:
        A message indicating whether the source code is syntactically correct or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
            response = client.get(url + "/check", params={"name": name, "r": str(uuid.uuid4())})

            return response.text
        
        except Exception as e:
            return f"Error: {e}"

def get_tools():
    return [
        ("read_interface", read_interface),
        ("search_interfaces", search_interfaces),
        ("create_interface", create_interface),
        ("update_interface", update_interface),
        ("activate_interface", activate_interface),
        ("check_interface_syntax", check_interface_syntax),
    ]
