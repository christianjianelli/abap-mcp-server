from email.mime import message

import httpx
import os
import uuid

from dotenv import load_dotenv
from pydantic import BaseModel

class CreateMessageClass(BaseModel):
    name: str
    shortDescription: str
    package: str
    transportRequest: str

class UpdateMessageClass(BaseModel):
    name: str
    shortDescription: str
    transportRequest: str

load_dotenv()

url = os.getenv("BASE_URL") + "message_class_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)

async def create_message_class(messageClass: CreateMessageClass) -> str:

    """Creates a new message class in the SAP system based on the provided information.

    Args:
        message: A CreateMessageClass object containing the necessary information to create the message class.

    Returns:
        A string indicating the result of the creation operation.
    """
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.post(url, json=messageClass.model_dump())
    
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

async def read_message_class(messageClass: str) -> str:
    """Returns the description of a transport request.

    Args:
        messageClass: The message class to look up.

    Returns:
        A string describing the message class (description, owner, creation date, etc.).
    """

    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.get(url, params={"name": messageClass, "r": str(uuid.uuid4())})

        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

async def update_message_class(messageClass: UpdateMessageClass) -> str:

    """Updates an existing message class in the SAP system based on the provided information.

    Args:
        message: A UpdateMessageClass object containing the necessary information to update the message class.

    Returns:
        A string indicating the result of the update operation.
    """
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.put(url, json=messageClass.model_dump())
    
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text


def get_tools():
    return [
        ("create_message_class", create_message_class),
        ("read_message_class", read_message_class),
        ("update_message_class", update_message_class),
    ]
