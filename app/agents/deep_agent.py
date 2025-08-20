from .base import Agent
from tools.filesystem import FileSystemTool
from tools.planning import TodoListTool
from .sub_agent import SubAgent


class DeepAgent(Agent):
    """The main class for the deep agent."""

    def __init__(self, tools: dict, sub_agents: list[SubAgent], system_prompt: str):
        self.tools = tools
        self.sub_agents = {agent.name: agent for agent in sub_agents}
        self.system_prompt = system_prompt
        print("DeepAgent initialized.")
        print(f"Registered Sub-Agents: {list(self.sub_agents.keys())}")

    def run_tool(self, tool_name: str, **kwargs):
        """
        Runs a specified tool with the given arguments.
        This is a simplified dispatcher.
        """
        if tool_name not in self.tools:
            return {"status": "error", "message": f"Tool '{tool_name}' not found."}

        tool = self.tools[tool_name]

        # Simplified logic: map tool name to a specific method
        if tool_name == "file_system" and isinstance(tool, FileSystemTool):
            # For this example, we'll assume the action is 'write_file'
            filename = kwargs.get("filename")
            content = kwargs.get("content")
            if not filename or content is None:
                return {
                    "status": "error",
                    "message": "Missing 'filename' or 'content' for file_system tool.",
                }
            return tool.write_file(filename=filename, content=content)

        elif tool_name == "planning" and isinstance(tool, TodoListTool):
            tasks = kwargs.get("tasks")
            if not tasks:
                return {
                    "status": "error",
                    "message": "Missing 'tasks' for planning tool.",
                }
            return tool.create_plan(tasks=tasks)

        else:
            return {
                "status": "error",
                "message": f"No action defined for tool '{tool_name}'.",
            }

    def chat(self, query: str):
        """
        Simulates the agent's thinking process in response to a query.
        Returns a mocked plan of action.
        """
        print(f"Received query: {query}")

        # This is the mocked "thinking" process.
        # In a real implementation, an LLM call would generate this plan.
        mock_plan = {
            "user_query": query,
            "thought": "The user wants me to perform a research task. I need to break this down into a plan, use my tools to manage the process, and delegate to my specialized sub-agents.",
            "plan_of_action": [
                {
                    "step": 1,
                    "action": "use_tool",
                    "tool_name": "planning",
                    "arguments": {
                        "tasks": [
                            "Write the original question to 'question.txt'",
                            "Delegate the main research to the 'research-agent'",
                            "Write the research findings to 'final_report.md'",
                            "Delegate the critique of the report to the 'critique-agent'",
                        ]
                    },
                },
                {
                    "step": 2,
                    "action": "use_tool",
                    "tool_name": "file_system",
                    "arguments": {"filename": "question.txt", "content": query},
                },
                {
                    "step": 3,
                    "action": "delegate_to_sub_agent",
                    "sub_agent_name": "research-agent",
                    "instructions": "Please conduct a detailed investigation into the user's query.",
                },
                {
                    "step": 4,
                    "action": "delegate_to_sub_agent",
                    "sub_agent_name": "critique-agent",
                    "instructions": "Please review the file 'final_report.md' and provide feedback for improvement.",
                },
            ],
        }
        return mock_plan
