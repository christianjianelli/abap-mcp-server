import httpx
import os
import uuid

from dotenv import load_dotenv
from pydantic import BaseModel

class FunctionGroupCreate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    package: str

class FunctionGroupUpdate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str

load_dotenv()

url = os.getenv("BASE_URL") + "func_group_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)


async def read_function_group(name: str) -> str:
    """Returns the description, package and source code of an ABAP function group.

    Args:
        name: The name of the ABAP function group to look up.

    Returns:
        The description, package and source code of the ABAP function group.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.get(url, params={"name": name, "r": str(uuid.uuid4())})
        
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text
    
async def search_function_groups(package: str, name: str = "", description: str = "") -> str:
    """Returns a list of ABAP function groups matching the search criteria.

    Args:
        package: The package containing the ABAP function group.
        name: The name of the ABAP function group to look up.
        description: A description of the ABAP function group.

    Returns:
        A list of ABAP function groups matching the search criteria.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.get(url, params={"package": package, "name": name, "description": description, "r": str(uuid.uuid4())})
       
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text
    
async def create_function_group(functionGroupCreate: FunctionGroupCreate) -> str:
    """Creates a new ABAP function group.

    Args:
        functionGroupCreate: An instance of FunctionGroupCreate containing the function group details.

    Returns:
        A message indicating whether the creation was successful or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.post(url, json=functionGroupCreate.model_dump())

        
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text    
    
async def update_function_group(functionGroupUpdate: FunctionGroupUpdate) -> str:
    """Updates an existing ABAP function group.

    Args:
        functionGroupUpdate: An instance of FunctionGroupUpdate containing the updated function group details.

    Returns:
        A message indicating whether the update was successful or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.put(url, json=functionGroupUpdate.model_dump())

        
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text    
    
async def check_function_group_syntax(name: str) -> str:
    """Perform a syntax check on the source code of an ABAP function group.

    Args:
        name: The name of the ABAP function group to check.

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
    
async def activate_function_group(name: str) -> str:
    """Activates the source code of an ABAP function group.

    Args:
        name: The name of the ABAP function group to look up.

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

def get_tools():
    return [
        ("read_function_group", read_function_group),
        ("search_function_groups", search_function_groups),
        ("create_function_group", create_function_group),
        ("update_function_group", update_function_group),
        ("check_function_group_syntax", check_function_group_syntax),
        ("activate_function_group", activate_function_group),
    ]
