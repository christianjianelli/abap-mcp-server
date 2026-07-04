import httpx
import os
import uuid

from dotenv import load_dotenv
from pydantic import BaseModel

class IncludeCreate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    package: str

class IncludeUpdate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    sourceCode: str

load_dotenv()

url = os.getenv("BASE_URL") + "prog_include_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)


async def read_include(name: str) -> str:
    """Returns the source code of an ABAP include.

    Args:
        name: The name of the ABAP include to look up.

    Returns:
        The source code of the ABAP include.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.get(url, params={"name": name, "r": str(uuid.uuid4())})
       
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

async def search_includes(package: str, name: str = "", description: str = "") -> str:
    """Returns a list of ABAP includes matching the search criteria.

    Args:
        package: The package containing the ABAP include.
        name: The name of the ABAP include to look up.
        description: A description of the ABAP include.

    Returns:
        A list of ABAP includes matching the search criteria.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.get(url, params={"package": package, "name": name, "description": description, "r": str(uuid.uuid4())})
       
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

async def create_include(includeCreate: IncludeCreate) -> str:
    """Creates a new ABAP include.

    Args:
        includeCreate: An instance of IncludeCreate containing the include details.

    Returns:
        A message indicating whether the creation was successful or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.post(url, json=includeCreate.model_dump())

        
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text


async def update_include(includeUpdate: IncludeUpdate) -> str:
    """Updates an existing ABAP include.

    Args:
        includeUpdate: An instance of IncludeUpdate containing the updated include details.

    Returns:
        A message indicating whether the update was successful or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.put(url, json=includeUpdate.model_dump())

        
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text
    
async def activate_include(name: str) -> str:
    """Activates the source code of an ABAP include.

    Args:
        name: The name of the ABAP include to look up.

    Returns:
        A message indicating whether the activation was successful or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.get(url + "/activate", params={"name": name, "r": str(uuid.uuid4())})
        
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text
    
async def check_include_syntax(name: str) -> str:
    """Perform a syntax check on the source code of an ABAP include.

    Args:
        name: The name of the ABAP include to check.

    Returns:
        A message indicating whether the source code is syntactically correct or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.get(url + "/check", params={"name": name, "r": str(uuid.uuid4())})
        
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

def get_tools():
    return [
        ("read_include", read_include),
        ("search_includes", search_includes),
        ("create_include", create_include),
        ("update_include", update_include),
        ("activate_include", activate_include),
        ("check_include_syntax", check_include_syntax),
    ]
