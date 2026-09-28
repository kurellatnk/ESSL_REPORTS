import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentType, initialize_agent
from langchain_core.tools import StructuredTool

# 1. Load environment secrets
load_dotenv()

print("=== Initializing Autonomous AI Agent ===")

# 2. Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)

# 3. Create a clean tool wrapper for the agent
def check_system_security(dummy_arg: str = "none") -> str:
    """Checks the local environment security status and returns a diagnostic report."""
    return "Diagnostic Report: Firewall status ACTIVE. Dual gateways operational. No unauthorized entries detected."

# Explicitly map it as a single-input structured tool
tools = [
    StructuredTool.from_function(
        func=check_system_security,
        name="check_system_security",
        description="Checks the local environment security status and returns a diagnostic report."
    )
]

# 4. Initialize the Agent with error handling enabled
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True  # Automatically fixes LLM text formatting slips!
)

# 5. Give the agent a complex goal
goal = "Run a security check on the local infrastructure and summarize the status for the lead architect."
print(f"\nAgent Goal: {goal}\n")

response = agent.invoke({"input": goal})

print(f"\nAgent Final Output:\n{response['output']}")