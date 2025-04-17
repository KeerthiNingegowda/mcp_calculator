# A simple calculator app using Model Context protocol

#### Purpose of this repo
To explore basic building blocks of MCP and intricacies of tool calling within MCP, from scratch. Keeping it as simple as possible without handling many edge cases.

#### Core Features
<li> A calculator app to do add, subtract, multiply, divide and modulo</li>
<li> Debugging server using MCP Inspector </li
<li> A MCP-based client that takes a query from the user to perform the above mentioned operations </li>

#### Future possibilities for quick concept exploration
<li>Sequential tool calling</li>
<li> Storage of previous chat history is not supported to maintain simplicity </li>


<b> 🚨 Most of the technolgies used in this repo like FastMCP, tool calling in anthropic and MCP itself are very recent. So there are some features in these technologies that are either not available or buggy. But the main goal is a simple exploration without using cursor or Claude Desktop 🚨 </b>

#### MCP compliant Calculator Server
Is built using FastMCP, due to its simplicty and automatic error handling. 
Points to remember:-
<li> Always name the server either as mcp or server or app. Throws an error otherwise and is quite explicit </li>
<li>Annotations can be included as a future reference. Right now it is not supported in FastMCP for the version in uv.lock</li>

#### To reproduce the working environment
`uv sync`

Add your anthropic API key to .env file

More about this on link to medium article.
