import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("SAP_USERNAME")

def get_current_username() -> str:
    """Returns the current username you are logged in as.

    Returns:
        The current username you are logged in as.
    """
    return username 

def get_tools():
    return [
        ("get_current_username", get_current_username),
    ]
    