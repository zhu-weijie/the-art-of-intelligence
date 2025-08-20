from .base import Agent


class DeepAgent(Agent):
    """The main class for the deep agent."""

    def __init__(self, tools: list, system_prompt: str):
        self.tools = tools
        self.system_prompt = system_prompt
        print("DeepAgent initialized.")
        print(f"System Prompt: {self.system_prompt[:100]}...")
