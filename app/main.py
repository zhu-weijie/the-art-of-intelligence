from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tools.planning import TodoListTool
from tools.filesystem import FileSystemTool

app = FastAPI()

# --- Tool Instantiation ---
# Create a single, shared instance of the filesystem tool
# This allows it to maintain state between API calls.
fs_tool = FileSystemTool()


class PlanRequest(BaseModel):
    tasks: list[str]


class FileWriteRequest(BaseModel):
    filename: str
    content: str


# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/plan")
def create_a_plan(plan_request: PlanRequest):
    todo_tool = TodoListTool()
    return todo_tool.create_plan(tasks=plan_request.tasks)


@app.post("/files/write")
def write_a_file(request: FileWriteRequest):
    """Writes content to a file in the virtual filesystem."""
    return fs_tool.write_file(request.filename, request.content)


@app.get("/files/read/{filename}")
def read_a_file(filename: str):
    """Reads content from a file in the virtual filesystem."""
    result = fs_tool.read_file(filename)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@app.get("/files/list")
def list_all_files():
    """Lists all files in the virtual filesystem."""
    return fs_tool.list_files()
