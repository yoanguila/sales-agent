import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import get_sales_by_month, get_top_product, compare_months, get_total_revenue

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_sales_by_month",
            "description": "Get total revenue and units sold for a specific month.",
            "parameters": {
                "type": "object",
                "properties": {
                    "month": {"type": "string", "description": "Month name, e.g. 'January'"}
                },
                "required": ["month"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_product",
            "description": "Get the best-selling product by revenue. Can be filtered by month.",
            "parameters": {
                "type": "object",
                "properties": {
                    "month": {"type": "string", "description": "Optional month filter"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_months",
            "description": "Compare total revenue between two months.",
            "parameters": {
                "type": "object",
                "properties": {
                    "month_a": {"type": "string", "description": "First month"},
                    "month_b": {"type": "string", "description": "Second month"}
                },
                "required": ["month_a", "month_b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_total_revenue",
            "description": "Get total revenue and units sold across all months.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

FUNCTION_MAP = {
    "get_sales_by_month": get_sales_by_month,
    "get_top_product": get_top_product,
    "compare_months": compare_months,
    "get_total_revenue": get_total_revenue,
}

def run_agent(user_message: str, messages: list) -> str:
    messages.append({"role": "user", "content": user_message})

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS
        )

        choice = response.choices[0]

        if choice.finish_reason == "stop":
            messages.append({"role": "assistant", "content": choice.message.content})
            return choice.message.content
        
        if choice.finish_reason == "tool_calls":
            messages.append(choice.message)

            for tool_call in choice.message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"  [calling {name} with {args}]")

                func = FUNCTION_MAP.get(name)
                result = func(**args) if func else {"error": f"Unknown function: {name}"}


                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })