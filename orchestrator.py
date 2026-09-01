import asyncio
import sys
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from config import OPENAI_API_KEY


async def run_video_query(user_query: str):
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Load tools from local FastMCP server
            tools = await load_mcp_tools(session)

            model = ChatOpenAI(
                model="gpt-4o", api_key=OPENAI_API_KEY, temperature=0.0
            ).bind_tools(tools)

            system_instruction = (
                "You are an AI Video Assistant. Answer questions about uploaded"
                " videos strictly using the provided search tool. Always include"
                " timestamps in your final answer when referencing events."
            )

            messages = [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_query},
            ]

            response = await model.ainvoke(messages)

            # Agentic tool call handling
            if response.tool_calls:
                messages.append(response)

                for tool_call in response.tool_calls:
                    tool_to_call = next(
                        t for t in tools if t.name == tool_call["name"]
                    )
                    tool_output = await tool_to_call.ainvoke(tool_call["args"])

                    messages.append({
                        "role": "tool",
                        "content": str(tool_output),
                        "tool_call_id": tool_call["id"],
                    })

                final_response = await model.ainvoke(messages)
                return final_response.content

            return response.content


if __name__ == "__main__":
    prompt = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "What main events happen in the video and at what timestamps?"
    )
    answer = asyncio.run(run_video_query(prompt))
    print("\n=== ANSWER ===")
    print(answer)
