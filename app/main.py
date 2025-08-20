from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tools.planning import TodoListTool
from tools.filesystem import FileSystemTool
from agents.deep_agent import DeepAgent
from prompts.system import GENERAL_SYSTEM_PROMPT
from typing import Any
from agents.sub_agent import SubAgent
from agents.sub_agent_configs import all_sub_agents

app = FastAPI()

# --- Tool Instantiation ---
fs_tool = FileSystemTool()
todo_tool = TodoListTool()

# --- Agent Instantiation ---
deep_agent = DeepAgent(
    tools={"file_system": fs_tool, "planning": todo_tool},
    sub_agents=all_sub_agents,
    system_prompt=GENERAL_SYSTEM_PROMPT,
)


class ChatRequest(BaseModel):
    query: str


class PlanRequest(BaseModel):
    tasks: list[str]


class FileWriteRequest(BaseModel):
    filename: str
    content: str


class ToolRunRequest(BaseModel):
    tool_name: str
    kwargs: dict[str, Any]


# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"Hello": "World"}


# --- Agent Endpoints ---
@app.post("/agent/chat")
def agent_chat(request: ChatRequest):
    """
    The main endpoint for interacting with the deep agent.
    Simulates a chat response by returning a plan of action.
    """
    return deep_agent.chat(query=request.query)


@app.get("/agent/sub-agents", response_model=list[SubAgent])
def get_sub_agents():
    """Returns the configuration of all registered sub-agents."""
    return list(deep_agent.sub_agents.values())


@app.post("/agent/run-tool")
def agent_run_tool(request: ToolRunRequest):
    """Commands the agent to run a specific tool with given arguments."""
    result = deep_agent.run_tool(tool_name=request.tool_name, **request.kwargs)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.get("/agent/prompt")
def get_agent_prompt():
    """Returns the system prompt the agent was initialized with."""
    return {"system_prompt": deep_agent.system_prompt}


# --- Tool Endpoints ---
@app.post("/plan")
def create_a_plan(plan_request: PlanRequest):
    return todo_tool.create_plan(tasks=plan_request.tasks)


@app.post("/files/write")
def write_a_file(request: FileWriteRequest):
    return fs_tool.write_file(request.filename, request.content)


@app.get("/files/read/{filename}")
def read_a_file(filename: str):
    result = fs_tool.read_file(filename)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@app.get("/files/list")
def list_all_files():
    return fs_tool.list_files()
