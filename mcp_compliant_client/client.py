##References examples from official python-sdk implementation from mcp



import os
from dotenv import load_dotenv
import asyncio
from async_exit_stack import AsyncExitStack 
import sys
from typing import Optional
import logging


##MCP specific imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

#LLM
from anthropic import Anthropic

#System prompts
import system_prompt


class MCP_Calc_Client:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

        #load the LLM API KEY - Anthropic in this example
        load_dotenv()
        MODEL_API_KEY = os.environ.get("CLAUDE_API_KEY")

        self.anthropic = Anthropic(api_key = MODEL_API_KEY)

    async def connect_to_server(self,server_file_path:str):
        """Connect to the server and get the read and write streams"""

        if not server_file_path.endswith(".py"):
            raise ValueError("Only python servers are supported")
        
        server_params = StdioServerParameters(
            command = "python",
            args = [server_file_path],
            env = None ## put you API KEY here if any of your tools/resources need API_KEY. Eg:- Web search
        )

        
        ##Connection to server which return read and write stream controls
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.read, self.write = stdio_transport 
        ##Connection between client and server using the previous control streams
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.read, self.write))

        await self.session.initialize()


    async def return_tool_info(self):
        """ Return tool info. This will change based on the LLM used"""

        available_tools = await self.session.list_tools()

        return [{ 
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
            
            } for tool in available_tools.tools]

    async def check_if_tool_exist(self, tool_name:str) -> bool:

        """Check if a particular tool exists. Helpful when working with multiple servers concurrently"""

        tools = await self.session.list_tools()
        avail_tools = [tool.name for tool in tools.tools]
        return True if tool_name in avail_tools else False

    async def tool_text_response(self, tools_info, messages):
            model_response = self.anthropic.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1000,
            temperature=0,
            messages=messages,
            tools=tools_info,
            system=system_prompt.TOOL_CALLER_PROMPT)

            return model_response


    async def process_query(self, messages):

        """ 2 step LLM call; 1 to select the tool another to present the output nicely"""


        response_to_user = []
        tools_info = await self.return_tool_info()

        ##Can return either a text/tool block  or both
        model_response = await self.tool_text_response(tools_info, messages)

        for response in model_response.content:
            if response.type == "text":
                response_to_user.append(response.text)

            elif response.type == "tool_use" :

                ##Check if the tool exists then execute
                if await self.check_if_tool_exist(response.name):

                    tool_result = await self.session.call_tool(response.name, response.input)
                    response_to_user.append(f"Calling tool {response.name} with args {response.input}")

                else:
                    raise NotImplementedError("Tool doesnot exist to perform this operation")

                ##Tool results are always user role, since this not model generated.
                messages.append({
                    "role":"user",
                    "content": tool_result.content
                })

                ##Present a clean response
                clean_response = self.anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    temperature=0,
                    messages=messages,
                    system=system_prompt.OUTPUT_PRESENTER_PROMPT
                )

                response_to_user.append(clean_response.content[0].text)

        return "\n".join(response_to_user)



    async def chat_loop(self):
        print("Calculator app started. Please enter quit or exit to close")

        while True:
            messages = []
            query = input("Query: ").strip()
            messages.append({
                "role":"user",
                "content":query
            })

            if query.lower() == "quit" or query.lower() == "exit":
                break
            
            response = await self.process_query(messages)
            
            print("\n" + response)


    async def cleanup(self):
        """Clean up resources elegantly"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        logging.error("Usage: python <client_file_name> <path_to_server_file>")
        sys.exit(1)

    client = MCP_Calc_Client()

    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
