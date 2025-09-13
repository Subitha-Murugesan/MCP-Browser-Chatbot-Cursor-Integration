# MCP Browser Chatbot (Cursor Integration)

A conversational **MCP client** built with Python, [LangChain](https://www.langchain.com/), and [Groq LLMs](https://groq.com/) — designed to run inside **Cursor**.

This chatbot connects to multiple MCP servers (Playwright, DuckDuckGo search, Airbnb, etc.) and lets you control them conversationally, either in the terminal or through Cursor’s MCP integration.

---

## Features

* **Cursor-native**: Add this project as an MCP client inside Cursor.
* Talks to **all MCP servers** defined in `browser_mcp.json`.
* Automates browser interactions via **Playwright MCP**.
* Search the web with **DuckDuckGo MCP**.
* Query Airbnb listings with **OpenBNB MCP**.
* Memory-enabled conversations (clearable on demand).
* Powered by **Groq LLMs** (`qwen3-32b`, `llama3`, etc.).

---

## Setup with `uv`

1. **Initialize the project**

   ```bash
   uv init mcpdemo
   cd mcpdemo
   ```

2. **Create & activate a virtual environment**

   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   uv add langchain-groq
   uv add mcp-use
   ```

4. **Add chatbot script** (`main.py`) to the project root:

   ```python
   import asyncio
   import os
   from dotenv import load_dotenv
   from langchain_groq import ChatGroq
   from mcp_use import MCPAgent, MCPClient

   async def run_memory_chat():
       load_dotenv()
       os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

       print("Initializing chat")

       client = MCPClient.from_config_file(
           os.path.join(os.path.dirname(__file__), "browser_mcp.json")
       )

       llm = ChatGroq(model="qwen/qwen3-32b")

       agent = MCPAgent(llm=llm, client=client, max_steps=15, memory_enabled=True)

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

               print("chatbot:", end="", flush=True)

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
   ```

5. **Add environment variables**
   Create a `.env` file with your Groq API key:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

6. **Configure MCP servers** in `browser_mcp.json`:

   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp@latest"]
       },
       "duckduckgo-search": {
         "command": "npx",
         "args": ["-y", "duckduckgo-mcp-server"]
       },
       "airbnb": {
         "command": "npx",
         "args": ["-y", "@openbnb/mcp-server-airbnb"]
       }
     }
   }
   ```

---

## Run the Chatbot

```bash
uv run python main.py
```

Example:

```
Enter your message: search for cafes near Paris
chatbot:
Result: Found 10 cafes near Paris...
```
```
Enter your message: 
please open google.com and then open makemytrip.com
chatbot:
<img width="2170" height="1108" alt="image" src="https://github.com/user-attachments/assets/7d59a203-7401-4412-b6a2-d96273a0b7b1" />
<img width="2404" height="1604" alt="image" src="https://github.com/user-attachments/assets/b908f13d-e015-422c-9244-94a06beaba4f" />

```
```
Enter your message:Give top AI news
chatbot:
<img width="2404" height="1662" alt="image" src="https://github.com/user-attachments/assets/61c177ec-09c6-4a68-97c4-dfea8273db65" />
```

### Commands

* `clear` → Clear conversation history
* `exit | quit | bye` → Exit chatbot

---

## Configure Cursor for MCP

1. Open **Cursor Settings**

   * Go to **Cursor Settings → MCP and Integrations**

2. Click **Add Custom MCP**
   <img width="2170" height="1108" alt="image" src="https://github.com/user-attachments/assets/f0db346a-5a3d-4daf-b40f-f5dca54e404e" />



4. Cursor will open (or create) your `mcp.json` file. Add your server config there, for example:

   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp@latest"]
       },
       "duckduckgo-search": {
         "command": "npx",
         "args": ["-y", "duckduckgo-mcp-server"]
       },
       "airbnb": {
         "command": "npx",
         "args": ["-y", "@openbnb/mcp-server-airbnb"]
       }
     }
   }
   ```

5. **Save the file** → Cursor will now recognize and connect to these MCP servers.

---
