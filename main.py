from dotenv import load_dotenv
from agent import run_agent

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
    if not user_input:
        continue

    print("Agent thinking...")
    response = run_agent(user_input, messages)
    print(f"\nAgent: {response}\n")
