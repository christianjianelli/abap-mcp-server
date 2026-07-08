from email.mime import message

import httpx
import os
import uuid

from dotenv import load_dotenv
from pydantic import BaseModel

class Message(BaseModel):
    messageClass: str
    messageNumber: int
    messageText: str
    transportRequest: str

class TranslateMessage(BaseModel):
    messageClass: str
    messageNumber: int
    messageText: str
    language: str
    transportRequest: str

load_dotenv()

url = os.getenv("BASE_URL") + "message_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)

async def create_message(message: Message) -> str:

    """Creates a new message in the SAP system based on the provided information.

    Args:
        message: A Message object containing the necessary information to create the message.

    Returns:
        A string indicating the result of the creation operation.
    """
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.post(url, json=message.model_dump())
    
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

async def read_message(messageClass: str, messageNumber: int, language: str = "") -> str:
    """Returns the message information for a specific message.

    Args:
        messageClass: The message class to look up.
        messageNumber: The number of the message to look up.
        language: The language for the message (optional). If not provided, the original language will be used.

    Returns:
        A string describing the message.
    """
    
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.get(url, params={"message_class": messageClass, "message_number": messageNumber, "language": language, "r": str(uuid.uuid4())})

        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text

async def update_message(message: Message) -> str:

    """Updates an existing message in the SAP system based on the provided information.

    Args:
        message: A Message object containing the necessary information to update the message.

    Returns:
        A string indicating the result of the update operation.
    """
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.put(url, json=message.model_dump())
    
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text
    
async def translate_message(translateMessage: TranslateMessage) -> str:

    """Translates a message in the SAP system based on the provided information.

    Args:
        message: A TranslateMessage object containing the necessary information to translate the message.

    Returns:
        A string indicating the result of the translate operation.
    """
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.put(url, json=translateMessage.model_dump())
    
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text
    
async def delete_message(messageClass: str, messageNumber: int) -> str:

    """Deletes an existing message in the SAP system based on the provided information.

    Args:
        messageClass: The class of the message to delete.
        messageNumber: The number of the message to delete.

    Returns:
        A string indicating the result of the delete operation.
    """
    with httpx.Client(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = client.delete(url, params={"message_class": messageClass, "message_number": messageNumber, "transport_request": "NPLK900125"})
    
        except Exception as e:
            return f"Error: {e}"
        
        if response.is_error:
            return f"Error: {response.status_code} - {response.reason_phrase}"
        
        return response.text
    
def get_tools():
    return [
        ("create_message", create_message),
        ("read_message", read_message),
        ("update_message", update_message),
        ("delete_message", delete_message),
    ]