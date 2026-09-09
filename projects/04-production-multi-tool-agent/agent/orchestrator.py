from concurrent.futures import ThreadPoolExecutor
from tools.registry import TOOLS


def execute_tool(tool_call):
    try:
        tool = TOOLS[tool_call.tool]
        result = tool.invoke(tool_call.arguments)

        return tool_call.tool, {
            "status": "success",
            "result": result,
        }

    except Exception as e:
        return tool_call.tool, {
            "status": "error",
            "error": str(e),
        }


def execute_tools(route) -> dict:
    with ThreadPoolExecutor() as executor:
        results = executor.map(execute_tool, route.tool_calls)

    return dict(results)