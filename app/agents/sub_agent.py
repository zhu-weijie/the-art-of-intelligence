from pydantic import BaseModel


class SubAgent(BaseModel):
    """A data model for defining a sub-agent."""

    name: str
    description: str
    prompt: str
