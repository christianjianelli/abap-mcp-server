from mcp.server.fastmcp import FastMCP
from tools import transport_request, domain, data_element, structure, database_table, table_type, cds, sql, program, function_module, oo_class, oo_interface 

# Initialize FastMCP server
mcp = FastMCP("ABAP")

# Register the ABAP transport request tools
for tool_name, tool_function in transport_request.get_tools():
    mcp.tool(name=tool_name)(tool_function)

# Register the ABAP DDIC domain tools
for tool_name, tool_function in domain.get_tools():
    mcp.tool(name=tool_name)(tool_function)

# Register the ABAP DDIC data element tools
for tool_name, tool_function in data_element.get_tools():
    mcp.tool(name=tool_name)(tool_function)

# Register the ABAP DDIC structure tools
for tool_name, tool_function in structure.get_tools():
    mcp.tool(name=tool_name)(tool_function)

# Register the ABAP DDIC database table tools
for tool_name, tool_function in database_table.get_tools():
    mcp.tool(name=tool_name)(tool_function)

# Register the ABAP DDIC table type tools
for tool_name, tool_function in table_type.get_tools():
    mcp.tool(name=tool_name)(tool_function)

# Register the ABAP CDS view tools
for tool_name, tool_function in cds.get_tools():
    mcp.tool(name=tool_name)(tool_function)

# Register the ABAP SQL tools
for tool_name, tool_function in sql.get_tools():
    mcp.tool(name=tool_name)(tool_function)

# Register the ABAP program tools
for tool_name, tool_function in program.get_tools():
    mcp.tool(name=tool_name)(tool_function)

# Register the ABAP function module tools
for tool_name, tool_function in function_module.get_tools():
    mcp.tool(name=tool_name)(tool_function)

# Register the ABAP OO class tools
for tool_name, tool_function in oo_class.get_tools():
    mcp.tool(name=tool_name)(tool_function)

# Register the ABAP OO interface tools
for tool_name, tool_function in oo_interface.get_tools():
    mcp.tool(name=tool_name)(tool_function)

def main():
    # Initialize and run the server
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()