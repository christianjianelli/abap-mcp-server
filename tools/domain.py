import httpx
import os
import uuid

from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

class FixedValue(BaseModel):
    value: str
    description: str


class DomainCreate(BaseModel):
    name: str
    shortDescription: str
    dataType: str
    length: int
    decimals: int = 0
    caseSensitive: bool = False
    transportRequest: str
    package: str
    fixedValues: List[FixedValue] | None = None

class DomainUpdate(BaseModel):
    name: str
    shortDescription: str
    dataType: str
    length: int
    decimals: int = 0
    caseSensitive: bool = False
    transportRequest: str
    fixedValues: List[FixedValue] | None = None

class DomainTranslate(BaseModel):
    name: str
    shortDescription: str
    language: str
    transportRequest: str
    fixedValues: List[FixedValue] | None = None

load_dotenv()

url = os.getenv("BASE_URL") + "domain_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)

async def read_domain(name: str) -> str:
    """Returns the ABAP domain technical information.

    Args:
        name: The domain name to look up.

    Returns:
        A string describing the domain (type, length, decimal places, description, etc.).
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.get(url, params={"name": name, "r": str(uuid.uuid4())})

            return response.text

        except Exception as e:
            return f"Error: {e}"
        
async def search_domains(package: str, name: str = "", description: str = "") -> str:
    """Search for domains within a package optionally filtered by name.

    Args:
        package: Package name to limit the search.
        name: Optional domain name filter.
        description: Optional domain description filter.

    Returns:
        A string summarizing the matching domains.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.get(url, params={"package": package, "name": name, "description": description, "r": str(uuid.uuid4())})

            return response.text
    
        except Exception as e:
            return f"Error: {e}"

async def create_domain(domain: DomainCreate) -> str:
    """Creates a new ABAP domain based on the provided definition.

    Args:
        domain: A DomainCreate object containing all necessary information to create the domain.

    Returns:
        A string indicating success or failure of the domain creation.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.post(url, json=domain.model_dump())

            return response.text
    
        except Exception as e:
            return f"Error: {e}"       
        
async def update_domain(domain: DomainUpdate) -> str:
    """Updates an existing ABAP domain based on the provided definition.

    Args:
        domain: A DomainUpdate object containing all necessary information to update the domain.

    Returns:
        A string indicating success or failure of the domain update.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.put(url, json=domain.model_dump())

            return response.text
    
        except Exception as e:
            return f"Error: {e}"
        
async def translate_domain(domain: DomainTranslate) -> str:
    """Translates the short description and fixed value descriptions of an existing ABAP domain into another language.

    Args:
        domain: A DomainTranslate object containing all necessary information for the translation.

    Returns:
        A string indicating success or failure of the domain translation.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.post(url + "/set_translation?r=" + str(uuid.uuid4()), json=domain.model_dump())

            return response.text
    
        except Exception as e:
            return f"Error: {e}"

async def get_domain_translation(name: str, language: str) -> str:
    """Retrieves the translation of a domain's short description and fixed value descriptions into a specific language.

    Args:
        name: The domain name.
        language: The target language for translation.

    Returns:
        A string containing the translated information.
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.get(url + "/get_translation", params={"name": name, "language": language, "r": str(uuid.uuid4())})

            return response.text
    
        except Exception as e:
            return f"Error: {e}"

def get_tools():
    return [
        ("read_domain", read_domain),
        ("search_domains", search_domains),
        ("create_domain", create_domain),
        ("update_domain", update_domain),
        ("translate_domain", translate_domain),
        ("get_domain_translation", get_domain_translation),
    ]
    
    