from mcp.server.fastmcp import FastMCP 
import json 


##Create a MCP server
mcp = FastMCP("Calculator")

# This logic is for annotations. This is not implemnted in fastMCP yet.
#once implemented you can change it to
#eg:- @mcp.tool(tools_metadata['add_function']) 

# with open("tool_config.json", "r") as f:
#     tools_metadata = json.load(f)


@mcp.tool()
def add(a:float, b:float) -> float:
    """Adds two numbers.  
    Args:
    a: Input 1
    b: input 2 """
    
    return a+b

@mcp.tool()
def subtract(a:float, b:float) -> float:
    """Subtracts two numbers.
    Args:
    a: Input 1
    b: Input 2"""

    return a-b

@mcp.tool()
def multiply(a:float, b:float) -> float:
    """Multiplies 2 numbers.
        Args:
        a: Input 1
        b: Input 2
    """

    return a*b

@mcp.tool()
def divide(a:float, b:float) -> str | float:
    """Divides 2 numbers
        Args:
        a: Dividend
        b: Divisor"""

    if b == 0:
        return "Cannot divide by zero."
    else:
        return a/b

@mcp.tool()
def modulo(a:float, b:float) -> str | float:
    """ Remainder from dividing 2 numbers
        Args:
        a: Divdiend
        b: Divisor"""


    if b == 0:
        return "Remainder does not exist when dividing by 0"
    else:
        return a%b


if __name__ == "__main__":
    mcp.run(transport='stdio')