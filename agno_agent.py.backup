from agno.agent import Agent
from agno.models.google import Gemini
from agno.os import AgentOS
from agno.tools.mcp import MCPTools
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create the Agent
agno_agent = Agent(
    name="Agno Agent",
    model=Gemini(id="gemini-flash-latest"),
    tools=[MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")],
    add_history_to_context=True,
    markdown=True,
)

# Create the AgentOS
agent_os = AgentOS(agents=[agno_agent])
app = agent_os.get_app()

if __name__ == "__main__":
    print("🚀 Starting Agno Agent")
    print("📊 API docs: http://localhost:8000/docs")
