from .base import Tool


class TodoListTool(Tool):
    """A tool for creating and displaying a plan."""

    def create_plan(self, tasks: list[str]):
        """
        Takes a list of tasks, prints them as a plan,
        and returns a confirmation.
        """
        print("\n--- To-Do Plan ---")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
        print("--------------------\n")
        return {"status": "success", "message": "Plan created and logged."}
