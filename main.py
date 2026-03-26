import json
from dotenv import load_dotenv
from agent import run_agent, run_agent_structured, run_agent_streaming

load_dotenv()

print("Sales Agent ready. Type 'exit' to quit.\n")

messages = [
    {
        "role": "system",
        "content": (
            "You are a sales analysis assistant. "
            "Use the available tools to answer questions about sales data. "
            "Always use real data from the tools — never guess or estimate. "
            "Be concise and clear in your answers."
        )
    }
]

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        break
    if user_input.lower().startswith("json:"):
        query = user_input[5:].strip()
        print("Agent thinking (structured)...")
        result = run_agent_structured(query, messages)
        print(f"\nAgent (JSON): {json.dumps(result, indent=2)}\n")
    elif user_input.lower().startswith("stream"):
        query = user_input[7:].strip()
        print("Agent thinking...")
        run_agent_streaming(query, messages)
    else:
        print("Agent thinking...")
        response = run_agent(user_input, messages)
        print(f"\nAgent: {response}\n")