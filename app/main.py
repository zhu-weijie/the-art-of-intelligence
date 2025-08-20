from fastapi import FastAPI
from pydantic import BaseModel
from app.tools.planning import TodoListTool

app = FastAPI()


# Define the request body model
class PlanRequest(BaseModel):
    tasks: list[str]


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Add the new endpoint
@app.post("/plan")
def create_a_plan(plan_request: PlanRequest):
    """
    Receives a list of tasks and uses the TodoListTool to process them.
    """
    todo_tool = TodoListTool()
    result = todo_tool.create_plan(tasks=plan_request.tasks)
    return result
