import httpx
import os
import uuid

from pydantic import BaseModel

from dotenv import load_dotenv

class TableTypeCreate(BaseModel):
    name: str
    shortDescription: str
    rowType: str
    transportRequest: str
    package: str

class TableTypeUpdate(BaseModel):
    name: str
    shortDescription: str
    rowType: str
    transportRequest: str

load_dotenv()

url = os.getenv("BASE_URL") + "table_type_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)

async def read_table_type(name: str) -> str:
    """Returns the technical information of a table type and its fields.

    Args:
        name: The name of the table type to look up.

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

async def search_table_types(package: str, name: str = "", description: str = "") -> str:
    """Returns the technical information of a table type and its fields.

    Args:
        package: The package to which the table type belongs (mandatory).
        name: The name (or part of the name) of the table type to look up (optional).
        description: A description for the table type (optional).

    Returns:
        A string with a list of table types containing their names and descriptions.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.get(url, params={"name": name, "package": package, "description": description, "r": str(uuid.uuid4())})

        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

async def create_table_type(table_type: TableTypeCreate) -> str:

    """Creates a new table type in the SAP system.
    
    Args:
        table_type: A TableTypeCreate object containing the necessary information to create the table type.

    Returns:
        A string indicating the result of the creation operation.
    """
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.post(url, json=table_type.model_dump())
    
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text
        
async def update_table_type(table_type: TableTypeUpdate) -> str:
    
    """Updates an existing table type in the SAP system based on the provided information.

    Args:
        table_type: A TableTypeUpdate object containing the necessary information to update the table type.

    Returns:
        A string indicating the result of the update operation.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.put(url, json=table_type.model_dump())
    
        except Exception as e:
            return f"Error: {e}"    
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

def get_tools():
    return [
        ("read_table_type", read_table_type),
        ("search_table_types", search_table_types),
        ("create_table_type", create_table_type),
        ("update_table_type", update_table_type),
    ]
