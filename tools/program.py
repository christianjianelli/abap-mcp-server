import httpx
import os
import uuid

from dotenv import load_dotenv
from pydantic import BaseModel

class ProgramCreate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    package: str

class ProgramUpdate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    sourceCode: str

load_dotenv()

url = os.getenv("BASE_URL") + "program_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)


async def read_program(name: str) -> str:
    """Returns the source code of an ABAP program.

    Args:
        name: The name of the ABAP program to look up.

    Returns:
        The source code of the ABAP program.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.get(url, params={"name": name, "r": str(uuid.uuid4())})
       
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

async def search_programs(package: str, name: str = "", description: str = "") -> str:
    """Returns a list of ABAP programs matching the search criteria.

    Args:
        package: The package containing the ABAP program.
        name: The name of the ABAP program to look up.
        description: A description of the ABAP program.

    Returns:
        A list of ABAP programs matching the search criteria.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.get(url, params={"package": package, "name": name, "description": description, "r": str(uuid.uuid4())})
       
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

async def create_program(programCreate: ProgramCreate) -> str:
    """Creates a new ABAP program.

    Args:
        programCreate: An instance of ProgramCreate containing the program details.

    Returns:
        A message indicating whether the creation was successful or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.post(url, json=programCreate.model_dump())

        
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text


async def update_program(programUpdate: ProgramUpdate) -> str:
    """Updates an existing ABAP program.

    Args:
        programUpdate: An instance of ProgramUpdate containing the updated program details.

    Returns:
        A message indicating whether the update was successful or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.put(url, json=programUpdate.model_dump())

        
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text
    
async def activate_program(name: str) -> str:
    """Activates the source code of an ABAP program.

    Args:
        name: The name of the ABAP program to look up.

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
    
async def check_program_syntax(name: str) -> str:
    """Perform a syntax check on the source code of an ABAP program.

    Args:
        name: The name of the ABAP program to check.

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
        ("read_program", read_program),
        ("search_programs", search_programs),
        ("create_program", create_program),
        ("update_program", update_program),
        ("activate_program", activate_program),
        ("check_program_syntax", check_program_syntax),
    ]
