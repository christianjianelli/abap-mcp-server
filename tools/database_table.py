import httpx
import os
import uuid

from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

class Component(BaseModel):
    fieldName: str
    keyFlag: bool = False
    shortDescription: str
    dataElement: str
    dataType: str
    length: int
    decimals: int = 0
    refField: str

class DatabaseTableCreate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    package: str
    components: List[Component]

class DatabaseTableUpdate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    components: List[Component]

load_dotenv()

url = os.getenv("BASE_URL") + "db_table_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)

async def read_database_table(name: str) -> str:
    """Returns the technical information of a database table and its fields.

    Args:
        name: The name of the database table to look up.

    Returns:
        The technical information of the database table and its fields.
    """
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:
        
        try:
    
            response = client.get(url, params={"name": name, "r": str(uuid.uuid4())})

            return response.text

        except Exception as e:
            return f"Error: {e}"
    
async def search_database_tables(package: str, name: str = "", description: str = "") -> str:
    """Returns the technical information of a database table and its fields.

    Args:
        package: The package to which the database table belongs (mandatory).
        name: The name (or part of the name) of the database table to look up (optional).
        description: A description for the database table (optional).

    Returns:
        A string with a list of database tables containing their names and descriptions.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.get(url, params={"name": name, "package": package, "description": description, "r": str(uuid.uuid4())})

            return response.text

        except Exception as e:
            return f"Error: {e}"
        
async def create_database_table(table: DatabaseTableCreate) -> str:
    """Creates a database table in the SAP ABAP system based on the provided technical information.
    
    Args:
        table: A DatabaseTableCreate object containing the technical information of the database table to be created.

    Returns:
        A string indicating the success or failure of the database table creation.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.post(url, json=table.model_dump())

            return response.text
    
        except Exception as e:
            return f"Error: {e}"
        
async def update_database_table(table: DatabaseTableUpdate) -> str:
    """Updates a database table in the SAP ABAP system based on the provided technical information.

    Args:
        table: A DatabaseTableUpdate object containing the technical information of the database table to be updated.

    Returns:
        A string indicating the success or failure of the database table update.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.put(url, json=table.model_dump())

            return response.text
    
        except Exception as e:
            return f"Error: {e}"

def get_tools():
    return [
        ("read_database_table", read_database_table),
        ("search_database_tables", search_database_tables),
        ("create_database_table", create_database_table),
        ("update_database_table", update_database_table),
    ]
