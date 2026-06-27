import httpx
import os
import uuid

from dotenv import load_dotenv
from pydantic import BaseModel

class ClassCreate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    package: str

class ClassUpdate(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str
    sourceCode: str

load_dotenv()

url = os.getenv("BASE_URL") + "oo_class_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)

async def read_class(name: str) -> str:
    """Returns the source code of an ABAP class.

    Args:
        name: The name of the ABAP class to look up.

    Returns:
        The source code of the ABAP class.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
            response = client.get(url, params={"name": name, "r": str(uuid.uuid4())})

            return response.text
        
        except Exception as e:
            return f"Error: {e}"

async def search_classes(package: str, name: str = "", description: str = "") -> str:
    """Returns a list of ABAP classes matching the search criteria.

    Args:
        package: The package containing the ABAP class.
        name: The name of the ABAP class to look up.
        description: A description of the ABAP class.

    Returns:
        A list of ABAP classes matching the search criteria.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
            response = client.get(url, params={"package": package, "name": name, "description": description, "r": str(uuid.uuid4())})

            return response.text
        
        except Exception as e:
            return f"Error: {e}"

async def create_class(abapClassCreate: ClassCreate) -> str:
    """Creates a new ABAP class.

    Args:
        abapClass: An instance of ClassCreate containing the class details.

    Returns:
        A message indicating whether the creation was successful or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
            response = client.post(url, json=abapClassCreate.model_dump())

            return response.text
        
        except Exception as e:
            return f"Error: {e}"

async def update_class(abapClassUpdate: ClassUpdate) -> str:
    """Updates an existing ABAP class.

    Args:
        abapClass: An instance of ClassUpdate containing the updated class details.

    Returns:
        A message indicating whether the update was successful or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
            response = client.put(url, json=abapClassUpdate.model_dump())

            return response.text
        
        except Exception as e:
            return f"Error: {e}"        

async def activate_class(name: str) -> str:
    """Activates the source code of an ABAP class.

    Args:
        name: The name of the ABAP class to look up.

    Returns:
        A message indicating whether the activation was successful or not.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
            response = client.get(url + "/activate", params={"name": name, "r": str(uuid.uuid4())})

            return response.text
        
        except Exception as e:
            return f"Error: {e}"
        
async def check_class_syntax(name: str) -> str:
    """Perform a syntax check on the source code of an ABAP class.

    Args:
        name: The name of the ABAP class to check.

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
        ("read_class", read_class),
        ("search_classes", search_classes),
        ("create_class", create_class),
        ("update_class", update_class),
        ("activate_class", activate_class),
        ("check_class_syntax", check_class_syntax),
    ]
