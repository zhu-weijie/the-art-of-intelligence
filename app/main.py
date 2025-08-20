from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tools.planning import TodoListTool
from tools.filesystem import FileSystemTool
from agents.deep_agent import DeepAgent
from prompts.system import GENERAL_SYSTEM_PROMPT

app = FastAPI()

# --- Tool Instantiation ---
fs_tool = FileSystemTool()
todo_tool = TodoListTool()

# --- Agent Instantiation ---
# Create a single, shared instance of our agent
deep_agent = DeepAgent(tools=[fs_tool, todo_tool], system_prompt=GENERAL_SYSTEM_PROMPT)


class PlanRequest(BaseModel):
    tasks: list[str]


class FileWriteRequest(BaseModel):
    filename: str
    content: str


# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"Hello": "World"}


# --- New Agent Endpoint ---
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
