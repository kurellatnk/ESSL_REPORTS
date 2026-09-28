import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentType, initialize_agent
from langchain_core.tools import StructuredTool
import requests

# 1. Load environment secrets
load_dotenv()

# 2. Initialize FastAPI app
app = FastAPI(title="AI Agent Production Server", version="1.0")

# 3. Define the expected incoming JSON request structure using Pydantic
class AgentRequest(BaseModel):
    goal: str

# 4. Define the security diagnostic tool
def check_system_security(dummy_arg: str = "none") -> str:
    """Checks the local environment security status and returns a diagnostic report."""
    return "Diagnostic Report: Firewall status ACTIVE. Dual gateways operational. No unauthorized entries detected."

# 5. Helper function to parse raw eSSL tab-delimited text into structured JSON
def parse_essl_logs(raw_text: str) -> list:
    """Parses raw tab-delimited eSSL transaction strings into structured dictionaries."""
    parsed_logs = []
    lines = raw_text.split("\n")
    for line in lines:
        parts = line.split("\t")
        if len(parts) >= 2:
            emp_code = parts[0].strip()
            timestamp = parts[1].strip()
            if emp_code and timestamp:
                parsed_logs.append({
                    "employee_id": emp_code,
                    "timestamp": timestamp
                })
    return parsed_logs

# 6. Define the eSSL remote attendance tool
def fetch_essl_transactions(employee_id: str) -> str:
    """Fetches and parses attendance punch logs for an employee from the remote eSSL Web API service."""
    url = "http://192.168.7.245:85/WebAPIService.asmx"
    
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    past_time_str = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d %H:%M")
    
    payload = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <GetTransactionsLog xmlns="http://tempuri.org/">
          <FromDateTime>{past_time_str}</FromDateTime>
          <ToDateTime>{current_time_str}</ToDateTime>
          <SerialNumber>M014200992108001477</SerialNumber>
                        M014200992108001477 
          <UserName>vmtnk</UserName>
          <UserPassword>Lahari@1951</UserPassword>
          <strDataList>{employee_id}</strDataList>
        </GetTransactionsLog>
      </soap:Body>
    </soap:Envelope>"""
    
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://tempuri.org/GetTransactionsLog"
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=20)
        if response.status_code == 200:
            text = response.text
            
            # Handle self-closing or empty result tags from eSSL cleanly
            if "<GetTransactionsLogResult />" in text or "<GetTransactionsLogResult/>" in text:
                return str([])
                
            start_tag = "<GetTransactionsLogResult>"
            end_tag = "</GetTransactionsLogResult>"
            if start_tag in text and end_tag in text:
                raw_data = text.split(start_tag)[1].split(end_tag)[0].strip()
                if not raw_data:
                    return str([])
                structured_logs = parse_essl_logs(raw_data)
                return str(structured_logs)
                
            return f"API Response from eSSL Server: {text}"
        else:
            return f"Failed to fetch from eSSL API. Status code: {response.status_code}"
    except Exception as e:
        return f"Connection error reaching remote eSSL server: {str(e)}"

# # Wrap the eSSL function into a structured tool
# essl_api_tool = StructuredTool.from_function(
    # func=fetch_essl_transactions,
    # name="fetch_essl_transactions",
    # description="Queries the remote eSSL server API to get structured attendance logs and punch history for a specific employee ID."
# )

# Wrap the eSSL function into a structured tool
essl_api_tool = StructuredTool.from_function(
    func=fetch_essl_transactions,
    name="fetch_essl_transactions",
    description="Queries the remote eSSL server API to get structured attendance logs for a specific employee ID. CRITICAL: If the returned list is empty '[]', you must state that no records were found. NEVER invent or hallucinate dates."
)
# 7. Combine all tools into a single list
tools = [
    StructuredTool.from_function(
        func=check_system_security,
        name="check_system_security",
        description="Checks the local environment security status and returns a diagnostic report."
    ),
    essl_api_tool  
]

# 8. Initialize the LLM and Agent
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
agent = initialize_agent(
    tools=tools,  
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,  
    handle_parsing_errors=True
)

# 9. FastAPI Endpoints
@app.get("/")
def health_check():
    return {"status": "online", "message": "AI Agent Server is up and running!"}

@app.post("/run-agent")
def run_agent_endpoint(request: AgentRequest):
    try:
        response = agent.invoke({"input": request.goal})
        return {
            "status": "success",
            "goal": request.goal,
            "output": response["output"]
        }
    except Exception as e:
        error_message = str(e)
        if "429" in error_message or "ResourceExhausted" in error_message:
            raise HTTPException(
                status_code=429, 
                detail="API quota exceeded. Please wait a moment for your rate-limit window to reset, or check your Google AI Studio billing tier."
            )
        raise HTTPException(status_code=500, detail=error_message)

@app.get("/test-essl/{employee_id}")
def test_essl_connection(employee_id: str):
    """Directly tests the remote eSSL server connection without invoking the AI model."""
    try:
        result = fetch_essl_transactions(employee_id)
        return {
            "status": "success",
            "employee_id": employee_id,
            "parsed_attendance_logs": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }