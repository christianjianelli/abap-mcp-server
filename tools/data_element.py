import uuid
import httpx
import os

from pydantic import BaseModel
from dotenv import load_dotenv

class DataElementCreate(BaseModel):
    name: str
    shortDescription: str
    domainName: str
    dataType: str
    length: int
    decimals: int = 0
    labelShort: str
    labelMedium: str
    labelLong: str
    labelHeading: str
    transportRequest: str
    package: str

class DataElementUpdate(BaseModel):
    name: str
    shortDescription: str
    domainName: str
    dataType: str
    length: int
    decimals: int = 0
    labelShort: str
    labelMedium: str
    labelLong: str
    labelHeading: str
    transportRequest: str

class DataElementTranslation(BaseModel):
    name: str
    shortDescription: str
    labelShort: str
    labelMedium: str
    labelLong: str
    labelHeading: str
    language: str
    transportRequest: str


load_dotenv()

url = os.getenv("BASE_URL") + "data_element_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)

async def read_data_element(name: str) -> str:
    """Returns the ABAP data element technical information.

    Args:
        name: The data element name to look up.

    Returns:
        A string describing the data element (type, length, decimal places, description, etc.).
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.get(url, params={"name": name, "r": str(uuid.uuid4())})
    
        except Exception as e:
            return f"Error: {e}"

        if response.status_code == 200:
            return response.text
        else:
            return f"Error: {response.status_code} - {response.text}"
        
async def search_data_elements(package: str, name: str = "", description: str = "") -> str:
    """Search for data elements within a package optionally filtered by name.

    Args:
        package: Package name to limit the search.
        name: Optional data element name filter.
        description: Optional data element description filter.
    Returns:
        A string summarizing the matching data elements.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.get(url, params={"package": package, "name": name, "description": description, "r": str(uuid.uuid4())})
    
        except Exception as e:
            return f"Error: {e}"

        if response.status_code == 200:
            return response.text
        else:
            return f"Error: {response.status_code} - {response.text}"

async def create_data_element(data_element: DataElementCreate) -> str:
    """Creates a new ABAP data element based on the provided information.

    Args:
        data_element: A DataElementCreate object containing the details of the data element to create.

    Returns:
        A string indicating success or failure of the creation operation.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.post(url, json=data_element.model_dump())

            return response.text
    
        except Exception as e:
            return f"Error: {e}"       

async def update_data_element(data_element: DataElementUpdate) -> str:
    """Updates an existing ABAP data element based on the provided information.

    Args:
        data_element: A DataElementUpdate object containing the updated details of the data element.

    Returns:
        A string indicating success or failure of the update operation.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.put(url, json=data_element.model_dump())

            return response.text
    
        except Exception as e:
            return f"Error: {e}"

async def translate_data_element(translation: DataElementTranslation) -> str:
    
    """Sets a translation for an existing ABAP data element.

    Args:
        translation: A DataElementTranslation object containing the translation details.

    Returns:
        A string indicating success or failure of the translation operation.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.put(url + "/set_translation", json=translation.model_dump())

            return response.text
        
        except Exception as e:
            return f"Error: {e}"

async def get_data_element_translation(name: str) -> str:

    """Retrieves the translation of an ABAP data element for a specific language.

    Args:
        name: The name of the data element to retrieve the translation for.
        
        Returns:
        A string containing the translation details of the data element.
    
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:
        try:
    
            response = client.get(url + "/get_translation", params={"name": name, "r": str(uuid.uuid4())})

            return response.text

        except Exception as e:
            return f"Error: {e}"


def get_tools():
    return [
        ("read_data_element", read_data_element),
        ("search_data_elements", search_data_elements),
        ("create_data_element", create_data_element),
        ("update_data_element", update_data_element),
        ("translate_data_element", translate_data_element),
        ("get_data_element_translation", get_data_element_translation),
    ]
