import httpx
import os
import uuid

from typing import Any, Dict
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("BASE_URL") + "sql_mcp"
username = os.getenv("SAP_USERNAME")
password = os.getenv("SAP_PASSWORD")
auth = httpx.BasicAuth(username=username, password=password)

async def execute_sql_query(fieldlist: str, table: str, where_clause: str) -> str:
    """Executes a SQL query on the SAP system and returns the results.

    Args:
        fieldlist: A comma-separated list of fields to select (e.g. "FIELD1, FIELD2"). Field names should be in uppercase.
        table: The name of the table to query. Table names should be in uppercase.
        where_clause: The WHERE clause to filter the results (e.g. "FIELD1 = 'value'"). Field names should be in uppercase.

    Returns:
        A string containing the results of the query, or an error message if the query fails.
    """
    
    async with httpx.AsyncClient(auth=auth, verify=False, timeout=60) as client:

        try:
    
            response = await client.get(url, params={"fieldlist": fieldlist, "table": table, "where": where_clause, "r": str(uuid.uuid4())})

            return response.text

        except Exception as e:
            return f"Error: {e}"
        
async def execute_sql_insert(table: str, data: Dict[str, Any]) -> str:
    """Executes a SQL INSERT statement on the SAP system and returns the result.

    Args:
        table: The name of the table to insert into. Table names should be in uppercase.
        data: A dictionary containing the field names as keys and their corresponding values. Field names should be in uppercase.

    Returns:
        A string containing the result of the INSERT statement, or an error message if the statement fails.
    """

    async with httpx.AsyncClient(auth=auth, verify=False, timeout=60) as client:

        try:

            response = await client.post(url, params={"table": table, "r": str(uuid.uuid4())}, json=data)

            return response.text

        except Exception as e:
            return f"Error: {e}"
        
async def execute_sql_update(table: str, fieldlist: str, where_clause: str) -> str:
    """Executes a SQL UPDATE statement on the SAP system and returns the result.

    Args:
        fieldlist: A comma-separated list of fields to update (e.g. "FIELD1 = 'value1', FIELD2 = 'value2'"). Field names should be in uppercase.
        table: The name of the table to update. Table names should be in uppercase.
        where_clause: The WHERE clause to filter the records to update (e.g. "FIELD1 = 'value'"). Field names should be in uppercase.

    Returns:
        A string containing the result of the UPDATE statement, or an error message if the statement fails.
    """

    async with httpx.AsyncClient(auth=auth, verify=False, timeout=60) as client:

        try:

            response = await client.put(url, params={"table": table, "fieldlist": fieldlist, "where": where_clause, "r": str(uuid.uuid4())})

            return response.text

        except Exception as e:
            return f"Error: {e}"

async def execute_sql_delete(table: str, where_clause: str) -> str:
    """Executes a SQL DELETE statement on the SAP system and returns the result.

    Args:
        table: The name of the table to delete from. Table names should be in uppercase.
        where_clause: The WHERE clause to filter the records to delete (e.g. "FIELD1 = 'value'"). Field names should be in uppercase.

    Returns:
        A string containing the result of the DELETE statement, or an error message if the statement fails.
    """

    async with httpx.AsyncClient(auth=auth, verify=False, timeout=60) as client:

        try:

            response = await client.delete(url, params={"table": table, "where": where_clause, "r": str(uuid.uuid4())})

            return response.text

        except Exception as e:
            return f"Error: {e}"

def get_tools():
    return [
        ("execute_sql_query", execute_sql_query),
        ("execute_sql_insert", execute_sql_insert),
        ("execute_sql_update", execute_sql_update),
        ("execute_sql_delete", execute_sql_delete)
    ]
