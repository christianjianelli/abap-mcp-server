import httpx
import os
import uuid

from dotenv import load_dotenv

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

            return response.text
        
        except Exception as e:
            return f"Error: {e}"


def get_tools():
    return [
        ("read_program", read_program),
    ]
