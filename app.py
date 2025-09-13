#create a chatbot which will interact with the browser using the playwright mcp server

#i should communicate to all mcp servers in the browser_mcp.json file

import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

async def run_memory_chat():
    # Load environment variables
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


    print("Initializing chat")
    # Create MCPClient from config file
    client = MCPClient.from_config_file(
        os.path.join(os.path.dirname(__file__), "browser_mcp.json")
    )

    # Create LLM
    llm = ChatGroq(model="qwen/qwen3-32b")
    # Alternative models:
    # llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    # llm = ChatGroq(model="llama3-8b-8192")

    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=15,memory_enabled=True)

    try:
        while True:
            user_input = input("Enter your message: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Exiting chat")
                break
            if user_input.lower() in ["clear"]:
                agent.clear_conversation_history()
                print("Conversation history cleared")
                continue

            print("chatbot:",end="",flush=True)

            try:
                result = await agent.run(user_input)
                print(f"\nResult: {result}")
            except Exception as e:
                print(f"Error: {e}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
