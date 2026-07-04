import httpx
import os
import uuid

from dotenv import load_dotenv

load_dotenv()

url = os.getenv("BASE_URL") + "func_module_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)


async def read_function_module(name: str) -> str:
    """Returns the source code of an ABAP function module.

    Args:
        name: The name of the ABAP function module to look up.

    Returns:
        The source code of the ABAP function module.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:

            response = client.get(url, params={"name": name, "r": str(uuid.uuid4())})
        
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

def get_tools():
    return [
        ("read_function_module", read_function_module),
    ]
