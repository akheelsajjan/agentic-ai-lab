from pydantic import BaseModel


class ToolDependency(BaseModel):
    tool: str
    depends_on: list[str] = []