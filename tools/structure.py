import httpx
import os
import uuid

from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

class Component(BaseModel):
    fieldName: str
    description: str
    shortDescription: str
    dataElement: str
    dataType: str
    length: int
    decimals: int = 0
    refField: str

class StructureCreate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    package: str
    components: List[Component]

class StructureUpdate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    components: List[Component]    

load_dotenv()

url = os.getenv("BASE_URL") + "structure_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)

async def read_structure(name: str) -> str:
    """Returns the technical information of a structure and its fields.

    Args:
        name: The name of the structure to look up.

    Returns:
        A string describing the structure (description, fields, etc.).
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.get(url, params={"name": name, "r": str(uuid.uuid4())})

        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text
        
async def search_structures(package: str, name: str = "", description: str = "") -> str:
    """Returns the technical information of a structure and its fields.

    Args:
        package: The package to which the structure belongs (mandatory).
        name: The name (or part of the name) of the structure to look up (optional).
        description: A description for the structure (optional).

    Returns:
        A string with a list of structures containing their names and descriptions.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.get(url, params={"name": name, "package": package, "description": description, "r": str(uuid.uuid4())})

        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

async def create_structure(structure: StructureCreate) -> str:

    """Creates a new structure in the SAP system based on the provided information.
    
    Args:
        structure: A StructureCreate object containing the necessary information to create the structure.

    Returns:
        A string indicating the result of the creation operation.
    """
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.post(url, json=structure.model_dump())
    
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text
        
async def update_structure(structure: StructureUpdate) -> str:

    """Updates an existing structure in the SAP system based on the provided information.
    
    Args:
    structure: 
        A StructureUpdate object containing the necessary information to update the structure.
    
    Returns:
        A string indicating the result of the update operation.
    
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.put(url, json=structure.model_dump())
    
        except Exception as e:
            return f"Error: {e}"        
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

def get_tools():
    return [
        ("read_structure", read_structure),
        ("search_structures", search_structures),
        ("create_structure", create_structure),
        ("update_structure", update_structure),
    ]
